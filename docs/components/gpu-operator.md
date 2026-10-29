# GPU Operator（gpu-operator）

> 分类：GPU 与加速　|　用途：自动化部署与生命周期管理 NVIDIA GPU 驱动、容器运行时、Device Plugin 与监控组件。

| 项 | 值 |
| --- | --- |
| Chart | [gpu-operator](https://github.com/NVIDIA/gpu-operator) |
| 仓库版本 | **v26.7.2**（`charts/gpu-operator-v26.7.2.tgz`） |
| appVersion | **v26.7.2** |
| 来源 | [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) / Helm：`https://helm.ngc.nvidia.com/nvidia` |
| 镜像清单 | [gpu-operator-images.md](../gpu-operator-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| v26.7.2 | v26.7.2 | `charts/gpu-operator-v26.7.2.tgz` | 默认 values：容器 GPU 路径，`sandboxWorkloads.enabled=false` |

## 镜像

所有镜像 repository 已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/nvidia/`）。

默认 values 下会拉取 Operator、校验、NFD、Driver、驱动管理、Container Toolkit、Device Plugin、DCGM Exporter、MIG Manager 等镜像；Driver 镜像实际 tag 常带 OS 后缀（如 `595.91.07-ubuntu22.04`），由节点操作系统决定。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| gpu-operator | `.../pixiu-public/nvidia/gpu-operator:v26.7.2` | Operator 控制器 |
| node-feature-discovery | `.../pixiu-public/nvidia/node-feature-discovery:v0.19.0` | NFD（`nfd.enabled=true`） |
| driver | `.../pixiu-public/nvidia/driver:595.91.07` | GPU 驱动容器（实际 tag 可能含 OS 后缀） |
| container-toolkit | `.../pixiu-public/nvidia/container-toolkit:v1.20.1` | NVIDIA Container Toolkit |
| k8s-device-plugin | `.../pixiu-public/nvidia/k8s-device-plugin:v0.20.1` | Device Plugin；GFD 默认共用此镜像 |
| dcgm-exporter | `.../pixiu-public/nvidia/dcgm-exporter:4.6.1-4.8.4-distroless` | GPU 指标导出 |

完整镜像明细（含沙箱 / DRA 等可选组件）见镜像清单。

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

## 安装说明

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| Driver 镜像拉取失败 | Driver 实际 tag 常带 OS 后缀（如 `595.91.07-ubuntu22.04`），由节点操作系统决定 | 按目标系统准备对应 tag 并推送到 mirror |
| 开启沙箱工作负载后组件镜像缺失 | 部分沙箱相关组件 `enabled` 默认为 true，但 `sandboxWorkloads.enabled=false` 时通常不会在普通 GPU 节点调度 | 开启沙箱工作负载前按镜像清单的可选组件表补齐镜像 |

## 相关链接

- [镜像清单](../gpu-operator-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/NVIDIA/gpu-operator
