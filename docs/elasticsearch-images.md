# Elasticsearch 镜像列表

对应 Chart：`elasticsearch`

| 项 | 值 |
| --- | --- |
| Chart | [elasticsearch](https://github.com/elastic/helm-charts/tree/main/elasticsearch) |
| Chart 版本 | **8.5.1**（仓库文件：`charts/elasticsearch-8.5.1.tgz`） |
| appVersion | **8.5.1**（Elasticsearch 版本） |
| 来源 | [helm.elastic.co](https://helm.elastic.co)（Elastic 官方 Helm 仓库最新稳定版） |
| Pixiu 默认调整 | 镜像替换为华为云 SWR mirror；默认 values 调整为开箱即装：单副本（minimumMasterNodes 1）+ JVM 512m + 小资源 + PVC 5Gi |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。默认部署为 3 节点 StatefulSet（master/data 复合角色），所有节点共用同一镜像。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| elasticsearch 节点 | `docker.elastic.co/elasticsearch/elasticsearch:8.5.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/elasticsearch/elasticsearch:8.5.1` | Elasticsearch StatefulSet（默认 3 节点），含 `sysctlInitContainer`（同一镜像） |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| 无额外镜像 | — | Ingress、PDB、NetworkPolicy、PSP 等均为 ES 同镜像或不引入新镜像；values 中 `busybox` 仅为 preStop hook 注释示例，默认不渲染 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.elastic.co/elasticsearch/elasticsearch:8.5.1
```

## 离线 / 私有仓库建议

1. 将上面原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/elasticsearch/`（保持 tag 不变）；
2. Chart 包内默认 values 已指向 SWR mirror，离线环境开箱即用；
3. 若使用其他私有仓库，按 `image` 整体替换前缀（`imageTag` 单独控制版本）。

## 备注

- Chart 8.5.1 是 Elastic 官方 Helm 仓库（helm.elastic.co）当前最新稳定版；Elastic 在 8.5.1 之后已将 Elastic Stack Helm Charts 移交社区并归档（`elastic/helm-charts` 仓库 archived），后续版本官方推荐通过 ECK Operator 部署，不再发布传统 chart。
- Elasticsearch 安全自检（`xpack.security.enabled` 等）沿用 chart 默认值；默认开启 TLS 传输层认证（secret-cert.yaml），service 端口 `9200`（HTTP）/ `9300`（transport）。
- 默认资源已调低（单副本 + JVM 512m + requests 200m/512Mi + PVC 5Gi），单节点/小规格集群开箱即装；生产多节点集群请改回 replicas: 3 / minimumMasterNodes: 2 并调大资源与存储。
- 应用商店安装实录见下方「应用商店安装实录」章节。

## 应用商店安装实录（2026-10-29，pixiu-dev 单节点）

平台安装记录：`pixiu-system`，deploy_status=success / deployed；**实际资源（sts/PVC/Pod）落在 `default` 命名空间**（与 minio 落点一致，见踩坑 3）。

### 实测通过的安装 values（已内化为 Chart 默认值，开箱即装；以下为调整前的手工 values 存档）

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

### 踩坑与解决

1. **默认资源在单节点装不下（已内化修复）**：上游默认 3 副本、每副本 1C2G + 30Gi PVC；Chart 默认值已改为 `replicas: 1` + requests 200m/512Mi + JVM 512m + 5Gi PVC。生产多节点集群按需改回。
2. **调度失败 Insufficient memory**：节点实际用量很低，但各 Pod **requests 汇总**已占满 allocatable。压到 requests 512Mi 仍未通过，最终 patch StatefulSet requests 到 128Mi 才调度成功（注意 patch 会被下次 helm upgrade 覆盖，根治需释放其它组件 requests 或扩节点）。
3. **命名空间不一致**：平台安装记录写 `pixiu-system`（helm release secret 也在 pixiu-system），但 sts/PVC/Pod 实际在 `default`。验证 Pod 时用 `kubectl get sts -A` 别只盯记录。
4. **平台多副本下 chart 包文件丢失**：安装报 `chart package not found: stat /etc/pixiu/appstore/charts/elasticsearch-8.5.1.tgz`，需「删 Chart → 重传 → 重装」循环重试（平台级问题，见 [appstore-chart-guide.md](./appstore-chart-guide.md)）。
5. **Longhorn 卷 faulted（insufficient storage）**：ES 5Gi PVC 与其它新卷合计超过 Longhorn 可调度余量（平台级问题及解决方式见 [appstore-chart-guide.md](./appstore-chart-guide.md)）。
6. **经平台 K8s 代理验证 ES 受 Authorization 头冲突限制**：`Authorization: Bearer` 被 apiserver 消费，无法同时给 ES 传 Basic auth。解决：起一次性 Job 在集群内 `curl -sku elastic:$PW https://elasticsearch-master.default.svc:9200/_cluster/health`（密码从 Secret 读），再经代理读 Job Pod 日志取结果，测完删 Job。

### TLS 与凭据

- 默认 `protocol: https` + `createCert: true`，开启 xpack security，服务端口 9200 为 HTTPS。
- 默认账号 `elastic`，密码在 Secret `elasticsearch-master-credentials`（default 命名空间）`password` 字段。

### 验证结果

- Pod：elasticsearch-master-0 Running 且 Ready（init 容器 `configure-sysctl` 正常通过）。
- 集群内 curl `_cluster/health` → `{"status":"green","number_of_nodes":1,"active_shards_percent_as_number":100.0}`。

## 参考

- Chart 源码：<https://github.com/elastic/helm-charts/tree/main/elasticsearch>
- Elasticsearch 项目：<https://github.com/elastic/elasticsearch>
- Helm 仓库：`helm repo add elastic https://helm.elastic.co`
