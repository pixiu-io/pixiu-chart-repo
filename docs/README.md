# 文档索引

> 最后更新：2026-10-25　|　维护：平台组

每个主题对应一个独立 Markdown 文档，本文件仅作索引。

## 索引

| 编号 | 标题 | 分类 | 文档 |
|---|---|---|---|
| DOC-001 | 应用商店 Chart 添加说明 | 应用商店 / Chart 管理 | [appstore-chart-guide.md](./appstore-chart-guide.md) |
| DOC-002 | Prometheus（Operator）镜像清单 | 应用商店 / 镜像 | [prometheus-images.md](./prometheus-images.md) |
| DOC-003 | Velero 镜像清单 | 应用商店 / 镜像 | [velero-images.md](./velero-images.md) |
| DOC-004 | GPU Operator 镜像清单 | 应用商店 / 镜像 | [gpu-operator-images.md](./gpu-operator-images.md) |
| DOC-005 | Ingress NGINX 镜像清单 | 应用商店 / 镜像 | [ingress-nginx-images.md](./ingress-nginx-images.md) |
| DOC-006 | MinIO 镜像清单 | 应用商店 / 镜像 | [minio-images.md](./minio-images.md) |
| DOC-007 | Loki 镜像清单 | 应用商店 / 镜像 | [loki-images.md](./loki-images.md) |
| DOC-008 | Promtail 镜像清单 | 应用商店 / 镜像 | [promtail-images.md](./promtail-images.md) |
| DOC-009 | Cert-manager 镜像清单 | 应用商店 / 镜像 | [cert-manager-images.md](./cert-manager-images.md) |
| DOC-010 | Longhorn 镜像清单 | 应用商店 / 镜像 | [longhorn-images.md](./longhorn-images.md) |
| DOC-011 | Elasticsearch 镜像清单 | 应用商店 / 镜像 | [elasticsearch-images.md](./elasticsearch-images.md) |

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
