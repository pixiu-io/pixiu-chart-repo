# MySQL Exporter（prometheus-mysql-exporter）

> 分类：可观测性　|　用途：把 MySQL Exporter 的运行指标暴露为 Prometheus 格式，供 Pixiu 统一监控与告警。

| 项 | 值 |
| --- | --- |
| Chart | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| 仓库版本 | **2.17.1**（`charts/prometheus-mysql-exporter-2.17.1.tgz`） |
| appVersion | **v0.21.0** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [prometheus-mysql-exporter-images.md](../prometheus-mysql-exporter-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 2.17.1 | v0.21.0 | `charts/prometheus-mysql-exporter-2.17.1.tgz` | 官方最新稳定版 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）。

默认只部署 mysqld-exporter 本体；数据源 DSN 通过 existingSecret 或 config 提供。cloud-sql-proxy sidecar 默认关闭，仅在 cloudsqlproxy.enabled=true 时渲染。

## 部署前置条件

需在 values 中配置 MySQL 数据源连接信息（config.datasource.* 或引用已有 Secret），并确保 exporter 所在 Pod 能访问 MySQL 端口。

## 验证方式

kubectl get pods -n monitoring | grep mysql-exporter 为 Running；访问 Service 的 /metrics 确认有 mysql_up 等指标。

## 备注

- 与 Pixiu 已上架的 kube-prometheus-stack 配套使用：开启 ServiceMonitor 后由 Prometheus Operator 自动抓取；
- 对应 Pixiu 数据源页面：`middleware/mysqld`（如适用）。
