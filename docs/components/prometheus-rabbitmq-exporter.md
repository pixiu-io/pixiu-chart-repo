# RabbitMQ Exporter（prometheus-rabbitmq-exporter）

> 分类：可观测性　|　用途：把 RabbitMQ Exporter 的运行指标暴露为 Prometheus 格式，供 Pixiu 统一监控与告警。

| 项 | 值 |
| --- | --- |
| Chart | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| 仓库版本 | **2.1.3**（`charts/prometheus-rabbitmq-exporter-2.1.3.tgz`） |
| appVersion | **1.0.0** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [prometheus-rabbitmq-exporter-images.md](../prometheus-rabbitmq-exporter-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 2.1.3 | 1.0.0 | `charts/prometheus-rabbitmq-exporter-2.1.3.tgz` | 官方最新稳定版 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）。

通过 RabbitMQ Management API（默认 15672 端口）采集指标，目标集群需启用 rabbitmq_management 插件。

## 部署前置条件

目标 RabbitMQ 必须启用 management 插件（rabbitmq-plugins enable rabbitmq_management），并在 values 中通过 rabbitmq.* 或 secret 提供地址与凭据。

## 验证方式

kubectl get pods -n monitoring | grep rabbitmq-exporter 为 Running；/metrics 中出现 rabbitmq_up、rabbitmq_queue_messages 等指标。

## 备注

- 与 Pixiu 已上架的 kube-prometheus-stack 配套使用：开启 ServiceMonitor 后由 Prometheus Operator 自动抓取；
- 对应 Pixiu 数据源页面：`middleware/rabbitmq`（如适用）。
