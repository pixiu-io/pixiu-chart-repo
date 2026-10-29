# Pixiu 应用商店 Chart 仓库

本仓库存放 Pixiu 应用商店使用的 Helm Chart 包。

[文档索引](docs/README.md) · [上架与打包规范](docs/appstore-chart-guide.md) · [charts/](charts)

快速导航：[可观测性](#可观测性) · [存储与备份](#存储与备份) · [网络与安全](#网络与安全) · [数据库与中间件](#数据库与中间件) · [镜像仓库](#镜像仓库) · [GPU-与加速](#gpu-与加速)

# 组件列表

## 可观测性

| 组件 | Chart | 仓库版本 | appVersion | 详情 |
| --- | --- | --- | --- | --- |
| [Prometheus Operator](docs/components/prometheus-operator.md) | kube-prometheus-stack | **92.11.0**<br><sub>charts/kube-prometheus-stack-92.11.0.tgz</sub> | **v0.94.1** | <span style="font-size:14px">[查看](docs/components/prometheus-operator.md)</span> |
| [Loki](docs/components/loki.md) | loki | **7.5.0**<br><sub>charts/loki-7.5.0.tgz</sub> | **3.6.16** | <span style="font-size:14px">[查看](docs/components/loki.md)</span> |
| [Promtail](docs/components/promtail.md) | promtail | **6.17.1**<br><sub>charts/promtail-6.17.1.tgz</sub> | **3.5.1** | <span style="font-size:14px">[查看](docs/components/promtail.md)</span> |
| [Elasticsearch](docs/components/elasticsearch.md) | elasticsearch | **8.5.1**<br><sub>charts/elasticsearch-8.5.1.tgz</sub> | **8.5.1** | <span style="font-size:14px">[查看](docs/components/elasticsearch.md)</span> |

## 存储与备份

| 组件 | Chart | 仓库版本 | appVersion | 详情 |
| --- | --- | --- | --- | --- |
| [Longhorn](docs/components/longhorn.md) | longhorn | **1.13.0**<br><sub>charts/longhorn-1.13.0.tgz</sub><br>**1.12.1**<br><sub>charts/longhorn-1.12.1.tgz</sub> | **v1.13.0** / **v1.12.1** | <span style="font-size:14px">[查看](docs/components/longhorn.md)</span> |
| [MinIO](docs/components/minio.md) | minio | **5.4.0**<br><sub>charts/minio-5.4.0.tgz</sub> | **RELEASE.2025-09-07T16-13-09Z** | <span style="font-size:14px">[查看](docs/components/minio.md)</span> |
| [Velero](docs/components/velero.md) | velero | **12.2.1**<br><sub>charts/velero-12.2.1.tgz</sub> | **1.18.2** | <span style="font-size:14px">[查看](docs/components/velero.md)</span> |

## 网络与安全

| 组件 | Chart | 仓库版本 | appVersion | 详情 |
| --- | --- | --- | --- | --- |
| [Ingress NGINX](docs/components/ingress-nginx.md) | ingress-nginx | **4.15.1**<br><sub>charts/ingress-nginx-4.15.1.tgz</sub> | **1.15.1** | <span style="font-size:14px">[查看](docs/components/ingress-nginx.md)</span> |
| [Cert-manager](docs/components/cert-manager.md) | cert-manager | **v1.21.3**<br><sub>charts/cert-manager-v1.21.3.tgz</sub> | **v1.21.3** | <span style="font-size:14px">[查看](docs/components/cert-manager.md)</span> |

## 数据库与中间件

| 组件 | Chart | 仓库版本 | appVersion | 详情 |
| --- | --- | --- | --- | --- |
| [MySQL Operator](docs/components/mysql-operator.md) | mysql-operator | **2.3.1**<br><sub>charts/mysql-operator-2.3.1.tgz</sub> | **26.10.0-2.3.1** | <span style="font-size:14px">[查看](docs/components/mysql-operator.md)</span> |
| [Redis Operator](docs/components/redis-operator.md) | redis-operator | **0.27.0**<br><sub>charts/redis-operator-0.27.0.tgz</sub> | **0.27.0** | <span style="font-size:14px">[查看](docs/components/redis-operator.md)</span> |

## 镜像仓库

| 组件 | Chart | 仓库版本 | appVersion | 详情 |
| --- | --- | --- | --- | --- |
| [Harbor](docs/components/harbor.md) | harbor | **1.19.4**<br><sub>charts/harbor-1.19.4.tgz</sub> | **2.15.4** | <span style="font-size:14px">[查看](docs/components/harbor.md)</span> |

## GPU 与加速

| 组件 | Chart | 仓库版本 | appVersion | 详情 |
| --- | --- | --- | --- | --- |
| [GPU Operator](docs/components/gpu-operator.md) | gpu-operator | **v26.7.2**<br><sub>charts/gpu-operator-v26.7.2.tgz</sub> | **v26.7.2** | <span style="font-size:14px">[查看](docs/components/gpu-operator.md)</span> |

# 仓库约定

| 目录 / 文件 | 说明 |
| --- | --- |
| [charts/](charts) | Helm Chart 归档包（`.tgz`） |
| [docs/](docs) | 镜像清单与上架规范文档 |
| [docs/components/](docs/components) | 组件详情页 |
| [scripts/check-chart-tgz.py](scripts/check-chart-tgz.py) | Chart 包自检脚本（清理 macOS 元数据残留） |

打包与自检：

```bash
COPYFILE_DISABLE=1 helm package ./chart
python3 scripts/check-chart-tgz.py charts/*.tgz
```

新增组件流程：

1. 打 chart：`COPYFILE_DISABLE=1 helm package ./chart`，产物归档到 `charts/`
2. 补 `docs/<chart>-images.md` 镜像清单
3. 新增 `docs/components/<chart>.md` 组件详情
4. 更新本 README 分类表与 [docs/README.md](docs/README.md) 索引

完整上架、打包、镜像处理与校验规范见 [docs/appstore-chart-guide.md](docs/appstore-chart-guide.md)。
