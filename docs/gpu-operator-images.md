# GPU Operator 镜像列表

对应 Chart：`gpu-operator`

| 项 | 值 |
| --- | --- |
| Chart | [gpu-operator](https://github.com/NVIDIA/gpu-operator) |
| Chart 版本 | **v26.7.2**（仓库文件：`charts/gpu-operator-v26.7.2.tgz`） |
| appVersion | **v26.7.2** |
| 来源 | [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) / Helm：`https://helm.ngc.nvidia.com/nvidia` |
| Pixiu 默认调整 | 所有镜像 repository 已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values**（容器 GPU 路径、`sandboxWorkloads.enabled=false`）整理。开启沙箱 / DRA / 可选组件或覆盖 `repository`/`image`/`version` 后，实际拉取列表会变化。  
> Driver 镜像实际 tag 常带 OS 后缀（如 `595.91.07-ubuntu22.04`），由节点 OS 决定，离线需按目标系统准备对应 tag。

## 默认会拉取的镜像

| 组件 | 镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| gpu-operator | `nvcr.io/nvidia/gpu-operator:v26.7.2` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/gpu-operator:v26.7.2` | Operator 控制器（`version` 为空时用 Chart `appVersion`） |
| validator | `nvcr.io/nvidia/gpu-operator:v26.7.2` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/gpu-operator:v26.7.2` | 安装校验（与 Operator 同镜像） |
| node-feature-discovery | `registry.k8s.io/nfd/node-feature-discovery:v0.19.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/node-feature-discovery:v0.19.0` | NFD（`nfd.enabled=true`，子 chart appVersion `v0.19.0`） |
| driver | `nvcr.io/nvidia/driver:595.91.07` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/driver:595.91.07` | GPU 驱动容器（实际 tag 可能含 OS 后缀） |
| k8s-driver-manager | `nvcr.io/nvidia/cloud-native/k8s-driver-manager:v0.12.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/k8s-driver-manager:v0.12.1` | 驱动生命周期管理 sidecar |
| container-toolkit | `nvcr.io/nvidia/k8s/container-toolkit:v1.20.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/container-toolkit:v1.20.1` | NVIDIA Container Toolkit |
| k8s-device-plugin | `nvcr.io/nvidia/k8s-device-plugin:v0.20.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/k8s-device-plugin:v0.20.1` | Device Plugin；GFD 默认共用此镜像 |
| dcgm-exporter | `nvcr.io/nvidia/k8s/dcgm-exporter:4.6.1-4.8.4-distroless` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/dcgm-exporter:4.6.1-4.8.4-distroless` | GPU 指标导出 |
| k8s-mig-manager | `nvcr.io/nvidia/cloud-native/k8s-mig-manager:v0.15.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/k8s-mig-manager:v0.15.1` | MIG 管理 |

## 默认不启用 / 按场景才拉取（可选）

| 组件 | 默认镜像 | mirror 镜像 | 何时需要 |
| --- | --- | --- | --- |
| dcgm | `nvcr.io/nvidia/cloud-native/dcgm:4.6.1-1-ubuntu24.04` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/dcgm:4.6.1-1-ubuntu24.04` | `dcgm.enabled=true` |
| nodeStatusExporter | `nvcr.io/nvidia/gpu-operator:v26.7.2` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/gpu-operator:v26.7.2` | `nodeStatusExporter.enabled=true` |
| nvidia-fs (GDS) | `nvcr.io/nvidia/cloud-native/nvidia-fs:2.29.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/nvidia-fs:2.29.4` | `gds.enabled=true` |
| gdrdrv | `nvcr.io/nvidia/cloud-native/gdrdrv:v2.6` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/gdrdrv:v2.6` | `gdrcopy.enabled=true` |
| vgpu-manager | （需自备，默认 repository 为空） | — | `vgpuManager.enabled=true` |
| vgpu-device-manager | `nvcr.io/nvidia/cloud-native/vgpu-device-manager:v0.5.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/vgpu-device-manager:v0.5.1` | vGPU / 相关设备管理场景 |
| vfioManager (+ driver-manager) | `nvcr.io/nvidia/cloud-native/k8s-driver-manager:v0.12.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/k8s-driver-manager:v0.12.1` | 沙箱 / VFIO 场景（`sandboxWorkloads`） |
| kubevirt-gpu-device-plugin | `nvcr.io/nvidia/kubevirt-gpu-device-plugin:v1.6.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/kubevirt-gpu-device-plugin:v1.6.0` | `sandboxWorkloads` + KubeVirt 模式 |
| nvidia-sandbox-device-plugin | `nvcr.io/nvidia/cloud-native/nvidia-sandbox-device-plugin:v0.0.5` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/nvidia-sandbox-device-plugin:v0.0.5` | `sandboxWorkloads.mode=kata` |
| k8s-cc-manager | `nvcr.io/nvidia/cloud-native/k8s-cc-manager:v0.4.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/k8s-cc-manager:v0.4.4` | 机密计算相关 |
| dra-driver-nvidia-gpu | `nvcr.io/nvidia/dra-driver-nvidia-gpu:v0.5.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/dra-driver-nvidia-gpu:v0.5.1` | `gpuCluster.deployCR=true`（默认 false） |

> Chart 中部分沙箱相关组件 `enabled` 默认为 true，但 `sandboxWorkloads.enabled=false` 时通常不会在普通 GPU 节点调度；开启沙箱工作负载前请按上表补齐镜像。

## 原生镜像

上游原始镜像地址（含默认与常见可选组件），可直接批量 pull 后重新 tag / push 到私有仓库：

```text
nvcr.io/nvidia/gpu-operator:v26.7.2
registry.k8s.io/nfd/node-feature-discovery:v0.19.0
nvcr.io/nvidia/driver:595.91.07
nvcr.io/nvidia/cloud-native/k8s-driver-manager:v0.12.1
nvcr.io/nvidia/k8s/container-toolkit:v1.20.1
nvcr.io/nvidia/k8s-device-plugin:v0.20.1
nvcr.io/nvidia/k8s/dcgm-exporter:4.6.1-4.8.4-distroless
nvcr.io/nvidia/cloud-native/k8s-mig-manager:v0.15.1
nvcr.io/nvidia/cloud-native/dcgm:4.6.1-1-ubuntu24.04
nvcr.io/nvidia/cloud-native/nvidia-fs:2.29.4
nvcr.io/nvidia/cloud-native/gdrdrv:v2.6
nvcr.io/nvidia/cloud-native/vgpu-device-manager:v0.5.1
nvcr.io/nvidia/kubevirt-gpu-device-plugin:v1.6.0
nvcr.io/nvidia/cloud-native/nvidia-sandbox-device-plugin:v0.0.5
nvcr.io/nvidia/cloud-native/k8s-cc-manager:v0.4.4
nvcr.io/nvidia/dra-driver-nvidia-gpu:v0.5.1
```

## 离线 / 私有仓库建议

1. 至少拉取「默认会拉取的镜像」并推送到私有镜像仓库；Driver 请按节点 OS 准备带后缀的 tag。  
2. 安装时可通过 values 覆盖各组件的 `repository` / `image` / `version`。  
3. Chart 包内已把默认 `repository` 写成 SWR mirror，离线安装无需额外改仓库前缀；若使用其他私有仓，按表中 mirror 列整体替换。

## 参考

- 安装指南：<https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html>  
- 发布说明：<https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/release-notes.html>  
- Helm 仓库：`helm repo add nvidia https://helm.ngc.nvidia.com/nvidia`  
- OCI：`oci://nvcr.io/nvidia/cloud-native-charts/gpu-operator`  
