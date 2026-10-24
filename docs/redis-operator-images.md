# Redis Operator 镜像列表

对应 Chart：`redis-operator`

| 项 | 值 |
| --- | --- |
| Chart | [redis-operator](https://github.com/OT-CONTAINER-KIT/redis-operator) |
| Chart 版本 | **0.27.0**（仓库文件：`charts/redis-operator-0.27.0.tgz`） |
| appVersion | **0.27.0**（Redis Operator 版本） |
| 来源 | [ot-container-kit.github.io/helm-charts](https://ot-container-kit.github.io/helm-charts/) 官方 Helm 仓库最新稳定版 |
| Pixiu 默认调整 | 镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/redis-operator/`） |

> 本 chart 只部署 **Redis Operator** 本体（含 webhook 自签证书 init 容器，同镜像）。安装后通过 `Redis` / `RedisCluster` / `RedisReplication` / `RedisSentinel` CR 创建 Redis 实例，实例镜像由 CR 配置决定，不随本 chart 默认拉取。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| redis-operator | `quay.io/opstree/redis-operator:v0.27.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/redis-operator/redis-operator:v0.27.0` | Operator Deployment；init-config init 容器（webhook 证书生成）同镜像同 tag |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| Redis 实例镜像 | `quay.io/opstree/redis`、`quay.io/opstree/redis-sentinel` 等 | 安装 Operator 后创建 Redis/RedisCluster 等 CR 时按 CR 的 `kubernetesConfig.image` 拉取，需按需推送到 mirror 并在 CR 中指定 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/opstree/redis-operator:v0.27.0
```

## 离线 / 私有仓库建议

1. 将上面原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/redis-operator/`（保持 tag 不变）；
2. Chart 包内默认 values 已指向 SWR mirror（`redisOperator.imageName`），离线环境开箱即用；
3. 后续创建 Redis 实例 CR 时，将 `kubernetesConfig.image` 同样指向 SWR mirror 前缀（如需 `redis` / `redis-exporter` 等实例镜像，提前推送）。

## 备注

- Chart 0.27.0 是 OT-CONTAINER-KIT 官方 Helm 仓库当前最新稳定版。
- 默认 `webhook: false`（无需 cert-manager）；开启 webhook 后证书自动生成或由 cert-manager 管理。
- 安装本 chart 不会创建任何 Redis 实例，需再提交 CR（可另做 `redis-cluster` 等实例 chart）。
- Operator 默认 watch 全部命名空间，可通过 `watchNamespace` 收敛。

## 参考

- Chart 源码：<https://github.com/OT-CONTAINER-KIT/redis-operator>
- Helm 仓库：`helm repo add ot-helm https://ot-container-kit.github.io/helm-charts/`
