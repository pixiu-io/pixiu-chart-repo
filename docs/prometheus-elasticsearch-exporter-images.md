# Elasticsearch Exporter 镜像列表

对应 Chart：`prometheus-elasticsearch-exporter`

| 项 | 值 |
| --- | --- |
| Chart | [ prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| Chart 版本 | **7.5.0**（仓库文件：`charts/prometheus-elasticsearch-exporter-7.5.0.tgz`） |
| appVersion | **v1.11.0** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间） |

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| 主镜像 | `quay.io/prometheuscommunity/elasticsearch-exporter:v1.11.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prometheuscommunity/elasticsearch-exporter:v1.11.0` | 导出器本体 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/prometheuscommunity/elasticsearch-exporter:v1.11.0
```

## 离线 / 私有仓库建议

1. 将上面原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/` 对应命名空间下，保持 tag 不变；
2. Chart 包内 values 已做镜像地址替换，`helm template` 渲染验证全部指向 SWR；
3. 其余 DSN / 认证配置属运行时参数，不影响镜像拉取。

## 备注

- 通过 ES REST API 采集指标，支持配置 es.uri、es.all、es.indices 等；Pixiu 应用商店已上架 elasticsearch 8.5.1 chart，二者可配套部署。
