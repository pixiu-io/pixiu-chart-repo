# Velero（velero）

> 分类：存储与备份　|　用途：Kubernetes 集群资源与持久卷的备份、恢复与迁移。

| 项 | 值 |
| --- | --- |
| Chart | [velero](https://github.com/vmware-tanzu/helm-charts/tree/main/charts/velero) |
| 仓库版本 | **12.2.1**（`charts/velero-12.2.1.tgz`） |
| appVersion | **1.18.2** |
| 来源 | [vmware-tanzu/helm-charts](https://github.com/vmware-tanzu/helm-charts) |
| 镜像清单 | [velero-images.md](../velero-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 12.2.1 | 1.18.2 | `charts/velero-12.2.1.tgz` | Pixiu 修订包：默认存储位置置空、`initContainers` 默认携带 `velero-plugin-for-aws` |

## 镜像

所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/`）。默认 values 下会拉取 `velero` Server 与 `velero-plugin-for-aws` 两个镜像；Pixiu 修订包默认写入 `initContainers`，使用 S3 兼容对象存储无需额外配置。可选组件 node-agent、CRD cleanup 的 kubectl 以及 GCP / Azure 插件默认不启用，开启或配置插件后实际拉取列表会变化。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| velero | `.../pixiu-public/velero/velero:v1.18.2` | Velero Server Deployment；`upgradeCRDs=true` 时 CRD 升级 Job 共用此镜像 |
| velero-plugin-for-aws | `.../pixiu-public/velero/velero-plugin-for-aws:v1.13.1` | 默认写入 `initContainers`，提供 AWS / S3 兼容对象存储插件 |

完整镜像明细（含可选组件）见镜像清单。

## 原生镜像

上游原始镜像地址（含默认与可选组件），可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/velero/velero:v1.18.2
registry.k8s.io/kubectl:<k8s-version>
docker.io/velero/velero-plugin-for-aws:v1.13.1
docker.io/velero/velero-plugin-for-gcp:<tag>
docker.io/velero/velero-plugin-for-microsoft-azure:<tag>
```

## 安装说明

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

安装前需知（源文档已有事实）：

- 至少需要一个对象存储插件（`initContainers`），否则 Velero 无法完成真实备份；Pixiu 修订包已默认携带 `velero-plugin-for-aws`，使用 S3 兼容存储无需额外配置，其它云厂商可在安装 values 中替换或追加 `initContainers`。
- Pixiu 备份模块会自动创建/更新 BackupStorageLocation（provider 固定 `aws`，兼容 S3 协议的对象存储），无需 chart 预置；chart 内的存储位置仅用于不使用 Pixiu 备份模块、需要自行预置的场景，Pixiu 修订包默认已将其置为 `[]`。
- 离线环境至少拉取默认两个镜像；若开启 node-agent、CRD cleanup 或使用 GCP / Azure 存储插件，再补对应可选镜像。
- 使用其他私有仓库时，需覆盖 `image.repository` / `image.tag`、`kubectl.image.repository` / `kubectl.image.tag`（或改 `initContainers[].image`）。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 安装报 `spec.provider: Required value`（BackupStorageLocation / VolumeSnapshotLocation 无效） | 上游 12.2.1 的 `values.yaml` 默认带占位存储位置（`name` 为空、`provider: ""`），模板无条件渲染，而 CRD 要求 `spec.provider` 必填 | 使用 Pixiu 修订包（已将两项默认设为 `[]`）；已导入旧包的平台更新该版本「默认配置」或删除后重新导入，也可在 values 中将 `configuration.backupStorageLocation` / `volumeSnapshotLocation` 改为 `[]` |
| 备份失败报 `unable to locate ObjectStore plugin named velero.io/aws` | Velero Deployment 未配置对象存储插件 initContainer | 使用已默认携带 `velero-plugin-for-aws` 的修订包；已安装实例补上 `initContainers` 后 `helm upgrade` 并重启 Deployment |
| 上传同版本包后修订不生效 | 应用商店按 Chart 名称 + 版本判重，同版本重复上传不会覆盖生效 | 在应用商店更新该版本「默认配置」，或删除该版本后重新导入 `charts/velero-12.2.1.tgz` |

## 相关链接

- [镜像清单](../velero-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/vmware-tanzu/helm-charts
