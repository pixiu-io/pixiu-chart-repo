# Pixiu 应用商店仓库

本仓库存放 Pixiu 应用商店使用的 Helm Chart 包。

## Prometheus

推荐使用 **Prometheus Operator** 方式部署，对应 Chart：`kube-prometheus-stack`。

| Chart | 版本 | 说明 |
| --- | --- | --- |
| `kube-prometheus-stack` | 92.11.0（另保留 65.1.1） | Operator 栈，生产推荐 |
| `prometheus` | 25.10.0 | 经典非 Operator 部署 |

上游来源：[prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts/)

**镜像清单（离线/私有仓必备）** → [docs/prometheus-images.md](docs/prometheus-images.md)
