# MongoDB Exporter 镜像列表

对应 Chart：`prometheus-mongodb-exporter`

| 项 | 值 |
| --- | --- |
| Chart | [ prometheus-community/helm-charts](https://github.com/prometheus-community/helm-charts) |
| Chart 版本 | **3.23.2**（仓库文件：`charts/prometheus-mongodb-exporter-3.23.2.tgz`） |
| appVersion | **0.54.0** |
| 来源 | [prometheus-community/helm-charts](https://prometheus-community.github.io/helm-charts) 官方 Helm 仓库最新稳定版 |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间） |

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| 主镜像 | `docker.io/percona/mongodb_exporter:0.54.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/percona/mongodb_exporter:0.54.0` | 导出器本体 |
| 测试 Pod | `docker.io/library/busybox:latest` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/busybox:latest` | 仅 `helm test` 连通性测试使用 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/percona/mongodb_exporter:0.54.0
docker.io/library/busybox:latest
```

## 离线 / 私有仓库建议

1. 将上面原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/` 对应命名空间下，保持 tag 不变；
2. Chart 包内 values 与 test-connection 模板已做镜像地址替换，`helm template` 渲染验证全部指向 SWR；
3. 其余连接串 / 认证配置属运行时参数，不影响镜像拉取。

## 备注

- 通过 `mongodb.uri` 或 `existingSecret`（key 为 `mongodb-uri`）指定目标 MongoDB；认证信息建议走 Secret 注入；
- 上游 exporter 为 Percona 维护的 `percona/mongodb_exporter`，prometheus-community 官方 chart 引用该镜像。
