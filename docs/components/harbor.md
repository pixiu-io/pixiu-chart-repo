# Harbor（harbor）

> 分类：镜像仓库　|　用途：企业级容器镜像仓库，提供镜像存储、权限、复制与漏洞扫描。

| 项 | 值 |
| --- | --- |
| Chart | [harbor](https://github.com/goharbor/harbor-helm) |
| 仓库版本 | **1.19.4**（`charts/harbor-1.19.4.tgz`） |
| appVersion | **2.15.4** |
| 来源 | [helm.goharbor.io](https://helm.goharbor.io) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [harbor-images.md](../harbor-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 1.19.4 | 2.15.4 | `charts/harbor-1.19.4.tgz` | 官方最新稳定版；Harbor 2.15 起移除 Notary 与 Chartmuseum，缓存层由 Redis 改为 Valkey |

## 镜像

所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/`，保留上游 goharbor 命名空间）。默认 values 下会拉取 8 个镜像：core、jobservice、registry、registryctl、portal、trivy、database、cache；PostgreSQL 使用 `harbor-db` 内置镜像、Redis 使用 `valkey-photon` 内置镜像，不使用外部子 chart。可选组件 nginx 反代（非 ingress 暴露时渲染）与 exporter（`metrics.enabled=true` 时渲染）默认不启用。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| core / jobservice | `.../pixiu-public/goharbor/harbor-core:v2.15.4` / `harbor-jobservice:v2.15.4` | 核心 API 与异步任务（复制、回收、扫描调度） |
| registry / registryctl | `.../pixiu-public/goharbor/registry-photon:v2.15.4` / `harbor-registryctl:v2.15.4` | 镜像存储与 Registry 管理 API |
| portal | `.../pixiu-public/goharbor/harbor-portal:v2.15.4` | Web 控制台（nginx 静态站点） |
| trivy | `.../pixiu-public/goharbor/trivy-adapter-photon:v2.15.4` | 漏洞扫描（Trivy adapter） |
| database / cache | `.../pixiu-public/goharbor/harbor-db:v2.15.4` / `valkey-photon:v2.15.4` | 内置 PostgreSQL 与 Valkey（StatefulSet） |

完整镜像明细（含可选镜像）见镜像清单。

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/goharbor/harbor-core:v2.15.4
docker.io/goharbor/harbor-jobservice:v2.15.4
docker.io/goharbor/registry-photon:v2.15.4
docker.io/goharbor/harbor-registryctl:v2.15.4
docker.io/goharbor/harbor-portal:v2.15.4
docker.io/goharbor/trivy-adapter-photon:v2.15.4
docker.io/goharbor/harbor-db:v2.15.4
docker.io/goharbor/valkey-photon:v2.15.4
docker.io/goharbor/nginx-photon:v2.15.4
docker.io/goharbor/harbor-exporter:v2.15.4
```

## 安装说明

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

安装前需知（源文档已有事实）：

- 默认 `expose.type=ingress`，需集群已安装 ingress controller（Ingress NGINX 已在应用商店提供）；`externalURL` 需改为实际访问地址。
- 默认使用内置 PostgreSQL / Valkey（StatefulSet + PVC）；生产建议 `database.type=external` / `redis.type=external` 接管外部实例，以简化备份扩容。
- Harbor 高可用至少需要：core / jobservice / portal 多副本 + 外部 PG / Redis + 共享存储（PVC 或外部对象存储）。
- Trivy 漏洞库（`trivy.db` / `trivy-java.db`）默认在 jobservice 首次扫描时从 GitHub 下载；离线环境需配置 `trivy.offlineScan` 并预置 DB（可挂载 PV 或用 `TRIVY_DB_REPOSITORY` 指向内部镜像源）。
- 离线时需将 10 个原生镜像（含两个可选镜像）同步到 SWR mirror，保持 tag 不变。

## 常见问题

暂无已记录的常见问题。

## 相关链接

- [镜像清单](../harbor-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/goharbor/harbor-helm
