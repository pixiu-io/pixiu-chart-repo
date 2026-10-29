# Elasticsearch（elasticsearch）

> 分类：可观测性　|　用途：分布式搜索与分析引擎，默认以 3 节点 StatefulSet 提供日志/数据检索能力。

| 项 | 值 |
| --- | --- |
| Chart | [elasticsearch](https://github.com/elastic/helm-charts/tree/main/elasticsearch) |
| 仓库版本 | **8.5.1**（`charts/elasticsearch-8.5.1.tgz`） |
| appVersion | **8.5.1**（Elasticsearch 版本） |
| 来源 | [helm.elastic.co](https://helm.elastic.co)（Elastic 官方 Helm 仓库最新稳定版；`elastic/helm-charts` 仓库已归档） |
| 镜像清单 | [elasticsearch-images.md](../elasticsearch-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 8.5.1 | 8.5.1 | `charts/elasticsearch-8.5.1.tgz` | Elastic 官方 Helm 仓库当前最新稳定版；之后官方推荐改用 ECK Operator 部署 |

默认部署为 3 节点 StatefulSet（master/data 复合角色），所有节点共用同一镜像。安全配置（`xpack.security.enabled` 等）沿用 chart 默认值，默认开启 TLS 传输层认证（`secret-cert.yaml`），service 端口 `9200`（HTTP）/ `9300`（transport）。默认资源为 requests 与 limits 各 cpu `1000m` / memory `2Gi`，`esJavaOpts`（JVM 堆）默认为空；小规格集群可按需调低 `resources` 或设置 `esJavaOpts`。

## 镜像

镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/elasticsearch/`）。默认 values 下仅拉取 1 个镜像：`elasticsearch:8.5.1`（StatefulSet，默认 3 节点，含 `sysctlInitContainer` 复用同一镜像）。

Ingress、PDB、NetworkPolicy、PSP 等均为 ES 同镜像或不引入新镜像；values 中 `busybox` 仅为 preStop hook 注释示例，默认不渲染。完整镜像明细见镜像清单。

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.elastic.co/elasticsearch/elasticsearch:8.5.1
```

## 安装说明

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

暂无已记录的常见问题。

## 相关链接

- [镜像清单](../elasticsearch-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/elastic/helm-charts
