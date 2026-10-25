# MinIO 镜像列表

对应 Chart：`minio`

| 项 | 值 |
| --- | --- |
| Chart | [minio](https://github.com/bitnami/charts/tree/main/bitnami/minio) |
| Chart 版本 | **17.0.21**（仓库文件：`charts/minio-17.0.21.tgz`） |
| appVersion | **2025.7.23**（MinIO Server 版本） |
| 来源 | [Bitnami charts](https://github.com/bitnami/charts)（上游已于 2026-09-08 弃用并删除该 chart，本仓库为归档包） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/`），并设置 `global.security.allowInsecureImages: true` |

> **弃用警示（重要）**：Bitnami minio chart 已于 2026-09-08 被上游弃用删除；`bitnamilegacy` 镜像最后更新于 2025-08-19，不再提供安全更新。本次替换仅解决镜像可获得性，属**过渡方案**，需评估后续迁移至其他 S3 兼容存储或自建镜像。

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

各镜像对应的源 manifest digest 与架构（多架构 manifest list，amd64 / arm64 均可用）：

| 镜像 | 源 digest | 架构 |
| --- | --- | --- |
| `docker.io/bitnamilegacy/minio:2025.7.23-debian-12-r3` | `sha256:953d489a81cc4de7975f90e07202189c4325da39b0b92470b6a13c7ea99e36cd` | amd64 / arm64 |
| `docker.io/bitnamilegacy/minio-object-browser:2.0.2-debian-12-r3` | `sha256:4ca163354c4f4e2cf87a0c6cf668f47d07f7f176b53d9bd4bd16b81df62b2763` | amd64 / arm64 |
| `docker.io/bitnamilegacy/minio-client:2025.7.21-debian-12-r2` | `sha256:7a6b4b93998903f1673d2bd2140ac26b807c4224627b743778c5a8f70db561f1` | amd64 / arm64 |
| `docker.io/bitnamilegacy/os-shell:12-debian-12-r50` | `sha256:e328cff6e45072a3e90a7659a16f3cf5fa801909b1151e6554c319059c092155` | amd64 / arm64 |

> digest 为**源镜像**（bitnamilegacy）的校验值，用于确认同步来源；镜像搬运到 SWR 后 manifest digest 会变化，**以 SWR manifest 为准**。Chart values 中的 `digest` 字段保持为空，按 tag 拉取，避免搬运后 digest 不匹配导致拉取失败。

## 离线 / 私有仓库建议

1. 至少将「默认会拉取的镜像」同步到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/bitnami/`（保持 tag 不变）；需要 provisioning / 卷权限 init 容器时再补 `os-shell`，需要手工 `mc` 调试时再补 `minio-client`。
2. Chart 包内默认 values 已通过 `global.imageRegistry`（SWR 域名）+ 各 `image.*.registry` / `repository` 指向 SWR mirror，离线安装无需额外改仓库前缀。
3. 若使用其他私有仓库，需同时修改 `global.imageRegistry` 与 4 处 `*.image.registry`、`*.image.repository`（repository 已去掉 `bitnami/` 前缀），并保留 `global.security.allowInsecureImages: true`，否则渲染会被 Bitnami 公共库拦截。
4. Chart values 中的 `digest` 保持为空，按 tag 拉取；如合规要求固定 digest，必须使用 **SWR manifest** 的 digest，切勿填入源镜像（bitnamilegacy）digest，否则搬运后 manifest 变化会导致拉取失败。

## 兼容性与迁移注意

本仓库此前使用 MinIO 官方 `minio` chart 5.4.0（appVersion `RELEASE.2024-12-18T13-15-44Z`，默认 `mode=distributed`、`replicas=16`）。Bitnami 17.0.21 是**另一套实现**（默认 `mode=standalone`、`console.enabled=true`），**不能原地 `helm upgrade`**，必须按全新安装 + 数据迁移处理。

- **不可原地升级**：两套 Chart 的 StatefulSet / Deployment `selector`、`serviceName`（旧 `<fullname>-svc` → 新 `<fullname>-headless`）、分布式模式 `volumeClaimTemplates` 名称均不同，而这些字段在 Kubernetes 中不可变；直接 `helm upgrade` 会失败或产生资源冲突。请卸载旧 release 后全新安装。

- **旧 values 键会被静默忽略**：Helm 不会对未知键报错，沿用旧 values 时配置会“看似生效、实际丢失”。常见对应关系：

  | 官方 5.4.0 | Bitnami 17.0.21 | 说明 |
  | --- | --- | --- |
  | `rootUser` / `rootPassword` | `auth.rootUser` / `auth.rootPassword` | 默认凭证 |
  | `mcImage` | `clientImage` | mc 客户端镜像（仅 NOTES 手工 Pod 使用） |
  | `replicas` | `statefulset.replicaCount` | 仅 distributed 模式有效，需为偶数且 `>= 4` |
  | `consoleService` | `console.service` | Console Service 配置 |
  | `mountPath` | `persistence.mountPath` | 新默认 `/bitnami/minio/data`，不要照抄旧值 `/export` |
  | `image.repository`（完整镜像地址） | `image.repository`（仅仓库名） | 新 Chart 由 `image.registry` + `repository` 拼接，语义不同 |

- **旧 values 快照会覆盖新默认值**：跨 Chart 升级时若使用 `--reuse-values` 或直接复用 5.4.0 的 values 文件，旧 `image.repository`（完整地址，如 `swr.../pixiu-public/minio/minio`）会与新 Chart 默认 `image.registry`（`swr.../pixiu-public/bitnami`）拼接，得到重复前缀的非法镜像地址。请以本 Chart 默认 values 为基线重新生成 values，不要复用旧 values。

- **默认部署模式不同**：5.4.0 默认 `distributed`（16 副本），17.0.21 默认 `standalone`。若原部署依赖分布式纠删码，需显式设置 `mode=distributed` 与 `statefulset.replicaCount`（偶数且 `>= 4`）。

- **数据路径变化**：容器内数据目录由 `/export` 改为 `/bitnami/minio/data`；distributed 模式的 `volumeClaimTemplates` 名称由 `export` 改为 `data`（多盘为 `data-<n>`）。依赖旧路径的 hostPath、备份脚本、sidecar 需同步调整。

- **Secret 键名变化**：默认 root 凭证 Secret 的 key 由 `rootUser` / `rootPassword` 改为 `root-user` / `root-password`，引用该 Secret 的外部应用 / Job 需同步修改。

- **Console 端口变化**：旧 Chart Console 与 Server 同进程，端口 `9001`（`consoleService.port`）；新 Chart Console 是独立的 object-browser Deployment（`console.enabled=true` 默认开启），端口 **`9090`**。Ingress、Service、防火墙和用户访问地址需同步调整；S3 API 端口仍为 `9000`。

- **PVC 保留注意**：standalone 模式的 PVC 是 Chart 管理的普通资源，`helm uninstall` 会一并删除（不同于 StatefulSet `volumeClaimTemplates` 生成的 PVC）。卸载前请先备份数据，并给旧 PVC 添加 `helm.sh/resource-policy: keep` 注解、确认 StorageClass `reclaimPolicy=Retain`；新旧 standalone PVC 都基于 release fullname 命名，同 namespace 同名 release 重装会冲突，建议使用新 release 名称 / namespace 或显式 `persistence.existingClaim`。

- **建议迁移步骤**：
  1. 备份对象数据（`mc mirror` 或直接备份 PVC），并导出 bucket / user / policy 配置；
  2. 为旧 PVC 加保留注解并确认回收策略，卸载旧 release；
  3. 用新的 Bitnami values 全新安装 17.0.21（建议先在新 namespace / 新 PVC 验证）；
  4. 将对象数据恢复到新数据路径 `/bitnami/minio/data`；
  5. 重建 bucket / user / policy（也可开启 `provisioning.enabled` 声明式创建）；
  6. 校验应用 endpoint / 凭证 / Console `9090` 后再切换流量，最后清理旧 PVC。

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
