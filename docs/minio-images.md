# MinIO 镜像列表

对应 Chart：`minio`

| 项 | 值 |
| --- | --- |
| Chart | [minio](https://github.com/minio/charts/tree/master/minio) |
| Chart 版本 | **5.4.0**（仓库文件：`charts/minio-5.4.0.tgz`） |
| appVersion | **RELEASE.2024-12-18T13-15-44Z**（MinIO Server 版本） |
| 来源 | [charts.min.io](https://charts.min.io/)（官方 Helm 仓库） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。开启可选配置（如 standalone 分布式模式、Console Ingress 等）不会引入额外镜像。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| minio server | `quay.io/minio/minio:RELEASE.2024-12-18T13-15-44Z` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/minio:RELEASE.2024-12-18T13-15-44Z` | MinIO Server Deployment / Statefulset |
| mc（bucket 初始化 Job） | `quay.io/minio/mc:RELEASE.2024-11-21T17-21-54Z` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/mc:RELEASE.2024-11-21T17-21-54Z` | 创建默认 bucket / user / policy 的 Job（`buckets`、`users`、`policies` 或 `svcacct` 配置非空时） |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| 无额外镜像 | — | Console、Ingress、PDB、NetworkPolicy 等均为 Server 同镜像，不引入新镜像 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/minio/minio:RELEASE.2024-12-18T13-15-44Z
quay.io/minio/mc:RELEASE.2024-11-21T17-21-54Z
```

## 离线 / 私有仓库建议

1. 将上面两个原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/minio/`（保持 tag 不变）；
2. Chart 包内默认 values 已指向 SWR mirror，离线环境开箱即用；
3. 若使用其他私有仓库，按 `image.repository` / `mcImage.repository` 整体替换前缀。

## 备注

- Chart 5.4.0 是 MinIO 官方 Helm 仓库当前最新稳定版（发布于 2025-01-02），上游社区 chart 此后未再发布新版本。
- MinIO 服务端口：`9000`（S3 API）/ `9001`（Console，`consoleService` 控制）。

## 参考

- Chart 源码：<https://github.com/minio/charts/tree/master/minio>
- MinIO 项目：<https://github.com/minio/minio>
- Helm 仓库：`helm repo add minio https://charts.min.io/`
