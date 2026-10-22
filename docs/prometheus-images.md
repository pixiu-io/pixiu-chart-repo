# Prometheus（Operator）镜像列表

对应 Chart：`kube-prometheus-stack`（Prometheus Operator 方式）

| 项 | 值 |
| --- | --- |
| Chart | [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) |
| Chart 版本 | **92.11.0**（仓库文件：`charts/kube-prometheus-stack-92.11.0.tgz`） |
| appVersion | **v0.94.1**（Prometheus Operator 版本） |
| 来源 | [prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts/) |

> 下列镜像取自 Chart **默认 values**（组件默认 `enabled`）。关闭子组件或覆盖 `image` 后，实际拉取列表会变化。

## 默认会拉取的镜像

| 组件 | 镜像 | 说明 |
| --- | --- | --- |
| prometheus-operator | `quay.io/prometheus-operator/prometheus-operator:v0.94.1` | Operator 控制器（tag 为空时使用 Chart `appVersion`） |
| prometheus-config-reloader | `quay.io/prometheus-operator/prometheus-config-reloader:v0.94.1` | Prometheus / Alertmanager 配置热加载 |
| admission-webhook | `quay.io/prometheus-operator/admission-webhook:v0.94.1` | Operator Admission Webhook |
| kube-webhook-certgen | `ghcr.io/jkroepke/kube-webhook-certgen:1.11.0` | Webhook 证书生成 / 注入 Job（`admissionWebhooks.patch`） |
| prometheus | `quay.io/prometheus/prometheus:v3.15.0-distroless` | Prometheus Server |
| alertmanager | `quay.io/prometheus/alertmanager:v0.34.1` | Alertmanager |
| grafana | `docker.io/grafana/grafana:13.2.4-distroless` | Grafana（子 chart appVersion `13.2.4`） |
| grafana initChownData | `docker.io/library/busybox:1.38.0` | Grafana 数据目录权限初始化 |
| grafana sidecar | `quay.io/kiwigrid/k8s-sidecar:2.14.1` | 加载 dashboard / datasource ConfigMap |
| kube-state-metrics | `registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.20.0` | 集群对象指标（tag 为空时用子 chart appVersion） |
| node-exporter | `quay.io/prometheus/node-exporter:v1.12.1` | 节点指标 DaemonSet（tag 为空时用子 chart appVersion） |

## 默认不启用（可选）

| 组件 | 默认镜像 | 何时需要 |
| --- | --- | --- |
| thanos / thanosRuler | `quay.io/thanos/thanos:v0.42.4` | 开启 Thanos / `thanosRuler.enabled` |
| windows-exporter | 见 `prometheus-windows-exporter` 子 chart | `windowsMonitoring.enabled=true` |
| kube-rbac-proxy | `quay.io/brancz/kube-rbac-proxy:v0.23.0` | 为 kube-state-metrics / node-exporter 开启 `kubeRBACProxy` |
| grafana-image-renderer | `docker.io/grafana/grafana-image-renderer:latest` | 开启 Grafana 图片渲染 |
| CRD upgrade Job | `docker.io/busybox:latest`、`registry.k8s.io/kubectl:<k8s-version>` | `crds.upgradeJob.enabled=true` |

## 离线 / 私有仓库建议

1. 按上表拉取并推送到私有镜像仓库。  
2. 安装时通过 values 覆盖各组件的 `registry` / `repository` / `tag`（或全局 `global.imageRegistry`，若 Chart 支持）。  
3. 旧版兼容：仓库仍保留 `kube-prometheus-stack-65.1.1.tgz`；经典非 Operator 包为 `prometheus-25.10.0.tgz`，镜像集与本表不同。

## 参考

- Chart 源码与升级说明：<https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack>  
- Helm 仓库：`helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`  
- OCI：`oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack`
