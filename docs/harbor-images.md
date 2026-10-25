# Harbor 镜像列表

对应 Chart：`harbor`

| 项 | 值 |
| --- | --- |
| Chart | [harbor](https://github.com/goharbor/harbor-helm) |
| Chart 版本 | **1.19.4**（仓库文件：`charts/harbor-1.19.4.tgz`） |
| appVersion | **2.15.4**（Harbor 版本） |
| 来源 | [helm.goharbor.io](https://helm.goharbor.io) 官方 Helm 仓库最新稳定版 |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/`，保留上游 goharbor 命名空间） |

> 下列镜像按本仓库 Chart 包内 **默认 values**（默认依赖已内置：PostgreSQL 使用 `harbor-db` 内置镜像、Redis 使用 `valkey-photon` 内置镜像，不使用外部子 chart）整理。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| core | `docker.io/goharbor/harbor-core:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/harbor-core:v2.15.4` | Harbor 核心 API 服务 |
| jobservice | `docker.io/goharbor/harbor-jobservice:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/harbor-jobservice:v2.15.4` | 异步任务（复制、回收、扫描调度） |
| registry | `docker.io/goharbor/registry-photon:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/registry-photon:v2.15.4` | 镜像存储（registry v3） |
| registryctl | `docker.io/goharbor/harbor-registryctl:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/harbor-registryctl:v2.15.4` | Registry 管理 API（与 registry 同 Pod） |
| portal | `docker.io/goharbor/harbor-portal:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/harbor-portal:v2.15.4` | Web 控制台（nginx 静态站点） |
| trivy | `docker.io/goharbor/trivy-adapter-photon:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/trivy-adapter-photon:v2.15.4` | 漏洞扫描（Trivy adapter，内含 trivy binary） |
| database | `docker.io/goharbor/harbor-db:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/harbor-db:v2.15.4` | 内置 PostgreSQL（StatefulSet） |
| cache | `docker.io/goharbor/valkey-photon:v2.15.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/valkey-photon:v2.15.4` | 内置 Valkey（Redis 兼容，StatefulSet） |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| nginx 反代 | `docker.io/goharbor/nginx-photon:v2.15.4` | `expose.type=clusterIP/nodePort/loadBalancer`（非 ingress 暴露）时渲染 |
| exporter | `docker.io/goharbor/harbor-exporter:v2.15.4` | `metrics.enabled=true` 时渲染 |

> Trivy 扫描漏洞库（`trivy.db` / `trivy-java.db`）默认在 jobservice 首次扫描时从 GitHub 下载，离线环境需配置 `trivy.offlineScan` 并预置 DB（可挂载 PV 或用 `TRIVY_DB_REPOSITORY` 指向内部镜像源）。

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

## 离线 / 私有仓库建议

1. 将上面 10 个原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/goharbor/`（保持 tag 不变，含两个可选镜像）；
2. Chart 包内默认 values 已全部指向 SWR mirror，离线环境开箱即用；
3. Trivy 漏洞库离线：预下载 `db/trivy.db` 与 `java-trivy.db` 放入共享 PVC，或配置内部漏洞库镜像源。

## 备注

- Chart 1.19.4 是 Harbor 官方 Helm 仓库当前最新稳定版；Harbor 2.15 起已移除 Notary 与 Chartmuseum（chart 存储走 OCI artifact），缓存层由 Redis 改为 Valkey。
- 默认 `expose.type=ingress`（需集群已装 ingress controller，Ingress NGINX 已在应用商店提供）；`externalURL` 需改为实际访问地址。
- 默认使用内置 PostgreSQL/Valkey（StatefulSet + PVC），生产建议 `database.type=external` / `redis.type=external` 接管外部实例以简化备份扩容。
- Harbor 高可用至少需要：core/jobservice/portal 多副本 + 外部 PG/Redis + 共享存储（PVC 或外部对象存储）。

## 参考

- Chart 源码：<https://github.com/goharbor/harbor-helm>
- Harbor 项目：<https://github.com/goharbor/harbor>
- Helm 仓库：`helm repo add harbor https://helm.goharbor.io`
