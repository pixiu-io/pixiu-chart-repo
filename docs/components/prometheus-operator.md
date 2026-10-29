# Prometheus Operator（kube-prometheus-stack）

> 分类：可观测性　|　用途：以 Prometheus Operator 方式提供集群监控与告警，内置 Prometheus Server、kube-state-metrics 与 node-exporter。

| 项 | 值 |
| --- | --- |
| Chart | [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) |
| 仓库版本 | **92.11.0**（`charts/kube-prometheus-stack-92.11.0.tgz`） |
| appVersion | **v0.94.1**（Prometheus Operator 版本） |
| 来源 | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts/) |
| 镜像清单 | [prometheus-images.md](../prometheus-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 92.11.0 | v0.94.1 | `charts/kube-prometheus-stack-92.11.0.tgz` | 仓库当前唯一版本，默认关闭 grafana 与 alertmanager |

本仓库对该 Chart 默认 values 做了定制：默认关闭 `grafana` 与 `alertmanager`；覆盖 `enabled` 或 `image` 后，实际拉取列表会变化。

## 镜像

所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/`）。默认 values 下共拉取 6 个镜像：prometheus-operator、prometheus-config-reloader、kube-webhook-certgen、prometheus、kube-state-metrics、node-exporter；Chart 包内已把默认镜像写成 SWR mirror，离线安装无需额外覆盖 `image`。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| prometheus-operator | `.../pixiu-public/prom/prometheus-operator:v0.94.1` | Operator 控制器（tag 为空时使用 Chart appVersion） |
| prometheus-config-reloader | `.../pixiu-public/prom/prometheus-config-reloader:v0.94.1` | Prometheus / Alertmanager 配置热加载 |
| prometheus | `.../pixiu-public/prom/prometheus:v3.15.0-distroless` | Prometheus Server |
| kube-state-metrics | `.../pixiu-public/prom/kube-state-metrics:v2.20.0` | 集群对象指标 |
| node-exporter | `.../pixiu-public/prom/node-exporter:v1.12.1-distroless` | 节点指标 DaemonSet |

可选组件（默认不启用）：alertmanager、grafana（含 initChownData、sidecar、testFramework、image-renderer）、admission-webhook、thanos / thanosRuler、windows-exporter、kube-rbac-proxy 与 CRD upgrade Job，全部明细见镜像清单。

## 原生镜像

上游原始镜像地址（含默认与可选组件），可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/prometheus-operator/prometheus-operator:v0.94.1
quay.io/prometheus-operator/prometheus-config-reloader:v0.94.1
ghcr.io/jkroepke/kube-webhook-certgen:1.11.0
quay.io/prometheus/prometheus:v3.15.0-distroless
registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.20.0
quay.io/prometheus/node-exporter:v1.12.1-distroless
quay.io/prometheus/alertmanager:v0.34.1
docker.io/grafana/grafana:13.2.4-distroless
docker.io/library/busybox:1.38.0
quay.io/kiwigrid/k8s-sidecar:2.14.1
quay.io/prometheus-operator/admission-webhook:v0.94.1
quay.io/thanos/thanos:v0.42.4
ghcr.io/prometheus-community/windows-exporter:0.31.9
quay.io/brancz/kube-rbac-proxy:v0.23.0
docker.io/grafana/grafana-image-renderer:latest
docker.io/bats/bats:1.14.0
docker.io/busybox:latest
registry.k8s.io/kubectl:<k8s-version>
```

## 安装说明

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

暂无已记录的常见问题。

## 相关链接

- [镜像清单](../prometheus-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/prometheus-community/helm-charts
