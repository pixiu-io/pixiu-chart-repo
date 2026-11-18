# PostgreSQL Exporter 镜像列表

对应 Chart：`prometheus-postgres-exporter`

| 项 | 值 |
| --- | --- |
| Chart | [ prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| Chart 版本 | **8.2.5**（仓库文件：`charts/prometheus-postgres-exporter-8.2.5.tgz`） |
| appVersion | **v0.20.1** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间） |

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| 主镜像 | `quay.io/prometheuscommunity/postgres-exporter:v0.20.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/prometheuscommunity/postgres-exporter:v0.20.1` | 导出器本体 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/prometheuscommunity/postgres-exporter:v0.20.1
```

## 离线 / 私有仓库建议

1. 将上面原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/` 对应命名空间下，保持 tag 不变；
2. Chart 包内 values 已做镜像地址替换，`helm template` 渲染验证全部指向 SWR；
3. 其余 DSN / 认证配置属运行时参数，不影响镜像拉取。

## 备注

- 渲染时必须提供数据源密码（config.datasource.password 或 passwordSecret/passwordFile/config.datasourceSecret），否则模板报错。
