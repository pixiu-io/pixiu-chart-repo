# Pixiu 应用商店仓库

本仓库存放 Pixiu 应用商店使用的 Chart 包。

文档索引: [docs/README.md](docs/README.md)（应用商店 Chart 添加说明）

# 组件列表
## Prometheus Operator

| 项 | 值 |
| --- | --- |
| Chart | [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) |
| Chart 版本 | **92.11.0**（仓库文件：`charts/kube-prometheus-stack-92.11.0.tgz`） |
| appVersion | **v0.94.1**（Prometheus Operator 版本） |
| 来源 | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts/) |
| 镜像清单 | [docs/prometheus-images.md](docs/prometheus-images.md) |

## Velero

| 项 | 值 |
| --- | --- |
| Chart | [velero](https://github.com/vmware-tanzu/helm-charts/tree/main/charts/velero) |
| Chart 版本 | **12.2.1**（仓库文件：`charts/velero-12.2.1.tgz`，Pixiu 同版本重打修订包） |
| appVersion | **1.18.2**（Velero 版本） |
| 来源 | [vmware-tanzu/helm-charts](https://github.com/vmware-tanzu/helm-charts) |
| 镜像清单 | [docs/velero-images.md](docs/velero-images.md) |

## GPU Operator

| 项 | 值 |
| --- | --- |
| Chart | [gpu-operator](https://github.com/NVIDIA/gpu-operator) |
| Chart 版本 | **v26.7.2**（仓库文件：`charts/gpu-operator-v26.7.2.tgz`） |
| appVersion | **v26.7.2** |
| 来源 | [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) |
| 镜像清单 | [docs/gpu-operator-images.md](docs/gpu-operator-images.md) |

## Ingress NGINX

| 项 | 值 |
| --- | --- |
| Chart | [ingress-nginx](https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx) |
| Chart 版本 | **4.15.1**（仓库文件：`charts/ingress-nginx-4.15.1.tgz`） |
| appVersion | **1.15.1** |
| 来源 | [kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx) |
| 镜像清单 | [docs/ingress-nginx-images.md](docs/ingress-nginx-images.md) |

## MinIO

| 项 | 值 |
| --- | --- |
| Chart | [minio](https://github.com/minio/charts/tree/master/minio)（上游仓库已归档，链接当前 404） |
| Chart 版本 | **5.4.0**（仓库文件：`charts/minio-5.4.0.tgz`） |
| appVersion | **RELEASE.2025-09-07T16-13-09Z** |
| 来源 | [charts.min.io](https://charts.min.io/)（官方 Helm 仓库，已停止更新） |
| 镜像清单 | [docs/minio-images.md](docs/minio-images.md) |

## Loki

| 项 | 值 |
| --- | --- |
| Chart | [loki](https://github.com/grafana/loki/tree/main/production/helm/loki) |
| Chart 版本 | **7.5.0**（仓库文件：`charts/loki-7.5.0.tgz`） |
| appVersion | **3.6.16**（默认镜像 tag 3.6.11） |
| 来源 | [grafana/helm-charts](https://github.com/grafana/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/loki-images.md](docs/loki-images.md) |

## Promtail

| 项 | 值 |
| --- | --- |
| Chart | [promtail](https://github.com/grafana/helm-charts/tree/main/charts/promtail) |
| Chart 版本 | **6.17.1**（仓库文件：`charts/promtail-6.17.1.tgz`） |
| appVersion | **3.5.1** |
| 来源 | [grafana/helm-charts](https://github.com/grafana/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/promtail-images.md](docs/promtail-images.md) |

## Cert-manager

| 项 | 值 |
| --- | --- |
| Chart | [cert-manager](https://github.com/cert-manager/cert-manager/tree/master/deploy/charts/cert-manager) |
| Chart 版本 | **v1.21.3**（仓库文件：`charts/cert-manager-v1.21.3.tgz`） |
| appVersion | **v1.21.3** |
| 来源 | [jetstack](https://charts.jetstack.io) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/cert-manager-images.md](docs/cert-manager-images.md) |

## Longhorn

| 项 | 值 |
| --- | --- |
| Chart | [longhorn](https://github.com/longhorn/longhorn) |
| Chart 版本 | **1.13.0**（仓库文件：`charts/longhorn-1.13.0.tgz`，K8s ≥1.34）；**1.12.1**（仓库文件：`charts/longhorn-1.12.1.tgz`，K8s ≥1.25，适用 1.28.x） |
| appVersion | **v1.13.0** / **v1.12.1** |
| 来源 | [charts.longhorn.io](https://charts.longhorn.io) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/longhorn-images.md](docs/longhorn-images.md) |

## Elasticsearch

| 项 | 值 |
| --- | --- |
| Chart | [elasticsearch](https://github.com/elastic/helm-charts/tree/main/elasticsearch) |
| Chart 版本 | **8.5.1**（仓库文件：`charts/elasticsearch-8.5.1.tgz`） |
| appVersion | **8.5.1**（Elasticsearch 版本） |
| 来源 | [helm.elastic.co](https://helm.elastic.co) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/elasticsearch-images.md](docs/elasticsearch-images.md) |

## Harbor

| 项 | 值 |
| --- | --- |
| Chart | [harbor](https://github.com/goharbor/harbor-helm) |
| Chart 版本 | **1.19.4**（仓库文件：`charts/harbor-1.19.4.tgz`） |
| appVersion | **2.15.4**（Harbor 版本） |
| 来源 | [helm.goharbor.io](https://helm.goharbor.io) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/harbor-images.md](docs/harbor-images.md) |

## Redis Operator

| 项 | 值 |
| --- | --- |
| Chart | [redis-operator](https://github.com/OT-CONTAINER-KIT/redis-operator) |
| Chart 版本 | **0.27.0**（仓库文件：`charts/redis-operator-0.27.0.tgz`） |
| appVersion | **0.27.0**（Redis Operator 版本） |
| 来源 | [ot-container-kit.github.io/helm-charts](https://ot-container-kit.github.io/helm-charts/) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/redis-operator-images.md](docs/redis-operator-images.md) |

## MySQL Operator

| 项 | 值 |
| --- | --- |
| Chart | [mysql-operator](https://github.com/mysql/mysql-operator) |
| Chart 版本 | **2.3.1**（仓库文件：`charts/mysql-operator-2.3.1.tgz`） |
| appVersion | **26.10.0-2.3.1**（MySQL 26.10.0 / Operator 2.3.1） |
| 来源 | [mysql.github.io/mysql-operator](https://mysql.github.io/mysql-operator/) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [docs/mysql-operator-images.md](docs/mysql-operator-images.md) |
