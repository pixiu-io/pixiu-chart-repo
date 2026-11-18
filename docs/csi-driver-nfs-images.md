# csi-driver-nfs 镜像列表

对应 Chart：`csi-driver-nfs`

| 项 | 值 |
| --- | --- |
| Chart | [csi-driver-nfs](https://github.com/kubernetes-csi/csi-driver-nfs) |
| Chart 版本 | **4.13.6**（仓库文件：`charts/csi-driver-nfs-4.13.6.tgz`） |
| appVersion | **4.13.6**（NFS CSI Driver 版本） |
| 来源 | [raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts](https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts)（Kubernetes SIG Storage 官方 Helm 仓库最新稳定版） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/`，保留上游 `sig-storage` 命名空间） |

> 本 chart 部署 **NFS CSI Driver**（Controller Deployment + Node DaemonSet），把外部 NFS 服务器接入集群并提供 `StorageClass` 动态供给。集群只需能访问 NFS 服务器（2049 端口）；驱动容器内置 nfs-utils，节点无需额外安装 NFS 客户端。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| nfsplugin | `registry.k8s.io/sig-storage/nfsplugin:v4.13.6` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/nfsplugin:v4.13.6` | NFS CSI 驱动本体（Controller + Node） |
| csi-provisioner | `registry.k8s.io/sig-storage/csi-provisioner:v6.3.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/csi-provisioner:v6.3.0` | PVC 动态供给 sidecar（Controller） |
| csi-resizer | `registry.k8s.io/sig-storage/csi-resizer:v2.2.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/csi-resizer:v2.2.1` | PVC 扩容 sidecar（Controller） |
| csi-snapshotter | `registry.k8s.io/sig-storage/csi-snapshotter:v8.6.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/csi-snapshotter:v8.6.0` | 快照 sidecar（Controller） |
| livenessprobe | `registry.k8s.io/sig-storage/livenessprobe:v2.19.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/livenessprobe:v2.19.0` | 健康探测 sidecar（Controller + Node） |
| csi-node-driver-registrar | `registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.17.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/csi-node-driver-registrar:v2.17.0` | 节点注册 sidecar（Node） |

## 开启快照后才会拉取（`feature.enableSnapshot=true`）

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| snapshot-controller | `registry.k8s.io/sig-storage/snapshot-controller:v8.6.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/snapshot-controller:v8.6.0` | VolumeSnapshot 控制器（默认关闭） |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
registry.k8s.io/sig-storage/nfsplugin:v4.13.6
registry.k8s.io/sig-storage/csi-provisioner:v6.3.0
registry.k8s.io/sig-storage/csi-resizer:v2.2.1
registry.k8s.io/sig-storage/csi-snapshotter:v8.6.0
registry.k8s.io/sig-storage/livenessprobe:v2.19.0
registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.17.0
registry.k8s.io/sig-storage/snapshot-controller:v8.6.0
```

## 离线 / 私有仓库建议

1. 将上面 7 个原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/sig-storage/`（保留 `sig-storage` 命名空间与原 tag）；
2. Chart 包内 values 已做两处替换：
   - `image.baseRepo` → SWR mirror（sidecar 镜像经模板 `baseRepo + /sig-storage/...` 拼接后指向 mirror）；
   - `image.nfs.repository` → SWR mirror 全路径（nfsplugin 本体镜像）；
3. values 中无其他上游镜像地址残留，`helm template` 渲染验证全部指向 SWR。

## 备注

- Chart 4.13.6 为 csi-driver-nfs 官方仓库当前最新稳定版（2026-10-23 发布），项目由 Kubernetes SIG Storage 活跃维护，未归档；
- 对 Kubernetes 版本要求低（官方标注 1.20+），v1.28.15 集群可直接安装；
- NFS 支持动态供给（每 PVC 一个子目录）与静态挂载（直接引用已有 export），不支持 NFS 配额与 RWX 之外的拓扑约束；
- **默认不创建 StorageClass**（`storageClass.create: false`），动态供给需按实际 NFS 环境开启并填写 `storageClass.name` / `parameters.server` / `parameters.share`（values 中有注释示例）；静态挂载则直接建 PV 引用已有 export。
