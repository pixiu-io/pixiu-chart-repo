# Redis Operator（redis-operator）

> 分类：数据库与中间件　|　用途：以 CR 方式管理 Redis 单机、主从、哨兵与集群实例的 Operator。

| 项 | 值 |
| --- | --- |
| Chart | [redis-operator](https://github.com/OT-CONTAINER-KIT/redis-operator) |
| 仓库版本 | **0.27.0**（`charts/redis-operator-0.27.0.tgz`） |
| appVersion | **0.27.0** |
| 来源 | [ot-container-kit.github.io/helm-charts](https://ot-container-kit.github.io/helm-charts/) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [redis-operator-images.md](../redis-operator-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 0.27.0 | 0.27.0 | `charts/redis-operator-0.27.0.tgz` | Redis Operator 0.27.0，当前仓库收录版本 |

## 镜像

镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/redis-operator/`）。

默认只拉取 redis-operator 本体（`webhook: false`，不渲染 webhook Service/证书资源）；Redis 实例镜像由 CR 配置决定，不随本 Chart 默认拉取。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| redis-operator | `.../pixiu-public/redis-operator/redis-operator:v0.27.0` | Operator Deployment（`webhook=true` 时另启用 webhook Service 与证书资源，不引入新镜像） |
| Redis 实例镜像（可选） | 按 CR `kubernetesConfig.image` 指定 | `quay.io/opstree/redis`、`quay.io/opstree/redis-sentinel` 等需按需推送到 mirror |

完整镜像明细见镜像清单。

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/opstree/redis-operator:v0.27.0
```

## 安装说明

- 本 Chart 只部署 Redis Operator 本体；`webhook` 默认 `false`（无需 cert-manager），开启后证书由 Helm 自签或 cert-manager 管理。
- 安装后需提交 `Redis` / `RedisCluster` / `RedisReplication` / `RedisSentinel` CR 才会创建实例。

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

暂无已记录的常见问题。

## 相关链接

- [镜像清单](../redis-operator-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/OT-CONTAINER-KIT/redis-operator
