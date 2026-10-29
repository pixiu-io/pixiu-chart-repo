# Promtail（promtail）

> 分类：可观测性　|　用途：以 DaemonSet 在每个节点采集容器日志并推送到 Loki。

| 项 | 值 |
| --- | --- |
| Chart | [promtail](https://github.com/grafana/loki/tree/main/clients/promtail) |
| 仓库版本 | **6.17.1**（`charts/promtail-6.17.1.tgz`） |
| appVersion | **3.5.1**（Promtail 版本） |
| 来源 | [grafana/helm-charts](https://github.com/grafana/helm-charts)（官方 Helm 仓库） |
| 镜像清单 | [promtail-images.md](../promtail-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 6.17.1 | 3.5.1 | `charts/promtail-6.17.1.tgz` | grafana 官方仓库当前最新稳定版；Promtail 已进入维护模式 |

Promtail 以 DaemonSet 方式在每个节点采集容器日志，`config.clients` 中的 `url` 需指向 Loki 的 push 端点（默认 `http://loki-gateway/loki/api/v1/push`）。

## 镜像

镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/grafana/`）。默认 values 下仅拉取 1 个镜像：`promtail:3.5.1`（日志采集 DaemonSet）；可选 configmap-reload sidecar（`sidecar.configReloader.enabled: true` 时启用）。

完整镜像明细见镜像清单。

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/grafana/promtail:3.5.1
ghcr.io/jimmidyson/configmap-reload:v0.12.0
```

## 安装说明

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 换用其他私有仓库后镜像拉取失败 | Chart 模板对 registry/repository 是强制拼接（`{{ registry }}/{{ repository }}`），只改其中一项会拼出错误地址 | 同时替换 `image.registry` 与 `image.repository`（本包将 `image.registry` 设为 SWR 域名、`image.repository` 设为 `pixiu-public/grafana/promtail`，二者缺一不可） |

## 相关链接

- [镜像清单](../promtail-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/grafana/helm-charts
