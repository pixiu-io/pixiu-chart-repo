# csi-driver-nfs（csi-driver-nfs）

> 分类：存储与备份　|　用途：NFS CSI 驱动，把外部 NFS 服务器接入集群，提供 StorageClass 动态供给与静态挂载。

| 项 | 值 |
| --- | --- |
| Chart | [csi-driver-nfs](https://github.com/kubernetes-csi/csi-driver-nfs) |
| 仓库版本 | **4.13.6**（`charts/csi-driver-nfs-4.13.6.tgz`） |
| appVersion | **4.13.6** |
| 来源 | [Kubernetes SIG Storage 官方 Helm 仓库](https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts)（最新稳定版，项目活跃维护中） |
| 镜像清单 | [csi-driver-nfs-images.md](../csi-driver-nfs-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 4.13.6 | 4.13.6 | `charts/csi-driver-nfs-4.13.6.tgz` | 官方最新稳定版；K8s 1.20+ 可用，v1.28.15 集群直接安装 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/csi-driver-nfs/`，保留上游 `sig-storage` 命名空间）。默认渲染 6 个镜像：nfsplugin（驱动本体）、csi-provisioner、csi-resizer、csi-snapshotter、livenessprobe、csi-node-driver-registrar；开启 `feature.enableSnapshot=true` 后额外渲染 snapshot-controller。

values 替换点：

- `image.baseRepo` → SWR mirror（sidecar 经模板 `baseRepo + /sig-storage/...` 拼接指向 mirror）
- `image.nfs.repository` → SWR mirror 全路径（nfsplugin 本体）

## 部署前置条件

1. 集群节点能访问 NFS 服务器（TCP 2049，挂载走 NFSv3/NFSv4）；
2. **默认不创建 StorageClass**（`storageClass.create: false`）：动态供给需开启 `storageClass.create` 并填写 `name` / `parameters.server` / `parameters.share`；静态挂载则直接创建 PV 引用已有 export；
3. 如需 VolumeSnapshot 能力，开启 `feature.enableSnapshot=true`（会额外拉取 snapshot-controller 镜像）。

## 验证方式

- `kubectl get pods -n kube-system | grep csi-nfs`：Controller Deployment 与 Node DaemonSet 均为 Running；
- 动态供给场景：`kubectl get sc` 确认自建 StorageClass 已创建，测试 PVC/Pod 读写并在 NFS 服务器上看到子目录；
- 静态挂载场景：创建测试 PV/PVC 并挂载 Pod 读写文件。

## 常见问题

- PVC 一直 Pending：多为 NFS 服务器地址/share 配置错误或网络不通（2049 端口），查 `csi-nfs-controller` 日志；
- 节点 Pod 报 mount 失败：确认 NFS 导出项允许该节点 IP 访问（`/etc/exports` 与防火墙）；
- RWX 多 Pod 共享读写是 NFS 天然能力；不支持 NFS 原生配额，容量限制需在 NFS 服务器侧控制。

## 备注

- 与 Longhorn 定位不同：Longhorn 用本地磁盘构建分布式存储；csi-driver-nfs 仅把客户现成 NAS/NFS 存储接入 K8s，两者可并存；
- 项目由 Kubernetes SIG Storage 维护，为官方生态中 NFS CSI 的唯一实现，长期维护有保障。
