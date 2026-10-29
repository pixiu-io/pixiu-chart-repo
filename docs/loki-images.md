# Loki 镜像列表

对应 Chart：`loki`

| 项 | 值 |
| --- | --- |
| Chart | [loki](https://github.com/grafana/loki/tree/main/production/helm/loki) |
| Chart 版本 | **7.5.0**（仓库文件：`charts/loki-7.5.0.tgz`） |
| appVersion | **3.6.16**（Chart 内默认 Loki Server 镜像 tag 为 3.6.11） |
| 来源 | [grafana/helm-charts](https://github.com/grafana/helm-charts)（官方 Helm 仓库） |
| Pixiu 默认调整 | 镜像替换为华为云 SWR mirror；默认 values 调整为开箱即装：SingleBinary 1 副本 + replication_factor 1 + filesystem 存储 + 内置 schemaConfig + PVC 5Gi |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理（`deploymentMode: SingleBinary`，内置 memcached 缓存默认开启）。默认 values 已内置 filesystem 存储与 schemaConfig，开箱即装；使用对象存储的集群可改回 s3 并配置 bucketNames。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| loki server | `docker.io/grafana/loki:3.6.11` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/loki:3.6.11` | Loki 单二进制 Deployment |
| loki-canary | `docker.io/grafana/loki-canary:3.6.16` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/loki-canary:3.6.16` | 写入/读取探活 Canary DaemonSet |
| helm-test | `docker.io/grafana/loki-helm-test:latest` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/loki-helm-test:latest` | `helm test` Pod |
| gateway | `docker.io/nginxinc/nginx-unprivileged:1.29-alpine` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/nginx-unprivileged:1.29-alpine` | nginx 网关（`gateway.enabled` 默认 true） |
| memcached | `memcached:1.6.39-alpine` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/memcached:1.6.39-alpine` | chunks/results 内置缓存 |
| memcached-exporter | `prom/memcached-exporter:v0.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/memcached-exporter:v0.15.4` | 缓存指标导出 |
| k8s-sidecar | `docker.io/kiwigrid/k8s-sidecar:2.5.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/k8s-sidecar:2.5.0` | rules/dashboards 配置 sidecar |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| enterprise-logs | `grafana/enterprise-logs:3.6.16` | 仅启用 Grafana Enterprise Logs（需 license）时 |
| enterprise-provisioner | `grafanalabs-global/docker-enterprise-provisioner-prod/enterprise-provisioner:latest` | 同上 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/grafana/loki:3.6.11
docker.io/grafana/loki-canary:3.6.16
docker.io/grafana/loki-helm-test:latest
docker.io/nginxinc/nginx-unprivileged:1.29-alpine
memcached:1.6.39-alpine
prom/memcached-exporter:v0.15.4
docker.io/kiwigrid/k8s-sidecar:2.5.0
```

## 离线 / 私有仓库建议

1. 将上面的原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/`（保持 tag 不变）；
2. Chart 包内默认 values 已指向 SWR mirror，离线环境开箱即用；
3. 若使用其他私有仓库，按 `loki.image.repository`、`lokiCanary.image.repository`、`gateway.image.repository`、`memcached.image.repository`、`memcachedExporter.image.repository`、`sidecar.image.repository` 等整体替换前缀。

## 备注

- Chart 7.5.0 为 grafana 官方仓库当前最新稳定版。
- Pixiu 对默认 values 的调整（上游默认 `SimpleScalable` 模式、s3 存储、无 schemaConfig，直接安装会失败）：
  - `deploymentMode: SingleBinary` + `singleBinary.replicas: 1`（上游默认 0），write/read/backend 副本默认 0
  - `loki.commonConfig.replication_factor: 1`（上游 3）
  - `loki.storage.type: filesystem`（上游 s3，需 bucket）
  - `loki.schemaConfig`：tsdb + v13 + filesystem，from 2024-01-01
  - `singleBinary.persistence.size: 5Gi`（上游 10Gi，小磁盘集群 Longhorn 调度预检友好）
- 需要大规模部署时：改回 `SimpleScalable`/`Distributed` 模式并调高 write/read/backend 副本、replication_factor，存储改 s3/oss。
- Promtail 通过独立的 `promtail` chart（同仓库 `charts/promtail-6.17.1.tgz`）部署，作为 Loki 的日志采集端。
- 应用商店安装实录见下方「应用商店安装实录」章节。

## 应用商店安装实录（2026-10-29，pixiu-dev 单节点）

平台安装记录：`pixiu-system`，deploy_status=success / deployed。

### 实测通过的安装 values（已内化为 Chart 默认值，开箱即装；以下为调整前的手工 values 存档）

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

### 踩坑与解决

1. **安装失败：缺少 schema_config** —— 现象：`execution error at (loki/templates/validate.yaml): You must provide a schema_config`。默认 values 不带，必须显式提供 `loki.schemaConfig`（上例 tsdb + v13 + filesystem）。卸载失败 release 后同名重装即可。
2. **多租户鉴权**：loki 默认 `auth_enabled: true`，gateway 要求 `X-Scope-OrgID`。promtail 等客户端推送需配 `tenant_id`（见 [promtail-images.md](./promtail-images.md)），查询 API 同样要带 `X-Scope-OrgID: <租户>`，否则 401 no org id。
3. **Longhorn 卷 faulted（insufficient storage）**：Longhorn 按**卷声明大小**做调度预检（非实际占用），磁盘 maximum 39.3GiB、storageReserved 30%（11.8GiB）→ 可调度上限 27.5GiB，已有卷（minio 10+10、loki 5、test 1）+ 新卷 5Gi 超限即 faulted，Pod 卡 `FailedAttachVolume ... rpc error: code = Aborted`。解决：调低节点磁盘保留（PATCH `longhorn.io/v1beta2 .../nodes/<node>` 的 `spec.disks.<id>.storageReserved`，本次改为 10%≈3.9GiB），Longhorn 自动恢复调度、重建副本。**经验：单节点小磁盘集群装大容量应用前，先看 Longhorn「可调度余量」而不是剩余磁盘；新应用 PVC 5Gi 起步。**

### 验证结果

- Pod：loki-0 / loki-gateway / loki-chunks-cache-0 / loki-results-cache-0 全部 Running 且 Ready。
- 经平台 K8s 服务代理查 `/loki/api/v1/labels`（带 X-Scope-OrgID）返回 app/container/namespace/pod 等标签；`query_range` 能查到 promtail 采集的真实容器日志（含 gateway 自身 access log，promtail push 204）。

## 参考

- Chart 源码：<https://github.com/grafana/loki/tree/main/production/helm/loki>
- Loki 项目：<https://github.com/grafana/loki>
- Helm 仓库：`helm repo add grafana https://grafana.github.io/helm-charts`
