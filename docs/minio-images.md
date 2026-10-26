# MinIO 镜像列表

对应 Chart：`minio`（基于官方 Helm chart 5.4.0 模板的 Pixiu 打包修订版 5.4.0）

| 项 | 值 |
| --- | --- |
| Chart | [minio](https://github.com/minio/charts/tree/master/minio)（上游仓库已归档，链接当前 404） |
| Chart 版本 | **5.4.0**（仓库文件：`charts/minio-5.4.0.tgz`） |
| appVersion | **RELEASE.2025-09-07T16-13-09Z**（MinIO Server 版本） |
| 来源 | [charts.min.io](https://charts.min.io/)（官方 Helm 仓库，已停止更新） |
| Pixiu 默认调整 | 模板保持官方 5.4.0 原样，仅 values 调整：`image` / `mcImage` 指向 SWR plain tag（无 `-cpuv1` 后缀），默认规格见下文「默认规格（Pixiu 调整）」 |

## 默认镜像

默认 values 中仅有 **2 个镜像引用**（`image` 与 `mcImage`），两者指向**同一个物理镜像**，因此实际只需拉取 **1 个镜像**：

| 组件 | 镜像引用（`image` 与 `mcImage` 相同） | 说明 |
| --- | --- | --- |
| minio server | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2025-09-07T16-13-09Z` | StatefulSet / Deployment（server） |
| mc（post-job） | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2025-09-07T16-13-09Z` | 创建默认 user / bucket / policy 的 post-install、post-upgrade Job；默认 `users` 非空，因此默认渲染 |

镜像 digest（manifest）：

```text
swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2025-09-07T16-13-09Z
  @ sha256:a1a8bd4ac40ad7881a245bab97323e18f971e4d4cba2c2007ec1bedd21cbaba2
```

镜像 manifest 总大小 62,242,297 B（约 59.4 MiB），仅 `linux/amd64`。

### 为什么 mc 复用 server 镜像

- SWR 的 `pixiu-public/minio/mc` 仓库为空，无法单独拉取 mc 镜像。
- server 镜像内已包含可用的 mc：`/usr/bin/mc`，版本 `RELEASE.2025-08-13T08-35-41Z`（30,535,864 B，sha256 `01f866e9c5f9b87c2b09116fa5d7c06695b106242d829a8bb32990c00312e891`）。
- 镜像内 `/bin -> usr/bin`，`usr/bin/sh -> bash`（即 `/bin/sh` 可用）；官方 post-job 模板使用 shell 脚本（`_helper_create_*.txt`）调用 `mc`，因此 post-job 可正常运行。
- 镜像 entrypoint 为 `/usr/bin/docker-entrypoint.sh`，默认 cmd 为 `["minio"]`；post-job 通过覆盖 command 执行脚本，不受影响。

### 变体说明

| 变体 | 说明 |
| --- | --- |
| `RELEASE.2025-09-07T16-13-09Z` | 本包使用；linux/amd64 单架构；UBI9 基础，要求 x86-64-v2 |
| `RELEASE.2025-09-07T16-13-09Z-cpuv1` | 备选；UBI8 基础，兼容 x86-64-v1 老 CPU（digest `sha256:e08497cde44985e0c36cacd391c9723831293d789d569cc967685f2fe17a7463`） |
| `.fips` | 历史版本曾提供 FIPS 140 变体；2025-09-07 版本 SWR 未镜像（无 `.fips` tag），本包不使用 |
| 旧裸 tag `RELEASE.2024-12-18T13-15-44Z` | 已从 SWR 与上游消失，不可用 |

## 默认规格（Pixiu 调整）

模板与官方 Helm chart 5.4.0 完全一致，以下仅为 values 默认值调整（Pixiu 默认规格差异）：

| 项 | Pixiu 默认 | 上游默认 |
| --- | --- | --- |
| `mode` | `distributed` | `distributed` |
| `replicas` | **4** | 16 |
| `pools` | 1 | 1 |
| `drivesPerNode` | 1 | 1 |
| `resources.requests.memory` | **2Gi** | 16Gi |
| `persistence.size` | **50Gi** | 500Gi |
| `persistence.storageClass` | `longhorn` | `""`（集群默认） |

合计：**4 个 Pod、8Gi 内存 request、200Gi raw 存储**（4 × 50Gi）。4 盘采用 EC:2，可用容量约 **100Gi**，允许坏 **2 盘**。

调整原因与说明：

- 上游默认面向生产大集群（16 Pod、256Gi 内存 request、约 8TiB raw 存储），应用商店默认值按可落地的较小规格收敛。
- `2Gi` 仅为 request、**不设 limit**，实际用量可超过该值；用户可在安装页按需调大。
- `replicas` 建议取 **4 的倍数**，以保持 EC 集与驱动器布局规整。
- 默认绑定 `longhorn` StorageClass：目标集群必须已安装 Longhorn 且存在名为 `longhorn` 的 StorageClass；若没有，PVC 会 Pending，请在安装页改回集群默认 SC 或实际 SC 名称。

## 可选：构建独立 mc 镜像

如后续需要独立 mc 镜像（例如脱离 server 镜像复用），可从 server 镜像提取 `/usr/bin/mc` 构建最小镜像。示例（可选，需自行验证静态链接与 CA 证书是否满足使用场景）：

```dockerfile
FROM swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2025-09-07T16-13-09Z AS src

FROM debian:bookworm-slim
COPY --from=src /usr/bin/mc /usr/local/bin/mc
ENTRYPOINT ["mc"]
```

构建并推送后，将 `mcImage.repository` / `mcImage.tag` 指向新镜像即可。

## 风险提示

- **镜像存在已知高危漏洞 CVE-2025-62506**：上游 2025-10-15 发布仅源码的安全修复版 `RELEASE.2025-10-15T17-29-55Z`（CVSS 8.1，High，Service Account / STS 会话策略绕过导致权限提升）。本包使用的 2025-09-07 镜像在受影响范围内。
- 官方未提供该修复版的容器镜像，SWR 也无对应 tag。如需修复，按上游指引自行构建并推送：

  ```bash
  git clone https://github.com/minio/minio
  git checkout RELEASE.2025-10-15T17-29-55Z
  GOOS=linux GOARCH=amd64 \
    TAG=<your-registry>/minio/minio:RELEASE.2025-10-15T17-29-55Z make docker
  ```

  请在 Linux amd64 构建机执行；构建需能拉取上游 Dockerfile 依赖的基础镜像。

  推送后将 chart 的 `image.tag` / `mcImage.tag` 指向自建镜像（需重新打包或在安装/升级时覆盖 values）。

- **2025-09-07 是 MinIO 社区版最后一个官方容器发布版**；此后官方未再发布容器镜像，上游 GitHub 仓库已归档。
- 本包为**过渡方案**，建议评估替代对象存储（如 Ceph RGW、SeaweedFS、Garage 等）并规划替代方案。
- plain tag 基于 UBI9，要求 CPU 支持 **x86-64-v2**：在不支持该指令集的老机器上 server 会无法启动，需改用 `-cpuv1` 变体。
- 本包默认镜像**仅 amd64**：arm64 集群无法使用。

## 端口

| 端口 | 用途 |
| --- | --- |
| `9000` | S3 API |
| `9001` | Console 端点；新社区版仅保留精简对象浏览器（管理操作需使用 `mc`） |

## 参考

- Chart 源码：<https://github.com/minio/charts/tree/master/minio>（已归档 / 404）
- MinIO 项目：<https://github.com/minio/minio>
- Helm 仓库：`helm repo add minio https://charts.min.io/`（已停止更新）
