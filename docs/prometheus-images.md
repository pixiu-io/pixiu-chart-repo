# Prometheus（Operator）镜像列表

对应 Chart：`kube-prometheus-stack`（Prometheus Operator 方式）

| 项 | 值 |
| --- | --- |
| Chart | [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) |
| Chart 版本 | **92.11.0**（仓库文件：`charts/kube-prometheus-stack-92.11.0.tgz`） |
| appVersion | **v0.94.1**（Prometheus Operator 版本） |
| 来源 | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts/) |

> 本仓库对 Chart 默认 values 做了定制：默认关闭 `grafana` 与 `alertmanager`；所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/`）。覆盖 `enabled` 或 `image` 后，实际拉取列表会变化。

## 默认会拉取的镜像

| 组件 | 镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| prometheus-operator | `quay.io/prometheus-operator/prometheus-operator:v0.94.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/prometheus-operator:v0.94.1` | Operator 控制器（tag 为空时使用 Chart `appVersion`） |
| prometheus-config-reloader | `quay.io/prometheus-operator/prometheus-config-reloader:v0.94.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/prometheus-config-reloader:v0.94.1` | Prometheus / Alertmanager 配置热加载 |
| kube-webhook-certgen | `ghcr.io/jkroepke/kube-webhook-certgen:1.11.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/kube-webhook-certgen:1.11.0` | Webhook 证书生成 / 注入 Job（`admissionWebhooks.patch`） |
| prometheus | `quay.io/prometheus/prometheus:v3.15.0-distroless` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/prometheus:v3.15.0-distroless` | Prometheus Server |
| kube-state-metrics | `registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.20.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/kube-state-metrics:v2.20.0` | 集群对象指标（tag 为空时用子 chart appVersion） |
| node-exporter | `quay.io/prometheus/node-exporter:v1.12.1-distroless` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/node-exporter:v1.12.1-distroless` | 节点指标 DaemonSet（tag 为空时用子 chart appVersion） |

## 默认不启用（可选）

| 组件 | 默认镜像 | mirror 镜像 | 何时需要 |
| --- | --- | --- | --- |
| alertmanager | `quay.io/prometheus/alertmanager:v0.34.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/alertmanager:v0.34.1` | `alertmanager.enabled=true` |
| grafana | `docker.io/grafana/grafana:13.2.4-distroless` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/grafana:13.2.4-distroless` | `grafana.enabled=true` |
| grafana initChownData | `docker.io/library/busybox:1.38.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/busybox:1.38.0` | 随 `grafana.enabled=true` 一同部署 |
| grafana sidecar | `quay.io/kiwigrid/k8s-sidecar:2.14.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/k8s-sidecar:2.14.1` | 随 `grafana.enabled=true` 一同部署（加载 dashboard / datasource ConfigMap） |
| grafana testFramework | `docker.io/bats/bats:1.14.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/bats:1.14.0` | 仅 `helm test` 使用（`grafana.testFramework.enabled`） |
| admission-webhook | `quay.io/prometheus-operator/admission-webhook:v0.94.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/admission-webhook:v0.94.1` | `prometheusOperator.admissionWebhooks.deployment.enabled=true` |
| thanos / thanosRuler | `quay.io/thanos/thanos:v0.42.4` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/thanos:v0.42.4` | 开启 Thanos / `thanosRuler.enabled` |
| windows-exporter | `ghcr.io/prometheus-community/windows-exporter:0.31.9` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/windows-exporter:0.31.9` | `windowsMonitoring.enabled=true` |
| kube-rbac-proxy | `quay.io/brancz/kube-rbac-proxy:v0.23.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/kube-rbac-proxy:v0.23.0` | 为 kube-state-metrics / node-exporter 开启 `kubeRBACProxy` |
| grafana-image-renderer | `docker.io/grafana/grafana-image-renderer:latest` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/grafana-image-renderer:latest` | 开启 Grafana 图片渲染 |
| CRD upgrade Job | `docker.io/busybox:latest`、`registry.k8s.io/kubectl:<k8s-version>` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/busybox:latest`、`swr.cn-north-4.myhuaweicloud.com/pixiu-public/prom/kubectl:<k8s-version>` | `crds.upgradeJob.enabled=true` |

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

## 离线 / 私有仓库建议

1. 按上表拉取并推送到私有镜像仓库。  
2. 安装时通过 values 覆盖各组件的 `registry` / `repository` / `tag`（或全局 `global.imageRegistry`，若 Chart 支持）。  
3. Chart 包内已把默认镜像写成 SWR mirror，离线安装无需额外覆盖 `image`；若使用其他私有仓库，需按表中 mirror 列整体替换仓库前缀。

## 参考

- Chart 源码与升级说明：<https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack>  
- Helm 仓库：`helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`  
- OCI：`oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack`
