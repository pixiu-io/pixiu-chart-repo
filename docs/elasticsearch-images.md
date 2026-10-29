# Elasticsearch 镜像列表

对应 Chart：`elasticsearch`

| 项 | 值 |
| --- | --- |
| Chart | [elasticsearch](https://github.com/elastic/helm-charts/tree/main/elasticsearch) |
| Chart 版本 | **8.5.1**（仓库文件：`charts/elasticsearch-8.5.1.tgz`） |
| appVersion | **8.5.1**（Elasticsearch 版本） |
| 来源 | [helm.elastic.co](https://helm.elastic.co)（Elastic 官方 Helm 仓库最新稳定版） |
| Pixiu 默认调整 | 镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/elasticsearch/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。默认部署为 3 节点 StatefulSet（master/data 复合角色），所有节点共用同一镜像。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| elasticsearch 节点 | `docker.elastic.co/elasticsearch/elasticsearch:8.5.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/elasticsearch/elasticsearch:8.5.1` | Elasticsearch StatefulSet（默认 3 节点），含 `sysctlInitContainer`（同一镜像） |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| 无额外镜像 | — | Ingress、PDB、NetworkPolicy、PSP 等均为 ES 同镜像或不引入新镜像；values 中 `busybox` 仅为 preStop hook 注释示例，默认不渲染 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.elastic.co/elasticsearch/elasticsearch:8.5.1
```

## 离线 / 私有仓库建议

1. 将上面原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/elasticsearch/`（保持 tag 不变）；
2. Chart 包内默认 values 已指向 SWR mirror，离线环境开箱即用；
3. 若使用其他私有仓库，按 `image` 整体替换前缀（`imageTag` 单独控制版本）。

## 备注

- Chart 8.5.1 是 Elastic 官方 Helm 仓库（helm.elastic.co）当前最新稳定版；Elastic 在 8.5.1 之后已将 Elastic Stack Helm Charts 移交社区并归档（`elastic/helm-charts` 仓库 archived），后续版本官方推荐通过 ECK Operator 部署，不再发布传统 chart。
- Elasticsearch 安全自检（`xpack.security.enabled` 等）沿用 chart 默认值；默认开启 TLS 传输层认证（secret-cert.yaml），service 端口 `9200`（HTTP）/ `9300`（transport）。
- 默认 `resources` 为 requests 与 limits 各 cpu `1000m` / memory `2Gi`，`esJavaOpts`（JVM 堆）默认为空，小规格集群可按需调低 `resources` 或设置 `esJavaOpts`。

## 参考

- Chart 源码：<https://github.com/elastic/helm-charts/tree/main/elasticsearch>
- Elasticsearch 项目：<https://github.com/elastic/elasticsearch>
- Helm 仓库：`helm repo add elastic https://helm.elastic.co`
