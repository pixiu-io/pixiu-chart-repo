# Longhorn 镜像列表

对应 Chart：`longhorn`

| 项 | 值 |
| --- | --- |
| Chart | [longhorn](https://github.com/longhorn/longhorn) |
| Chart 版本 | **1.13.0**（仓库文件：`charts/longhorn-1.13.0.tgz`） |
| appVersion | **v1.13.0** |
| 来源 | [charts.longhorn.io](https://charts.longhorn.io)（官方 Helm 仓库） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。Longhorn 的引擎类镜像（engine / instance-manager / share-manager / backing-image-manager）与 CSI sidecar 镜像通过 Longhorn Manager 的 Setting 下发，不在模板中直接渲染为容器镜像，离线环境**必须全部同步**。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| longhorn-manager | `longhornio/longhorn-manager:v1.13.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/longhorn-manager:v1.13.0` | 核心 Manager DaemonSet |
| longhorn-ui | `longhornio/longhorn-ui:v1.13.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/longhorn-ui:v1.13.0` | Web 控制台 |
| longhorn-driver | `longhornio/longhorn-manager:v1.13.0` | 同 manager | Driver Deployer（复用 manager 镜像） |
| longhorn-engine | `longhornio/longhorn-engine:v1.13.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/longhorn-engine:v1.13.0` | 数据面引擎（经 Setting 下发） |
| longhorn-instance-manager | `longhornio/longhorn-instance-manager:v1.13.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/longhorn-instance-manager:v1.13.0` | 实例管理器（经 Setting 下发） |
| longhorn-share-manager | `longhornio/longhorn-share-manager:v1.13.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/longhorn-share-manager:v1.13.0` | RWX 共享卷管理（经 Setting 下发） |
| backing-image-manager | `longhornio/backing-image-manager:v1.13.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/backing-image-manager:v1.13.0` | 备份镜像管理（经 Setting 下发） |
| support-bundle-kit | `longhornio/support-bundle-kit:v0.0.98` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/support-bundle-kit:v0.0.98` | 支持包采集（按需触发） |
| csi-attacher | `longhornio/csi-attacher:v4.13.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/csi-attacher:v4.13.0` | CSI 附加控制器 |
| csi-provisioner | `longhornio/csi-provisioner:v6.3.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/csi-provisioner:v6.3.0` | CSI 供给控制器 |
| csi-node-driver-registrar | `longhornio/csi-node-driver-registrar:v2.18.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/csi-node-driver-registrar:v2.18.0` | 节点 CSI 注册 |
| csi-resizer | `longhornio/csi-resizer:v2.2.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/csi-resizer:v2.2.1` | 卷扩容 |
| csi-snapshotter | `longhornio/csi-snapshotter:v8.6.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/csi-snapshotter:v8.6.0` | 快照控制器 |
| livenessprobe | `longhornio/livenessprobe:v2.20.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/livenessprobe:v2.20.0` | CSI 存活探针 |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| oauth-proxy | `quay.io/openshift/origin-oauth-proxy:<版本>` | 仅 OpenShift 集群（`image.openshift.oauthProxy`，默认空，需自行指定） |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
longhornio/longhorn-manager:v1.13.0
longhornio/longhorn-ui:v1.13.0
longhornio/longhorn-engine:v1.13.0
longhornio/longhorn-instance-manager:v1.13.0
longhornio/longhorn-share-manager:v1.13.0
longhornio/backing-image-manager:v1.13.0
longhornio/support-bundle-kit:v0.0.98
longhornio/csi-attacher:v4.13.0
longhornio/csi-provisioner:v6.3.0
longhornio/csi-node-driver-registrar:v2.18.0
longhornio/csi-resizer:v2.2.1
longhornio/csi-snapshotter:v8.6.0
longhornio/livenessprobe:v2.20.0
```

## 离线 / 私有仓库建议

1. 将上面的原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/`（保持 tag 不变）；
2. Chart 包内默认 values 已通过 `global.imageRegistry`（SWR 域名）+ `image.*.repository`（`pixiu-public/longhorn/<name>`）指向 SWR mirror，离线环境开箱即用；
3. 若使用其他私有仓库，可整体替换 `global.imageRegistry` 并同步修改 13 处 `image.*.repository`；引擎类与 CSI 镜像由 Manager Setting 下发，改 values 即可全局生效，无需改 Setting。

## 备注

- Chart 1.13.0 为 Longhorn 官方仓库当前最新稳定版。
- **Kubernetes 版本要求 >= 1.34**（`kubeVersion: ">=1.34.0-0"`），部署前确认集群版本。
- Longhorn 是分布式块存储（RWO/RWX 块设备），可作为集群默认 StorageClass 提供有状态应用存储。
- Chart 中 `privateRegistry`（`registryUrl/User/Passwd`）用于镜像仓库认证 Secret，使用 SWR 匿名 mirror 时无需配置。

## 参考

- Chart 源码：<https://github.com/longhorn/longhorn>
- Longhorn 文档：<https://longhorn.io/docs/>
- Helm 仓库：`helm repo add longhorn https://charts.longhorn.io`
