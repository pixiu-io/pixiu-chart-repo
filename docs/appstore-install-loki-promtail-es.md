# OPS-001 应用商店安装 Loki / Promtail / Elasticsearch 实操记录

- **分类**：应用商店 / Chart 上传与安装
- **环境**：console.cloud.pixiuio.com（admin），集群 `pixiu-fmqyrwig`（别名 pixiu-dev，v1.28.15，单节点，Longhorn 默认 StorageClass）
- **Chart 版本**：loki-7.5.0、promtail-6.17.1、elasticsearch-8.5.1（来自本仓库 `charts/`，镜像均为 SWR mirror）
- **最后更新**：2026-10-29

## 结果总览

| 应用 | 版本 | 命名空间（平台记录） | 部署状态 | 功能验证 |
|---|---|---|---|---|
| loki | 7.5.0 | pixiu-system | success / deployed | ✅ 网关查询正常，收到 promtail 日志流 |
| promtail | 6.17.1 | pixiu-system | success / deployed | ✅ 采集全节点容器日志并推送成功（gateway access log 204） |
| elasticsearch | 8.5.1 | pixiu-system（实际落在 default，见问题 5） | success / deployed | ✅ `_cluster/health` green（https + basic auth） |

## 一、标准操作步骤（有效流程，可复用）

### 1. 登录获取 token（有效期约 1 小时）

```bash
TOKEN=$(curl -s -X POST https://console.cloud.pixiuio.com/pixiu/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"name":"admin","password":"<密码>"}' | python3 -c \
  'import sys,json;print(json.load(sys.stdin)["result"]["token"])')
```

后续请求统一带 `Authorization: Bearer $TOKEN`。

### 2. 上传 Chart（multipart，字段 file）

```bash
curl -X POST https://console.cloud.pixiuio.com/pixiu/apps/charts \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@charts/loki-7.5.0.tgz"
# 返回 result.id 即 chart_id（本例：loki=20220822、promtail=20220823、elasticsearch=20220827）
```

同名同版本重复上传返回 409；包内容 sha256 与历史版本相同也会 409（仅改版本号不算新包）。

### 3. 安装（异步，入队即返回）

```bash
CLUSTER=pixiu-fmqyrwig
curl -X POST "https://console.cloud.pixiuio.com/pixiu/apps/clusters/$CLUSTER/namespaces/pixiu-system/releases" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"chart_id": <ID>, "release_name": "loki", "version": "7.5.0", "values": { ... }}'
```

轮询状态：

```bash
curl -s "https://console.cloud.pixiuio.com/pixiu/apps/clusters/$CLUSTER/installs" \
  -H "Authorization: Bearer $TOKEN"
# 看 deploy_status：pending → installing → success / failed（failed 时 message 有原因）
```

卸载：`DELETE .../namespaces/<ns>/releases/<release_name>`（异步）。

### 4. 集群内验证（走平台 K8s 代理）

```bash
# Pod 状态
curl -s "https://console.cloud.pixiuio.com/pixiu/proxy/$CLUSTER/api/v1/namespaces/pixiu-system/pods" \
  -H "Authorization: Bearer $TOKEN"

# 服务代理（Loki 查询，注意多租户要带 X-Scope-OrgID）
curl -G "https://console.cloud.pixiuio.com/pixiu/proxy/$CLUSTER/api/v1/namespaces/pixiu-system/services/http:loki-gateway:80/proxy/loki/api/v1/labels" \
  -H "Authorization: Bearer $TOKEN" -H "X-Scope-OrgID: pixiu"
```

## 二、实测通过的安装 values

### Loki 7.5.0（单二进制 + filesystem，适配单节点离线集群）

