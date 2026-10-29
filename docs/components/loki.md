# Loki（loki）

> 分类：可观测性　|　用途：日志聚合存储与查询，配合 Promtail 采集容器日志。

| 项 | 值 |
| --- | --- |
| Chart | [loki](https://github.com/grafana/loki/tree/main/production/helm/loki) |
| 仓库版本 | **7.5.0**（`charts/loki-7.5.0.tgz`） |
| appVersion | **3.6.16**（Chart 内默认 Loki Server 镜像 tag 为 3.6.11） |
| 来源 | [grafana/helm-charts](https://github.com/grafana/helm-charts)（官方 Helm 仓库） |
| 镜像清单 | [loki-images.md](../loki-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 7.5.0 | 3.6.16 | `charts/loki-7.5.0.tgz` | grafana 官方仓库当前最新稳定版；默认 SingleBinary 单副本 + filesystem（PVC）存储 |

Pixiu 默认调整：默认存储 `s3` → `filesystem`（PVC），配套 `deploymentMode: SingleBinary` 1 副本、write/read/backend 0 副本、`replication_factor: 1`、内置 `schemaConfig`（tsdb/v13/filesystem），PVC 大小保持上游默认 10Gi。

## 镜像

镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/`）。默认 values 下共拉取 7 个镜像：loki server、loki-canary、helm-test、gateway（nginx-unprivileged）、memcached、memcached-exporter、k8s-sidecar；内置 memcached 缓存默认开启。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| loki server | `.../pixiu-public/grafana/loki:3.6.11` | Loki 单二进制 Deployment |
| loki-canary | `.../pixiu-public/grafana/loki-canary:3.6.16` | 写入/读取探活 Canary DaemonSet |
| gateway | `.../pixiu-public/grafana/nginx-unprivileged:1.29-alpine` | nginx 网关（`gateway.enabled` 默认 true） |
| memcached | `.../pixiu-public/grafana/memcached:1.6.39-alpine` | chunks/results 内置缓存 |

可选组件：enterprise-logs、enterprise-provisioner（仅启用 Grafana Enterprise Logs、需 license）。如需最小化部署，可关闭 `gateway`、`lokiCanary`、`test`、`memcached`。完整镜像明细见镜像清单。

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

## 安装说明

应用商店安装实录（2026-10-29，pixiu-dev 单节点）：平台安装记录 `pixiu-system`，`deploy_status=success` / `deployed`。单节点小磁盘集群安装前先确认 Longhorn「可调度余量」足够（见常见问题）。

实测通过的安装 values（`deploymentMode`、`singleBinary`、`storage`、`schemaConfig` 已内化为 Chart 默认值；本例 PVC 5Gi 为实测值，Chart 默认 10Gi；`test` 与 `lokiCanary` 默认开启，安装时需显式关闭）：

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

验证结果：

- Pod：loki-0 / loki-gateway / loki-chunks-cache-0 / loki-results-cache-0 全部 Running 且 Ready。
- 经平台 K8s 服务代理查 `/loki/api/v1/labels`（带 `X-Scope-OrgID`）返回 app/container/namespace/pod 等标签；`query_range` 能查到 promtail 采集的真实容器日志（含 gateway 自身 access log，promtail push 204）。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 安装失败：`execution error at (loki/templates/validate.yaml): You must provide a schema_config` | 上游默认 values 不带 schema_config | 本仓库 Chart 已内置 `loki.schemaConfig`（tsdb + v13 + filesystem），使用仓库包即可；自备 values 时需补齐该校验项 |
| 查询 API 返回 401 no org id | loki 默认 `auth_enabled: true`，gateway 要求 `X-Scope-OrgID` | 客户端（如 promtail）需配 `tenant_id`，查询 API 同样要带 `X-Scope-OrgID: <租户>` |
| Longhorn 卷 faulted（insufficient storage），Pod 卡 `FailedAttachVolume ... rpc error: code = Aborted` | Longhorn 按卷声明大小做调度预检：磁盘 maximum 39.3GiB、storageReserved 30%（11.8GiB）→ 可调度上限 27.5GiB，已有卷（minio 10+10、loki 5、test 1）+ 新卷 5Gi 超限 | 调低节点磁盘保留（PATCH `longhorn.io/v1beta2 .../nodes/<node>` 的 `spec.disks.<id>.storageReserved`，本次改为 10%≈3.9GiB），Longhorn 自动恢复调度、重建副本；单节点小磁盘集群装大容量应用前先看「可调度余量」而非剩余磁盘，新应用 PVC 5Gi 起步 |

## 相关链接

- [镜像清单](../loki-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/grafana/loki
