# MinIO（minio）

> 分类：存储与备份　|　用途：S3 兼容的对象存储服务。

| 项 | 值 |
| --- | --- |
| Chart | [minio](https://github.com/minio/charts/tree/master/minio)（上游仓库已归档，链接当前 404） |
| 仓库版本 | **5.4.0**（`charts/minio-5.4.0.tgz`） |
| appVersion | **RELEASE.2025-09-07T16-13-09Z** |
| 来源 | [charts.min.io](https://charts.min.io/)（官方 Helm 仓库，已停止更新）；上游 GitHub 仓库已归档、链接 404，本包为基于官方 Helm chart 5.4.0 模板的 Pixiu 打包修订版 |
| 镜像清单 | [minio-images.md](../minio-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 5.4.0 | RELEASE.2025-09-07T16-13-09Z | `charts/minio-5.4.0.tgz` | 基于官方 Helm chart 5.4.0 模板的 Pixiu 修订包（新增 `templates/validate.yaml` 安装前校验） |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/`），plain tag 无 `-cpuv1` 后缀。默认 values 中仅有 `image` 与 `mcImage` 两个引用且指向同一物理镜像，因此实际只需拉取 1 个镜像；post-job 通过复用 server 镜像内自带的 `/usr/bin/mc` 完成初始化。镜像仅 `linux/amd64` 单架构，基于 UBI9，要求 CPU 支持 x86-64-v2。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| minio server | `.../pixiu-public/minio/minio:RELEASE.2025-09-07T16-13-09Z` | StatefulSet / Deployment（server） |
| mc（post-job） | `.../pixiu-public/minio/minio:RELEASE.2025-09-07T16-13-09Z` | 创建默认 user / bucket / policy 的 post-install、post-upgrade Job |

完整镜像明细（含 digest 与变体说明）见镜像清单。

## 原生镜像

上游镜像仓库为 `quay.io/minio/minio`，可直接 pull 后重新 tag / push 到私有仓库：

```text
quay.io/minio/minio:RELEASE.2025-09-07T16-13-09Z
```

> 上游 chart 的 `mcImage` 默认为 `quay.io/minio/mc`；Pixiu 修订包将 `mcImage` 与 `image` 统一指向上述 server 镜像（server 镜像内置 `mc`），因此实际只需拉取 1 个镜像。

## 安装说明

### 默认规格（Pixiu 调整）

模板与官方 Helm chart 5.4.0 一致（仅新增 `templates/validate.yaml` 安装前校验），Pixiu 默认 values 调整如下：

| 项 | Pixiu 默认 | 上游默认 |
| --- | --- | --- |
| `mode` | `distributed` | `distributed` |
| `replicas` | **2** | 16 |
| `pools` | 1 | 1 |
| `drivesPerNode` | 1 | 1 |
| `resources.requests.memory` | **2Gi** | 16Gi |
| `persistence.size` | **50Gi** | 500Gi |
| `persistence.storageClass` | `longhorn` | `""`（集群默认） |

合计：2 个 Pod、4Gi 内存 request、100Gi raw 存储（2 × 50Gi）；2 盘采用 EC:1，可用容量约 50Gi，允许坏 1 盘；如需 EC:2（允许坏 2 盘）在安装页把 `replicas` 调到 4。

说明：

- 上游默认面向生产大集群（16 Pod、256Gi 内存 request、约 8TiB raw 存储），应用商店默认值按可落地的较小规格收敛。
- `2Gi` 仅为 request、不设 limit，实际用量可超过该值；用户可在安装页按需调大。
- `replicas` 至少 2；建议取 4 的倍数（4/8…）以保持 EC 集与驱动器布局规整。
- 默认绑定 `longhorn` StorageClass：目标集群必须已安装 Longhorn 且存在名为 `longhorn` 的 StorageClass；若没有，PVC 会 Pending，请在安装页改回集群默认 SC 或实际 SC 名称。
- 安装前校验：`mode=distributed` 时若 `pools × replicas × drivesPerNode < 2` 直接渲染失败；`mode` 仅允许 `distributed` / `standalone`。

### 端口

| 端口 | 用途 |
| --- | --- |
| `9000` | S3 API |
| `9001` | Console 端点；新社区版仅保留精简对象浏览器（管理操作需使用 `mc`） |

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 安装失败：`failed post-install: job minio-post-job failed: BackoffLimitExceeded`；Pod 反复重启 | 在 `mode: distributed` 下把 `replicas` 改成 1（或小于 2）。distributed 模式只生成单个 URL 端点，MinIO 单盘部署要求 path 端点，启动报 `use path style endpoint for single node setup` 后退出，post-install Job 连不上服务 | 保持 distributed 时 `replicas` 至少为 2（默认 2，EC:1）；只需单实例时把 `mode` 改为 `standalone` 并设置 `persistence.size`。排查时先看 StatefulSet Pod 日志，再决定调整 `mode` 还是 `replicas` |
| 安装直接报 `MinIO distributed 模式至少需要 2 个磁盘/端点...` | Pixiu 修订包在安装前拦截了上述非法配置 | 按提示将 `replicas` 调整为至少 2（或 4），或把 `mode` 改为 `standalone`；已导入旧包的平台需更新默认配置或删除后重新导入 |
| 镜像启动失败 | plain tag 基于 UBI9，要求 CPU 支持 x86-64-v2 | 在不支持该指令集的老机器上改用 `-cpuv1` 变体 |

其他风险：本包使用的 2025-09-07 镜像受 CVE-2025-62506 影响（High，Service Account / STS 会话策略绕过导致权限提升），官方仅发布源码安全修复版 `RELEASE.2025-10-15T17-29-55Z`，无对应容器镜像；2025-09-07 是社区版最后一个官方容器发布版，本包为过渡方案，详见镜像清单「风险提示」。

## 相关链接

- [镜像清单](../minio-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://charts.min.io/