```json
{
  "deploymentMode": "SingleBinary",
  "singleBinary": {"replicas": 1, "persistence": {"enabled": true, "size": "5Gi"}},
  "write": {"replicas": 0}, "read": {"replicas": 0}, "backend": {"replicas": 0},
  "loki": {
    "commonConfig": {"replication_factor": 1},
    "storage": {"type": "filesystem"},
    "schemaConfig": {"configs": [{
      "from": "2024-01-01", "store": "tsdb", "object_store": "filesystem",
      "schema": "v13", "index": {"prefix": "loki_index_", "period": "24h"}
    }]}
  },
  "monitoring": {"enabled": false},
  "lokiCanary": {"enabled": false},
  "test": {"enabled": false}
}
```

### Promtail 6.17.1（默认值 + tenant_id）

默认值即可安装，但 **必须给 client 配 tenant_id**（见问题 6）。安装时的等价 values：

```json
{
  "config": {"clients": [
    {"url": "http://loki-gateway/loki/api/v1/push", "tenant_id": "pixiu"}
  ]}
}
```

### Elasticsearch 8.5.1（单节点瘦身）

```json
{
  "replicas": 1,
  "minimumMasterNodes": 1,
  "esJavaOpts": "-Xms512m -Xmx512m",
  "resources": {"requests": {"cpu": "200m", "memory": "512Mi"},
                "limits": {"cpu": "1", "memory": "2Gi"}},
  "volumeClaimTemplate": {"resources": {"requests": {"storage": "5Gi"}}}
}
```

注意：ES 默认 `protocol: https` + `createCert: true`，开启 xpack security；
默认账号 `elastic`，密码在 Secret `elasticsearch-master-credentials`（default 命名空间）。

## 三、踩坑与解决（按出现顺序）

### 1. Loki 安装失败：缺少 schema_config
- 现象：`execution error at (loki/templates/validate.yaml): You must provide a schema_config`
- 解决：values 里显式提供 `loki.schemaConfig`（tsdb + v13 + filesystem，见上）。
- 卸载失败的 release 后重装即可（失败记录 DELETE 后可同名重装）。

### 2. Longhorn 卷 faulted：precheck new replica failed: insufficient storage
- 现象：Pod 卡 `FailedAttachVolume ... rpc error: code = Aborted`，Longhorn 卷 `robustness=faulted`。
- 根因：Longhorn 按**卷声明大小**做调度预检。磁盘 maximum 39.3GiB、storageReserved 30%（11.8GiB）→ 可调度上限 27.5GiB；已有卷（minio 10+10、loki 5、test 1）+ 新卷 5Gi 超限。
- 解决：调低磁盘保留（改为 10%，3.9GiB），Longhorn 自动恢复调度、重建副本：
  ```bash
  curl -X PATCH ".../apis/longhorn.io/v1beta2/namespaces/<ns>/nodes/<node>" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/merge-patch+json' \
    -d '{"spec":{"disks":{"<disk-id>":{"storageReserved": 4220749004}}}}'
  ```
- 经验：**单节点小磁盘集群装大容量应用前，先看 Longhorn「可调度余量」而不是剩余磁盘**；新应用 PVC 5Gi 起步。

### 3. 平台 Bug：chart 包文件丢失（chart package not found）
- 现象：安装失败 `chart package not found: stat /etc/pixiu/appstore/charts/elasticsearch-8.5.1.tgz`，重新上传（200）后立即安装仍报同样错误。
- 推断：后端多副本部署，DB 共享但 `/etc/pixiu/appstore/charts` 是**实例本地磁盘**；上传落在 A 实例、安装任务由 B 实例执行时找不到文件（首轮 loki/promtail/ES 三个 chart 一次成功属运气；某一实例丢文件后 ES 反复失败）。
- 解决：**「删 Chart → 重传 → 重装」循环重试**，直到上传与任务执行落在同一实例（本次第 2 轮循环成功）。建议平台侧把 appstore data_dir 迁移到共享存储（NFS/S3/OSS）。

