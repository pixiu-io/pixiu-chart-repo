# MongoDB Exporter（prometheus-mongodb-exporter）

> 分类：可观测性　|　用途：把 MongoDB 的运行指标暴露为 Prometheus 格式，供 Pixiu 统一监控与告警。

| 项 | 值 |
| --- | --- |
| Chart | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| 仓库版本 | **3.23.2**（`charts/prometheus-mongodb-exporter-3.23.2.tgz`） |
| appVersion | **0.54.0** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| 镜像清单 | [prometheus-mongodb-exporter-images.md](../prometheus-mongodb-exporter-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 3.23.2 | 0.54.0 | `charts/prometheus-mongodb-exporter-3.23.2.tgz` | 官方最新稳定版 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）。

通过 `mongodb.uri` 或 `existingSecret`（key 为 `mongodb-uri`）指定目标 MongoDB；支持副本集/分片集群模式，认证信息建议走 Secret 注入。

## 部署前置条件

在 values 中配置目标 MongoDB 连接串（`mongodb.uri`，如 `mongodb://user:pass@host:27017/admin`）或引用外部 Secret，确保网络可达。

## 验证方式

kubectl get pods -n monitoring | grep mongodb-exporter 为 Running；/metrics 中出现 mongodb_up、mongodb_ss_connections 等指标。

## 备注

- 与 Pixiu 已上架的 kube-prometheus-stack 配套使用：开启 ServiceMonitor 后由 Prometheus Operator 自动抓取；
- 对应 Pixiu 数据源页面：`middleware/mongodb`（如适用）。
