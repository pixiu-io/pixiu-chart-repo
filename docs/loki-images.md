# Loki 镜像列表

对应 Chart：`loki`

| 项 | 值 |
| --- | --- |
| Chart | [loki](https://github.com/grafana/loki/tree/main/production/helm/loki) |
| Chart 版本 | **7.5.0**（仓库文件：`charts/loki-7.5.0.tgz`） |
| appVersion | **3.6.16**（Chart 内默认 Loki Server 镜像 tag 为 3.6.11） |
| 来源 | [grafana/helm-charts](https://github.com/grafana/helm-charts)（官方 Helm 仓库） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理（`deploymentMode: SingleBinary`，内置 memcached 缓存默认开启）。Loki 7.x 默认部署需要配置存储后端（对象存储或 filesystem）后才能正常安装。

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
- Loki 7.x 单二进制模式（SingleBinary）默认带 1 个 canary、gateway 与内置 memcached；如需最小化部署，可关闭 `gateway`、`lokiCanary`、`test`、`memcached`。
- Promtail 通过独立的 `promtail` chart（同仓库 `charts/promtail-6.17.1.tgz`）部署，作为 Loki 的日志采集端。

## 参考

- Chart 源码：<https://github.com/grafana/loki/tree/main/production/helm/loki>
- Loki 项目：<https://github.com/grafana/loki>
- Helm 仓库：`helm repo add grafana https://grafana.github.io/helm-charts`
