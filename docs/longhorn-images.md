# Longhorn 镜像列表

对应 Chart：`longhorn`

| 项 | 值 |
| --- | --- |
| Chart | [longhorn](https://github.com/longhorn/longhorn) |
| Chart 版本 | **1.13.0**（仓库文件：`charts/longhorn-1.13.0.tgz`，K8s ≥1.34）<br>**1.12.1**（仓库文件：`charts/longhorn-1.12.1.tgz`，K8s ≥1.25，覆盖 1.28.x） |
| appVersion | **v1.13.0** / **v1.12.1** |
| 来源 | [charts.longhorn.io](https://charts.longhorn.io)（官方 Helm 仓库） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/longhorn/`），两个版本处理方式一致 |
| 节点前置条件 | [见下文「节点前置条件（安装前必读）」](#节点前置条件安装前必读) — 每个节点都必须先安装 open-iscsi 等依赖，否则 longhorn-manager 会直接 CrashLoopBackOff |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。Longhorn 的引擎类镜像（engine / instance-manager / share-manager / backing-image-manager）与 CSI sidecar 镜像通过 Longhorn Manager 的 Setting 下发，不在模板中直接渲染为容器镜像，离线环境**必须全部同步**。

## 节点前置条件（安装前必读）

Longhorn 不包含任何自动安装宿主机依赖的 hook：`longhorn-manager` 启动时会自检环境，缺依赖直接 fatal 退出，Pod 随即 CrashLoopBackOff。上游 chart 包内 README 的「安装前准备」对 **1.12.1 与 1.13.0 完全一致**，因此本节适用于本仓库 `longhorn-1.12.1`、`longhorn-1.13.0` 及后续 Longhorn V1 数据引擎版本，不是某个版本的特例。

集群**每个节点**（包括单节点集群的控制平面节点）都必须满足下列条件。

### 依赖清单

| 依赖 | RHEL·CentOS·AmazonLinux2 | Debian·Ubuntu | SUSE | 是否必需 | 用途 |
| --- | --- | --- | --- | --- | --- |
| open-iscsi | `iscsi-initiator-utils` | `open-iscsi` | `open-iscsi` | 必需 | `longhorn-manager` 启动自检、iSCSI 连接后端存储 |
| iscsid 服务 | `iscsid`（`iscsi-initiator-utils` 提供） | `iscsid`（`open-iscsi` 提供） | `iscsid`（`open-iscsi` 提供） | 必需 | 须 enabled 且 running |
| iscsi_tcp 内核模块 | 对应内核包 | `linux-modules-extra`（或内核自带） | 内核自带 | 必需 | 必须在 iscsid 启动前加载 |
| NFSv4 客户端 | `nfs-utils` | `nfs-common` | `nfs-client` | 仅 RWX 卷必需 | 提供 ReadWriteMany（共享）卷 |
| cryptsetup | `cryptsetup` | `cryptsetup` | `cryptsetup` | 加密卷必需 | LUKS2 加密卷 |
| dmsetup | `device-mapper` | `dmsetup` | `device-mapper` | 必需 | 设备映射，Longhorn 引擎与快照依赖 |
| 基础工具 | `bash curl findmnt grep awk blkid lsblk`（util-linux / findutils / gawk） | 同左 | 同左 | 必需 | chart README 明确列出的启动脚本依赖 |
| mount propagation | 容器运行时支持 shared 传播（Docker/containerd 默认开启） | 同左 | 同左 | 必需 | CSI 卷在节点上的挂载传播 |
| root 运行 | 允许容器以 root 运行（Longhorn 工作负载默认 root） | 同左 | 同左 | 必需 | Manager / CSI 需访问宿主 `/dev`、`/proc` 等 |

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

`/etc/modules-load.d/iscsi_tcp.conf` 用于保证重启后 iscsi_tcp 在 iscsid 启动前加载；若运行中 `iscsid` 已先启动过，执行 `modprobe iscsi_tcp` 后重启一次 `iscsid` 更稳妥。

### 验证方式

在每个节点执行，全部满足后再安装 / 重装 chart：

```bash
iscsiadm --version                 # 有输出即可，注意避开 2.1.12（见备注）
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

### 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `longhorn-manager` CrashLoopBackOff，`longhorn-driver-deployer` 卡在 `Init:0/1`，`longhorn-ui` 正常 Running | 节点缺少 iscsiadm。日志关键字：`Error starting manager: failed to check environment, please make sure you have iscsiadm/open-iscsi installed on the host` | 按上文安装 open-iscsi 并启动 iscsid，然后删除 manager Pod 重新自检 |
| 单节点集群卷一直「降级 / Degraded」 | `default-replica-count` 默认 3，单节点无法满足 | 在 Longhorn UI 的 Setting 中将 `default-replica-count` 改为 1 |
| CentOS 7 上 `yum install` 报 404 | CentOS 7 已 EOL，官方源与 mirror 下线 | 将 yum 源切到 `vault.centos.org` 或使用内网源后再安装 |

### 备注

- chart 不会自动安装上述依赖，Pixiu 应用商店界面只展示 `Chart.yaml` 的 description 单行，不展示本文档，因此安装前须人工确认节点条件。
- 可使用官方 `longhornctl check preflight` 自动检查、`longhornctl install preflight` 自动安装依赖（需自行下载对应平台的二进制）。
- open-iscsi **2.1.12** 存在已知问题，请使用 `<=2.1.11` 或 `>=2.1.13` 的版本。
- 上述要求针对 Longhorn **V1 数据引擎**（默认，chart 默认 `dataEngine: v1`）；若启用 V2 数据引擎（SPDK），还需内核 6.7+、2GiB 大页、`vfio_pci`/`nvme-tcp` 模块等，不在本文范围。
- 节点需允许容器以 root 运行，镜像需可从 SWR mirror 拉取（见下方镜像清单）。

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

## 1.12.1 版本镜像（K8s ≥1.25，适用 v1.28.15 等旧集群）

Chart 1.12.1 与 1.13.0 组件结构一致（13 个镜像），mirror 路径相同，仅 tag 不同。原生镜像 → mirror 镜像对应关系同上表，tag 对照：

| 组件 | 1.12.1 tag | 原生镜像 |
| --- | --- | --- |
| longhorn-manager / longhorn-driver | `v1.12.1` | `longhornio/longhorn-manager:v1.12.1` |
| longhorn-ui | `v1.12.1` | `longhornio/longhorn-ui:v1.12.1` |
| longhorn-engine | `v1.12.1` | `longhornio/longhorn-engine:v1.12.1` |
| longhorn-instance-manager | `v1.12.1` | `longhornio/longhorn-instance-manager:v1.12.1` |
| longhorn-share-manager | `v1.12.1` | `longhornio/longhorn-share-manager:v1.12.1` |
| backing-image-manager | `v1.12.1` | `longhornio/backing-image-manager:v1.12.1` |
| support-bundle-kit | `v0.0.92` | `longhornio/support-bundle-kit:v0.0.92` |
| csi-attacher | `v4.12.0` | `longhornio/csi-attacher:v4.12.0` |
| csi-provisioner | `v5.3.0` | `longhornio/csi-provisioner:v5.3.0` |
| csi-node-driver-registrar | `v2.17.0` | `longhornio/csi-node-driver-registrar:v2.17.0` |
| csi-resizer | `v2.2.1` | `longhornio/csi-resizer:v2.2.1` |
| csi-snapshotter | `v8.6.0` | `longhornio/csi-snapshotter:v8.6.0` |
| livenessprobe | `v2.19.0` | `longhornio/livenessprobe:v2.19.0` |

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

## 备注

- Chart 1.13.0 为 Longhorn 官方仓库当前最新稳定版，**要求 Kubernetes ≥1.34**（`kubeVersion: ">=1.34.0-0"`），无法安装在 1.28 集群。
- **Chart 1.12.1 要求 Kubernetes ≥1.25**（`kubeVersion: ">=1.25.0-0"`），是支持 K8s v1.28.15 的最新版本，老集群请选此版本。
- Longhorn 不支持从高版本降级到低版本；两个版本可共存于应用商店，按集群 K8s 版本选择安装。
- Longhorn 是分布式块存储（RWO/RWX 块设备），可作为集群默认 StorageClass 提供有状态应用存储。
- Chart 中 `privateRegistry`（`registryUrl/User/Passwd`）用于镜像仓库认证 Secret，使用 SWR 匿名 mirror 时无需配置。

## 参考

- Chart 源码：<https://github.com/longhorn/longhorn>
- Longhorn 文档：<https://longhorn.io/docs/>
- Helm 仓库：`helm repo add longhorn https://charts.longhorn.io`
