# MinIO 镜像列表

对应 Chart：`minio`（基于 MinIO 官方 Helm chart 5.4.0 模板的 Pixiu 打包修订版 5.4.1）

| 项 | 值 |
| --- | --- |
| Chart | [minio](https://github.com/minio/charts/tree/master/minio)（上游仓库已归档，链接当前 404） |
| Chart 版本 | **5.4.1**（仓库文件：`charts/minio-5.4.1.tgz`） |
| appVersion | **RELEASE.2024-12-18T13-15-44Z**（MinIO Server 版本） |
| 来源 | [charts.min.io](https://charts.min.io/)（官方 Helm 仓库，已停止更新） |
| Pixiu 默认调整 | 模板保持官方 5.4.0 原样；仅 `image` / `mcImage` 指向 SWR `-cpuv1` 变体 |

> **重要**：官方 MinIO 镜像的裸 tag（`quay.io/minio/minio:RELEASE.2024-12-18T13-15-44Z`、`quay.io/minio/mc:RELEASE.2024-11-21T17-21-54Z`）已不可得，SWR 上的同名裸 tag 也已不存在，现仅提供 `-cpuv1` 与 `.fips` 变体。本 Chart 包使用 `-cpuv1`（**amd64 单架构**）；`mc` 直接复用 server 镜像内嵌的精确版本二进制。MinIO CE 已停止更新，本包仅作过渡方案。

## 默认镜像

默认 values 中仅有 **2 个镜像引用**（`image` 与 `mcImage`），两者指向**同一个物理镜像**，因此实际只需拉取 **1 个镜像**：

| 组件 | 镜像引用（`image` 与 `mcImage` 相同） | 说明 |
| --- | --- | --- |
| minio server | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2024-12-18T13-15-44Z-cpuv1` | StatefulSet / Deployment（server） |
| mc（post-job） | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2024-12-18T13-15-44Z-cpuv1` | 创建默认 user / bucket / policy 的 post-install、post-upgrade Job；默认 `users` 非空，因此默认渲染 |

镜像 digest：

```text
swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2024-12-18T13-15-44Z-cpuv1
  @ sha256:5409ec27af66a48d2195ebc6dc32bbd04c76e4f29cd4114bec0ac595900faf23
```

### 为什么 mc 复用 server 镜像

- SWR 的 `pixiu-public/minio/mc` 仓库为空，无法单独拉取 mc 镜像；上游 `quay.io/minio/mc` 裸 tag 亦不可得。
- server 镜像内已包含精确版本的 mc：`/usr/bin/mc`，版本 `RELEASE.2024-11-21T17-21-54Z`（sha256 `0312010a9d0aa7a52b4dfb14330f289ee4e295def80b3a3f530d4f38c1b71da0`），与官方 chart 5.4.0 默认的 mc tag 一致。
- 镜像内 `/bin -> usr/bin`，`/bin/sh` 可用；官方 post-job 模板使用 shell 脚本（`_helper_create_*.txt`）调用 `mc`，因此 post-job 可正常运行。

### `-cpuv1` 与 `.fips` 变体

| 变体 | 说明 |
| --- | --- |
| `RELEASE.2024-12-18T13-15-44Z-cpuv1` | 本包使用；**amd64 单架构**（无 arm64） |
| `.fips` | FIPS 140 变体；本包未使用 |
| 裸 tag `RELEASE.2024-12-18T13-15-44Z` | 已从 SWR 与上游消失，不可用 |

## 升级已有 5.4.0 release 的注意事项

本 Chart 5.4.1 的 **模板与官方 5.4.0 完全一致**，仅镜像 values 与打包版本号变化。升级已有 5.4.0 release 时：

1. 应用商店升级弹窗会**预填旧 values**（旧 values 中的 `image.tag` / `mcImage.*` 仍是裸 tag 或旧仓库），必须手动改为：

   ```yaml
   image:
     repository: swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio
     tag: RELEASE.2024-12-18T13-15-44Z-cpuv1
   mcImage:
     repository: swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio
     tag: RELEASE.2024-12-18T13-15-44Z-cpuv1
   ```

2. 若不改，升级后仍会按旧 tag 拉取，导致 `ImagePullBackOff`。

## 可选：构建独立 mc 镜像

如后续需要独立 mc 镜像（例如脱离 server 镜像复用），可从 server 镜像提取 `/usr/bin/mc` 构建最小镜像。示例（可选，需自行验证静态链接与 CA 证书是否满足使用场景）：

```dockerfile
FROM swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2024-12-18T13-15-44Z-cpuv1 AS src

FROM debian:bookworm-slim
COPY --from=src /usr/bin/mc /usr/local/bin/mc
ENTRYPOINT ["mc"]
```

构建并推送后，将 `mcImage.repository` / `mcImage.tag` 指向新镜像即可。

## 风险提示

- **MinIO CE 自 2025-10-15 起仅源码分发**，官方仓库已于 **2026-04-25 归档**；Chart 5.4.0/5.4.1 与 `RELEASE.2024-12-18T13-15-44Z` 镜像均不再获得后续安全修复。
- 本包为**过渡方案**，建议评估替代对象存储（如 Ceph RGW、SeaweedFS、Garage 等）并规划迁移。
- `-cpuv1` 仅 amd64：arm64 集群无法使用本包默认镜像。

## 端口

| 端口 | 用途 |
| --- | --- |
| `9000` | S3 API |
| `9001` | 内置 Console（`RELEASE.2024-12-18T13-15-44Z` 仍带 Console） |

## 参考

- Chart 源码：<https://github.com/minio/charts/tree/master/minio>（已归档 / 404）
- MinIO 项目：<https://github.com/minio/minio>
- Helm 仓库：`helm repo add minio https://charts.min.io/`（已停止更新）
