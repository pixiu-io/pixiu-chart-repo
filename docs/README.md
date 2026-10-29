# 文档索引

> 最后更新：2026-10-29　|　维护：平台组

每个主题对应一个独立 Markdown 文档，本文件仅作索引。

## 索引

| 编号 | 标题 | 分类 | 文档 |
|---|---|---|---|
| DOC-001 | 应用商店 Chart 添加说明 | 应用商店 / Chart 管理 | [appstore-chart-guide.md](./appstore-chart-guide.md) |
| DOC-002 | Prometheus（Operator）镜像列表 | 应用商店 / 镜像 | [prometheus-images.md](./prometheus-images.md) |
| DOC-003 | Velero 镜像列表 | 应用商店 / 镜像 | [velero-images.md](./velero-images.md) |
| DOC-004 | GPU Operator 镜像列表 | 应用商店 / 镜像 | [gpu-operator-images.md](./gpu-operator-images.md) |
| DOC-005 | Ingress NGINX 镜像列表 | 应用商店 / 镜像 | [ingress-nginx-images.md](./ingress-nginx-images.md) |
| DOC-006 | MinIO 镜像列表 | 应用商店 / 镜像 | [minio-images.md](./minio-images.md) |
| DOC-007 | Loki 镜像列表 | 应用商店 / 镜像 | [loki-images.md](./loki-images.md) |
| DOC-008 | Promtail 镜像列表 | 应用商店 / 镜像 | [promtail-images.md](./promtail-images.md) |
| DOC-009 | Cert-manager 镜像列表 | 应用商店 / 镜像 | [cert-manager-images.md](./cert-manager-images.md) |
| DOC-010 | Longhorn 镜像列表 | 应用商店 / 镜像 | [longhorn-images.md](./longhorn-images.md) |
| DOC-011 | Elasticsearch 镜像列表 | 应用商店 / 镜像 | [elasticsearch-images.md](./elasticsearch-images.md) |
| DOC-012 | Redis Operator 镜像列表 | 应用商店 / 镜像 | [redis-operator-images.md](./redis-operator-images.md) |
| DOC-013 | MySQL Operator 镜像列表 | 应用商店 / 镜像 | [mysql-operator-images.md](./mysql-operator-images.md) |
| DOC-014 | Harbor 镜像列表 | 应用商店 / 镜像 | [harbor-images.md](./harbor-images.md) |

## 组件详情

| 编号 | 标题 | 分类 | 文档 |
|---|---|---|---|
| DOC-015 | Prometheus Operator 组件详情 | 可观测性 | [components/prometheus-operator.md](./components/prometheus-operator.md) |
| DOC-016 | Loki 组件详情 | 可观测性 | [components/loki.md](./components/loki.md) |
| DOC-017 | Promtail 组件详情 | 可观测性 | [components/promtail.md](./components/promtail.md) |
| DOC-018 | Elasticsearch 组件详情 | 可观测性 | [components/elasticsearch.md](./components/elasticsearch.md) |
| DOC-019 | Longhorn 组件详情 | 存储与备份 | [components/longhorn.md](./components/longhorn.md) |
| DOC-020 | MinIO 组件详情 | 存储与备份 | [components/minio.md](./components/minio.md) |
| DOC-021 | Velero 组件详情 | 存储与备份 | [components/velero.md](./components/velero.md) |
| DOC-022 | Ingress NGINX 组件详情 | 网络与安全 | [components/ingress-nginx.md](./components/ingress-nginx.md) |
| DOC-023 | Cert-manager 组件详情 | 网络与安全 | [components/cert-manager.md](./components/cert-manager.md) |
| DOC-024 | MySQL Operator 组件详情 | 数据库与中间件 | [components/mysql-operator.md](./components/mysql-operator.md) |
| DOC-025 | Redis Operator 组件详情 | 数据库与中间件 | [components/redis-operator.md](./components/redis-operator.md) |
| DOC-026 | Harbor 组件详情 | 镜像仓库 | [components/harbor.md](./components/harbor.md) |
| DOC-027 | GPU Operator 组件详情 | GPU 与加速 | [components/gpu-operator.md](./components/gpu-operator.md) |

## 工具脚本

| 脚本 | 用途 |
|---|---|
| [scripts/check-chart-tgz.py](../scripts/check-chart-tgz.py) | 检查 / 清理 chart `.tgz` 中的 macOS `._*` / `.DS_Store` / `__MACOSX` 残留 |

合入 `charts/*.tgz` 前执行：`python3 scripts/check-chart-tgz.py charts/*.tgz`

**打包约定（详见 [appstore-chart-guide.md](./appstore-chart-guide.md)「标准流程」）**：最终包一律用 `COPYFILE_DISABLE=1 helm package ./chart`；禁止本机裸 `tar czf` 作为常规手段。

## 新增文档规范

1. 新建独立文件，命名 `<关键词>-<关键词>.md`
2. 文档结构固定：**适用范围 / 前置条件 / 操作步骤 / 验证方式 / 常见问题 / 备注**
3. 在本索引表追加一行并更新「最后更新」日期
