# Redis Exporter（prometheus-redis-exporter）

> 分类：可观测性　|　用途：把 Redis Exporter 的运行指标暴露为 Prometheus 格式，供 Pixiu 统一监控与告警。

| 项 | 值 |
| --- | --- |
| Chart | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| 仓库版本 | **6.37.0**（`charts/prometheus-redis-exporter-6.37.0.tgz`） |
| appVersion | **v1.97.0** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [prometheus-redis-exporter-images.md](../prometheus-redis-exporter-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 6.37.0 | v1.97.0 | `charts/prometheus-redis-exporter-6.37.0.tgz` | 官方最新稳定版 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）。

支持单实例/哨兵/集群模式，通过 redisAddress 或 config 指定目标；认证通过 Secret 注入。

## 部署前置条件

在 values 中配置目标 Redis 地址（redisAddress 或 extraArgs）及认证信息（如需），确保网络可达。

## 验证方式

kubectl get pods -n monitoring | grep redis-exporter 为 Running；/metrics 中出现 redis_up、redis_connected_clients 等指标。

## 备注

- 与 Pixiu 已上架的 kube-prometheus-stack 配套使用：开启 ServiceMonitor 后由 Prometheus Operator 自动抓取；
- 对应 Pixiu 数据源页面：`middleware/redis`（如适用）。
