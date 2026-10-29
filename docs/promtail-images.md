# Promtail 镜像列表

对应 Chart：`promtail`

| 项 | 值 |
| --- | --- |
| Chart | [promtail](https://github.com/grafana/loki/tree/main/clients/promtail) |
| Chart 版本 | **6.17.1**（仓库文件：`charts/promtail-6.17.1.tgz`） |
| appVersion | **3.5.1**（Promtail 版本） |
| 来源 | [grafana/helm-charts](https://github.com/grafana/helm-charts)（官方 Helm 仓库） |
| Pixiu 默认调整 | 镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。Promtail 以 DaemonSet 方式在每个节点采集容器日志，`config.clients` 中的 `url` 需指向 Loki 的 push 端点（默认 `http://loki-gateway/loki/api/v1/push`）。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| promtail | `docker.io/grafana/promtail:3.5.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/promtail:3.5.1` | 日志采集 DaemonSet |

> 注意：Chart 模板对 registry/repository 是**强制拼接**（`{{ registry }}/{{ repository }}`），本包将 `image.registry` 设为 SWR 域名、`image.repository` 设为 `pixiu-public/grafana/promtail`，二者缺一不可。

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| configmap-reload（sidecar） | `ghcr.io/jimmidyson/configmap-reload:v0.12.0` | `sidecar.configReloader.enabled: true` 时；mirror：`swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/configmap-reload:v0.12.0` |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/grafana/promtail:3.5.1
ghcr.io/jimmidyson/configmap-reload:v0.12.0
```

## 离线 / 私有仓库建议

1. 将上面的原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/`（保持 tag 不变）；
2. Chart 包内默认 values 已指向 SWR mirror，离线环境开箱即用；
3. 若使用其他私有仓库，需同时替换 `image.registry` 与 `image.repository`（模板不做智能拼接）。

## 备注

- Chart 6.17.1 为 grafana 官方仓库当前最新稳定版。
- Promtail 已进入维护模式（Loki 官方推荐新部署使用 Alloy），后续如需迁移另行评估。

## 参考

- Chart 源码：<https://github.com/grafana/helm-charts/tree/main/charts/promtail>
- Promtail 文档：<https://grafana.com/docs/loki/latest/clients/promtail/>
- Helm 仓库：`helm repo add grafana https://grafana.github.io/helm-charts`
