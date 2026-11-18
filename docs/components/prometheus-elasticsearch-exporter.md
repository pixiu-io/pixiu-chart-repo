# Elasticsearch Exporter（prometheus-elasticsearch-exporter）

> 分类：可观测性　|　用途：把 Elasticsearch Exporter 的运行指标暴露为 Prometheus 格式，供 Pixiu 统一监控与告警。

| 项 | 值 |
| --- | --- |
| Chart | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| 仓库版本 | **7.5.0**（`charts/prometheus-elasticsearch-exporter-7.5.0.tgz`） |
| appVersion | **v1.11.0** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [prometheus-elasticsearch-exporter-images.md](../prometheus-elasticsearch-exporter-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 7.5.0 | v1.11.0 | `charts/prometheus-elasticsearch-exporter-7.5.0.tgz` | 官方最新稳定版 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）。

通过 ES REST API 采集指标，支持配置 es.uri、es.all、es.indices 等；Pixiu 应用商店已上架 elasticsearch 8.5.1 chart，二者可配套部署。

## 部署前置条件

在 values 的 es.uri 中填写 Elasticsearch 访问地址（如 http://elasticsearch-master:9200），如需认证配置 es.username/password 或 Secret。

## 验证方式

kubectl get pods -n monitoring | grep elasticsearch-exporter 为 Running；/metrics 中出现 elasticsearch_cluster_health_* 等指标。

## 备注

- 与 Pixiu 已上架的 kube-prometheus-stack 配套使用：开启 ServiceMonitor 后由 Prometheus Operator 自动抓取；
- 对应 Pixiu 数据源页面：`middleware/elasticsearch`（如适用）。
