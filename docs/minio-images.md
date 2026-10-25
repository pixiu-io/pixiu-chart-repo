# MinIO 镜像列表

对应 Chart：`minio`

| 项 | 值 |
| --- | --- |
| Chart | [minio](https://github.com/bitnami/charts/tree/main/bitnami/minio) |
| Chart 版本 | **17.0.21**（仓库文件：`charts/minio-17.0.21.tgz`） |
| appVersion | **2025.7.23**（MinIO Server 版本） |
| 来源 | [Bitnami charts](https://github.com/bitnami/charts)（上游已于 2026-09-08 弃用并删除该 chart，本仓库为归档包） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/`），并设置 `global.security.allowInsecureImages: true` |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理（`mode=standalone`、`console.enabled=true`、`provisioning.enabled=false`、`defaultInitContainers.volumePermissions.enabled=false`）。默认安装只拉取 **2 个**镜像；开启可选配置后最多再引入 **2 个**。
>
> 该 Chart 默认 tag 的上游可拉取地址为 `docker.io/bitnamilegacy/*`（Bitnami 已将旧 tag 迁入 legacy 仓库）。`Chart.yaml` 的 `annotations.images` 仍写 `docker.io/bitnami/*`，属上游元数据，实际拉取以 values 为准。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| minio server | `docker.io/bitnamilegacy/minio:2025.7.23-debian-12-r3` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/minio:2025.7.23-debian-12-r3` | MinIO Server（`image.*`），standalone 模式 |
| minio console | `docker.io/bitnamilegacy/minio-object-browser:2.0.2-debian-12-r3` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/minio-object-browser:2.0.2-debian-12-r3` | Web Console（`console.image.*`），默认开启，HTTP 端口 **9090** |

## 默认不启用（可选）

| 组件 | 原生镜像 | mirror 镜像 | 何时需要 |
| --- | --- | --- | --- |
| minio client | `docker.io/bitnamilegacy/minio-client:2025.7.21-debian-12-r2` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/minio-client:2025.7.21-debian-12-r2` | Chart **不会**部署该镜像；仅 NOTES.txt 中手工运行 `mc` 调试 Pod 时使用（`clientImage.*`） |
| os-shell | `docker.io/bitnamilegacy/os-shell:12-debian-12-r50` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/os-shell:12-debian-12-r50` | `defaultInitContainers.volumePermissions.enabled=true` 的卷权限 init 容器；或 `provisioning.enabled=true` 时 provisioning Job 的 `wait-for-available-minio` init 容器（provisioning 主容器仍使用 minio server 镜像，`mc` 已内置） |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/bitnamilegacy/minio:2025.7.23-debian-12-r3
docker.io/bitnamilegacy/minio-client:2025.7.21-debian-12-r2
docker.io/bitnamilegacy/minio-object-browser:2.0.2-debian-12-r3
docker.io/bitnamilegacy/os-shell:12-debian-12-r50
```

## 离线 / 私有仓库建议

1. 至少将「默认会拉取的镜像」同步到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/`（保持 tag 不变）；需要 provisioning / 卷权限 init 容器时再补 `os-shell`，需要手工 `mc` 调试时再补 `minio-client`。
2. Chart 包内默认 values 已通过 `global.imageRegistry`（SWR 域名）+ 各 `image.*.registry` / `repository` 指向 SWR mirror，离线安装无需额外改仓库前缀。
3. 若使用其他私有仓库，需同时修改 `global.imageRegistry` 与 4 处 `*.image.registry`、`*.image.repository`（repository 已去掉 `bitnami/` 前缀），并保留 `global.security.allowInsecureImages: true`，否则渲染会被 Bitnami 公共库拦截。
4. `digest` 保持为空，按 tag 拉取；若需强一致性，可自行填入同步后镜像的 sha256 digest。

## `global.security.allowInsecureImages` 说明

Bitnami 公共库会校验 Chart 内所有镜像是否仍是其上游登记的标准镜像；只要 registry / repository 被替换（本仓库指向 SWR mirror），校验即失败并中止渲染。本 Chart 因此显式设置：

```yaml
global:
  security:
    allowInsecureImages: true
```

- **必要性**：设为 `false` 时，`helm template` / `helm install` 直接失败，报错列出 4 个 SWR 镜像并提示 `Unrecognized images`。
- **安全含义**：该开关关闭了 Bitnami 的镜像来源校验，镜像可信度完全依赖 SWR mirror 的同步治理。请只同步来自 `bitnamilegacy` 的原始镜像，避免向该路径推入无关/未审核镜像。

## 备注

- **上游已弃用**：Bitnami 于 2026-09-08 弃用并删除 `minio` chart，本仓库的 17.0.21 为归档版本，不再有上游修复。
- **镜像停更风险**：`bitnamilegacy` 仅为旧镜像归档，不再接收安全更新；后续 MinIO 或基础镜像（Debian 12）出现 CVE 时无法通过升级 tag 修复，存在明确的安全停更风险，建议规划迁移至仍在维护的 MinIO Chart / 镜像源。
- **端口**：S3 API `9000`；Console `9090`（注意与 MinIO 官方 Console 默认 `9001` 不同）。
- 默认 `mode=standalone`；`provisioning.enabled=false`，默认不会创建 bucket / user / policy。
- Chart 已从上游仓库删除，`Chart.yaml` 中的 `home` / `sources` 链接可能失效，保留仅为溯源。

## 参考

- Chart 源码（上游已删除）：<https://github.com/bitnami/charts/tree/main/bitnami/minio>
- Bitnami legacy 镜像：<https://hub.docker.com/u/bitnamilegacy>
- Bitnami 镜像校验说明：<https://github.com/bitnami/charts/issues/30850>
- MinIO 项目：<https://github.com/minio/minio>
