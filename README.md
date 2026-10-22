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

镜像清单: [docs/prometheus-images.md](docs/prometheus-images.md)

上游来源: [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts/)

## Velero

| 项 | 值 |
| --- | --- |
| Chart | [velero](https://github.com/vmware-tanzu/helm-charts/tree/main/charts/velero) |
| Chart 版本 | **12.2.1**（仓库文件：`charts/velero-12.2.1.tgz`） |
| appVersion | **1.18.2**（Velero 版本） |
| 来源 | [vmware-tanzu/helm-charts](https://github.com/vmware-tanzu/helm-charts) |

镜像清单: [docs/velero-images.md](docs/velero-images.md)

上游来源: [vmware-tanzu/helm-charts](https://github.com/vmware-tanzu/helm-charts)

## GPU Operator

| 项 | 值 |
| --- | --- |
| Chart | [gpu-operator](https://github.com/NVIDIA/gpu-operator) |
| Chart 版本 | **v26.7.2**（仓库文件：`charts/gpu-operator-v26.7.2.tgz`） |
| appVersion | **v26.7.2** |
| 来源 | [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) |

镜像清单: [docs/gpu-operator-images.md](docs/gpu-operator-images.md)

上游来源: [helm.ngc.nvidia.com/nvidia](https://helm.ngc.nvidia.com/nvidia) / OCI `oci://nvcr.io/nvidia/cloud-native-charts/gpu-operator`
