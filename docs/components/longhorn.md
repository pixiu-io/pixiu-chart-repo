# Longhorn（longhorn）

> 分类：存储与备份　|　用途：分布式块存储，为集群提供 RWO/RWX 卷与默认 StorageClass。

| 项 | 值 |
| --- | --- |
| Chart | [longhorn](https://github.com/longhorn/longhorn) |
| 仓库版本 | **1.13.0**（`charts/longhorn-1.13.0.tgz`）<br>**1.12.1**（`charts/longhorn-1.12.1.tgz`） |
| appVersion | **v1.13.0** / **v1.12.1** |
| 来源 | [charts.longhorn.io](https://charts.longhorn.io) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [longhorn-images.md](../longhorn-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 1.13.0 | v1.13.0 | `charts/longhorn-1.13.0.tgz` | 官方最新稳定版，要求 Kubernetes ≥1.34（`kubeVersion: ">=1.34.0-0"`），无法安装到 1.28 集群 |
| 1.12.1 | v1.12.1 | `charts/longhorn-1.12.1.tgz` | 要求 Kubernetes ≥1.25（`kubeVersion: ">=1.25.0-0"`），是支持 K8s v1.28.15 等旧集群的最新版本 |

Longhorn 不支持从高版本降级到低版本；两个版本可共存于应用商店，按集群 K8s 版本选择安装。

## 镜像

所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/`），1.12.1 与 1.13.0 处理方式一致、仅 tag 不同。默认 values 下共 13 个镜像引用：longhorn-manager、longhorn-ui、longhorn-engine、longhorn-instance-manager、longhorn-share-manager、backing-image-manager、support-bundle-kit 以及 5 个 CSI sidecar 与 livenessprobe。其中引擎类镜像（engine / instance-manager / share-manager / backing-image-manager）与 CSI sidecar 镜像通过 Longhorn Manager 的 Setting 下发，不在模板中直接渲染为容器镜像，离线环境**必须全部同步**。可选组件 oauth-proxy 仅 OpenShift 集群需要，默认不启用。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| longhorn-manager | `.../pixiu-public/longhorn/longhorn-manager:v1.13.0` | 核心 Manager DaemonSet；driver deployer 复用该镜像 |
| longhorn-ui | `.../pixiu-public/longhorn/longhorn-ui:v1.13.0` | Web 控制台 |
| longhorn-engine | `.../pixiu-public/longhorn/longhorn-engine:v1.13.0` | 数据面引擎（经 Setting 下发） |
| csi-attacher / csi-provisioner | `.../pixiu-public/longhorn/csi-attacher:v4.13.0` / `csi-provisioner:v6.3.0` | CSI 附加与供给控制器 |
| support-bundle-kit | `.../pixiu-public/longhorn/support-bundle-kit:v0.0.98` | 支持包采集（按需触发） |

完整镜像明细（含 1.12.1 tag 对照）见镜像清单。

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

### 1.12.1 版本

1.12.1 版本原生镜像（与 1.13.0 仅 tag 不同，推送到同一 mirror 路径即可）：

```text
longhornio/longhorn-manager:v1.12.1
longhornio/longhorn-ui:v1.12.1
longhornio/longhorn-engine:v1.12.1
longhornio/longhorn-instance-manager:v1.12.1
longhornio/longhorn-share-manager:v1.12.1
longhornio/backing-image-manager:v1.12.1
longhornio/support-bundle-kit:v0.0.92
longhornio/csi-attacher:v4.12.0
longhornio/csi-provisioner:v5.3.0
longhornio/csi-node-driver-registrar:v2.17.0
longhornio/csi-resizer:v2.2.1
longhornio/csi-snapshotter:v8.6.0
longhornio/livenessprobe:v2.19.0
```

## 安装说明

### 节点前置条件（安装前必读）

Longhorn 不包含任何自动安装宿主机依赖的 hook：`longhorn-manager` 启动时会自检环境，缺依赖直接 fatal 退出，Pod 随即 CrashLoopBackOff。上游 chart 包内 README 的「安装前准备」对 1.12.1 与 1.13.0 完全一致，适用于两个版本。

集群**每个节点**（包括单节点集群的控制平面节点）都必须满足：

| 依赖 | RHEL·CentOS·AmazonLinux2 | Debian·Ubuntu | SUSE | 是否必需 | 用途 |
| --- | --- | --- | --- | --- | --- |
| open-iscsi | `iscsi-initiator-utils` | `open-iscsi` | `open-iscsi` | 必需 | Manager 启动自检、iSCSI 连接后端存储 |
| iscsid 服务 | `iscsid` | `iscsid` | `iscsid` | 必需 | 须 enabled 且 running |
| iscsi_tcp 内核模块 | 对应内核包 | `linux-modules-extra`（或内核自带） | 内核自带 | 必需 | 必须在 iscsid 启动前加载 |
| NFSv4 客户端 | `nfs-utils` | `nfs-common` | `nfs-client` | 仅 RWX 卷必需 | 提供 ReadWriteMany 共享卷 |
| cryptsetup | `cryptsetup` | `cryptsetup` | `cryptsetup` | 加密卷必需 | LUKS2 加密卷 |
| dmsetup | `device-mapper` | `dmsetup` | `device-mapper` | 必需 | 设备映射，引擎与快照依赖 |
| 基础工具 | `bash curl findmnt grep awk blkid lsblk` | 同左 | 同左 | 必需 | chart 启动脚本依赖 |
| mount propagation | 容器运行时支持 shared 传播 | 同左 | 同左 | 必需 | CSI 卷节点挂载传播 |
| root 运行 | 允许容器以 root 运行 | 同左 | 同左 | 必需 | Manager / CSI 需访问宿主 `/dev`、`/proc` |

### 安装命令

RHEL / CentOS / Amazon Linux 2：

```bash
yum install -y iscsi-initiator-utils nfs-utils cryptsetup device-mapper
systemctl enable --now iscsid
echo iscsi_tcp > /etc/modules-load.d/iscsi_tcp.conf
modprobe iscsi_tcp
```

Debian / Ubuntu：

```bash
apt-get update
apt-get install -y open-iscsi nfs-common cryptsetup dmsetup
systemctl enable --now iscsid
echo iscsi_tcp > /etc/modules-load.d/iscsi_tcp.conf
modprobe iscsi_tcp
```

SUSE：

```bash
zypper install -y open-iscsi nfs-client cryptsetup device-mapper
systemctl enable --now iscsid
echo iscsi_tcp > /etc/modules-load.d/iscsi_tcp.conf
modprobe iscsi_tcp
```

`/etc/modules-load.d/iscsi_tcp.conf` 用于保证重启后 iscsi_tcp 在 iscsid 启动前加载；若运行中 `iscsid` 已先启动过，执行 `modprobe iscsi_tcp` 后重启一次 `iscsid` 更稳妥。open-iscsi **2.1.12** 存在已知问题，请使用 `<=2.1.11` 或 `>=2.1.13` 的版本。

### 验证方式

在每个节点执行，全部满足后再安装 / 重装 chart：

```bash
iscsiadm --version                 # 有输出即可，注意避开 2.1.12
systemctl is-active iscsid         # 期望 active
lsmod | grep iscsi_tcp             # 期望有 iscsi_tcp
dmsetup version                    # 有输出即可
mount.nfs -V                       # RWX 卷需要，有输出即可
which bash curl findmnt grep awk blkid lsblk
```

在 Pixiu 应用商店安装完成后，若此前已因缺依赖导致 `longhorn-manager` CrashLoopBackOff：

1. 确认节点依赖已装好；
2. 删除 `longhorn-manager` Pod 触发重新自检（或重装 chart）；
3. `longhorn-manager` 变为 Ready 后，`longhorn-driver-deployer` 会自动继续部署 CSI 插件与 StorageClass，无需人工干预。

备注：

- chart 不会自动安装上述依赖，Pixiu 应用商店界面只展示 `Chart.yaml` 的 description 单行，安装前须人工确认节点条件。
- 可使用官方 `longhornctl check preflight` / `longhornctl install preflight` 自动检查与安装依赖（需自行下载对应平台二进制）。
- 上述要求针对 Longhorn **V1 数据引擎**（chart 默认 `dataEngine: v1`）；V2 数据引擎（SPDK）还需内核 6.7+、2GiB 大页、`vfio_pci`/`nvme-tcp` 模块等，不在本页范围。
- Chart 中 `privateRegistry`（`registryUrl/User/Passwd`）用于镜像仓库认证 Secret，使用 SWR 匿名 mirror 时无需配置。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| `longhorn-manager` CrashLoopBackOff，`longhorn-driver-deployer` 卡在 `Init:0/1`，`longhorn-ui` 正常 Running | 节点缺少 iscsiadm，日志关键字：`Error starting manager: failed to check environment, please make sure you have iscsiadm/open-iscsi installed on the host` | 按上文安装 open-iscsi 并启动 iscsid，然后删除 manager Pod 重新自检 |
| 单节点集群卷一直「降级 / Degraded」 | `default-replica-count` 默认 3，单节点无法满足 | 在 Longhorn UI 的 Setting 中将 `default-replica-count` 改为 1 |
| CentOS 7 上 `yum install` 报 404 | CentOS 7 已 EOL，官方源与 mirror 下线 | 将 yum 源切到 `vault.centos.org` 或使用内网源后再安装 |

## 相关链接

- [镜像清单](../longhorn-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/longhorn/longhorn