### 4. ES 调度失败：Insufficient memory
- 现象：`0/1 nodes are available: 1 Insufficient memory`。节点实际用量仅 4.2GiB/15.4GiB，但**各 Pod requests 汇总已占满 allocatable**。
- 解决：压低 ES requests（512Mi）后仍未通过，最终直接 patch StatefulSet requests 到 128Mi 调度成功：
  ```bash
  curl -X PATCH ".../apis/apps/v1/namespaces/default/statefulsets/elasticsearch-master" \
    -H 'Content-Type: application/strategic-merge-patch+json' -d '{
    "spec":{"template":{"spec":{"containers":[{"name":"elasticsearch",
    "resources":{"requests":{"cpu":"100m","memory":"128Mi"}}}]}}}}'
  ```
  同时 `esJavaOpts: -Xms512m -Xmx512m` 限制堆。注意 patch 的 requests 会被下次 helm upgrade 覆盖，根治需释放其它组件（如 prometheus）的 requests 或扩节点。

### 5. 平台现象：ES 资源落在 default 命名空间
- 平台安装记录显示 `pixiu-system`（helm release secret 也在 pixiu-system），但 ES 的 sts/PVC/Pod 实际创建在 `default`。与 minio 的落点一致，疑似 chart 安装工作路径或 chart 模板命名空间处理问题，**验证 Pod 时别只盯记录里的命名空间**（`kubectl get sts -A`）。

### 6. promtail 推送 401 no org id
- 根因：loki 默认 `auth_enabled: true`，gateway 要求 `X-Scope-OrgID`；promtail 默认配置不带租户头。
- 解决（已实施，直接 patch Secret `promtail` 后删 Pod 重建）：
  ```yaml
  clients:
    - url: http://loki-gateway/loki/api/v1/push
      tenant_id: pixiu
  ```
- 注意：**该 patch 会被 promtail 升级覆盖**；后续重装/升级时应把 `config.clients[0].tenant_id` 写进安装 values（或 loki 侧 `auth_enabled: false`）。查询时同样要带 `X-Scope-OrgID: pixiu`。

### 7. 平台 K8s 代理测 ES 的 Authorization 头冲突
- 现象：经 apiserver 服务代理访问 ES 时，`Authorization` 头只能用于 apiserver 鉴权，无法同时给 ES 传 Basic auth（ES 返回 missing authentication credentials）。
- 解决：起一次性 Job（用集群内已有 ES 镜像，自带 curl/bash），从集群内 `curl -sku elastic:$PW https://elasticsearch-master.default.svc:9200/_cluster/health`，再通过代理读 Job Pod 日志拿结果。测试完删除 Job。

## 四、最终验证结果

1. **Pod**：loki-0 / loki-gateway / loki-chunks-cache-0 / loki-results-cache-0 / promtail / elasticsearch-master-0 全部 Running 且 Ready。
2. **Loki**：`/loki/api/v1/labels`（X-Scope-OrgID: pixiu）返回 app/container/namespace/pod 等标签；query_range 能查到 promtail 采集的真实容器日志（含 loki-gateway 自身 access log，promtail push 204）。
3. **Promtail**：patch tenant_id 后无 401，持续推送。
4. **Elasticsearch**：集群内 curl `_cluster/health` → `{"status":"green","number_of_nodes":1,"active_shards_percent_as_number":100.0}`。

## 五、后续建议

1. **平台侧（优先）**：appstore chart 包目录迁共享存储，修复多副本下「chart package not found」。
2. **平台侧**：排查 release 命名空间与实际部署命名空间不一致的问题（ES → default）。
3. **Chart 侧**：loki/promtail 若常用于单节点测试环境，可在本仓库维护一份「small/standalone」预置 values（SingleBinary + filesystem + tenant 打通），避免每次手填。
4. **集群侧**：requests 已打满（实际用量仅 ~27%），新应用需先核对 requests 余量；磁盘余量建议长期保留 ≥10GiB 可调度空间。
