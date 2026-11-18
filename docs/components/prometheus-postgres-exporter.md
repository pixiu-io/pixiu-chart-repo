# PostgreSQL Exporter（prometheus-postgres-exporter）

> 分类：可观测性　|　用途：把 PostgreSQL Exporter 的运行指标暴露为 Prometheus 格式，供 Pixiu 统一监控与告警。

| 项 | 值 |
| --- | --- |
| Chart | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| 仓库版本 | **8.2.5**（`charts/prometheus-postgres-exporter-8.2.5.tgz`） |
| appVersion | **v0.20.1** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [prometheus-postgres-exporter-images.md](../prometheus-postgres-exporter-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 8.2.5 | v0.20.1 | `charts/prometheus-postgres-exporter-8.2.5.tgz` | 官方最新稳定版 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）。

渲染时必须提供数据源密码（config.datasource.password 或 passwordSecret/passwordFile/config.datasourceSecret），否则模板报错。

## 部署前置条件

必须提供 config.datasource.host 与密码（config.datasource.password 或 config.datasourceSecret 等），否则 helm template/install 会失败。

## 验证方式

kubectl get pods -n monitoring | grep postgres-exporter 为 Running；/metrics 中出现 pg_up、pg_stat_* 等指标。

## 备注

- 与 Pixiu 已上架的 kube-prometheus-stack 配套使用：开启 ServiceMonitor 后由 Prometheus Operator 自动抓取；
- 对应 Pixiu 数据源页面：`middleware/postgres`（如适用）。
