# Velero 镜像列表

对应 Chart：`velero`

| 项 | 值 |
| --- | --- |
| Chart | [velero](https://github.com/vmware-tanzu/helm-charts/tree/main/charts/velero) |
| Chart 版本 | **12.2.1**（仓库文件：`charts/velero-12.2.1.tgz`） |
| appVersion | **1.18.2**（Velero 版本） |
| 来源 | [vmware-tanzu/helm-charts](https://github.com/vmware-tanzu/helm-charts) |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values**（组件默认 `enabled`）整理。开启可选组件、配置插件或覆盖 `image` 后，实际拉取列表会变化。

## 默认会拉取的镜像

| 组件 | 镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| velero | `docker.io/velero/velero:v1.18.2` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero:v1.18.2` | Velero Server Deployment；`upgradeCRDs=true` 时升级 CRD Job 共用此镜像 |
| velero-plugin-for-aws | `docker.io/velero/velero-plugin-for-aws:v1.13.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero-plugin-for-aws:v1.13.1` | Pixiu 修订包默认写入 `initContainers`，提供 AWS / S3 兼容对象存储插件 |

## 默认不启用（可选）

| 组件 | 默认镜像 | mirror 镜像 | 何时需要 |
| --- | --- | --- | --- |
| node-agent | `docker.io/velero/velero:v1.18.2` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero:v1.18.2` | `deployNodeAgent=true`（与 Server 同镜像，DaemonSet） |
| kubectl（CRD cleanup Job） | `registry.k8s.io/kubectl:<k8s-version>` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/kubectl:<k8s-version>` | `cleanUpCRDs=true`（生产慎用）；tag 未设置时取集群 Kubernetes 版本 |
| velero-plugin-for-gcp | `docker.io/velero/velero-plugin-for-gcp:<tag>` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero-plugin-for-gcp:<tag>` | 使用 GCP 备份存储时（需替换或追加 `initContainers` 项） |
| velero-plugin-for-microsoft-azure | `docker.io/velero/velero-plugin-for-microsoft-azure:<tag>` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero-plugin-for-microsoft-azure:<tag>` | 使用 Azure 备份存储时（需替换或追加 `initContainers` 项） |

> 至少需要一个对象存储插件（`initContainers`），否则 Velero 无法完成真实备份；Pixiu 修订包已默认携带 `velero-plugin-for-aws`，使用 S3 兼容存储无需额外配置，其它云厂商可在安装 values 中替换或追加 `initContainers`。

## 原生镜像

上游原始镜像地址（含默认与可选组件），可直接批量 pull 后重新 tag / push 到私有仓库：

```text
docker.io/velero/velero:v1.18.2
registry.k8s.io/kubectl:<k8s-version>
docker.io/velero/velero-plugin-for-aws:v1.13.1
docker.io/velero/velero-plugin-for-gcp:<tag>
docker.io/velero/velero-plugin-for-microsoft-azure:<tag>
```

## 离线 / 私有仓库建议

1. 至少拉取「默认会拉取的镜像」并推送到私有镜像仓库（已包含 `velero-plugin-for-aws`）；若开启 node-agent、CRD cleanup 或使用 GCP / Azure 存储插件，再补可选表中对应镜像。  
2. 安装时通过 values 覆盖 `image.repository` / `image.tag`、`kubectl.image.repository` / `kubectl.image.tag`（或改 `initContainers[].image`）。  
3. Chart 包内已把默认镜像写成 SWR mirror，离线安装无需额外覆盖 Server / kubectl 仓库前缀；若使用其他私有仓库，需按表中 mirror 列整体替换。

## 参考

- Chart 源码：<https://github.com/vmware-tanzu/helm-charts/tree/main/charts/velero>  
- Velero 项目：<https://github.com/vmware-tanzu/velero>  
- Helm 仓库：`helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts`  

## 常见问题

### 安装报 `spec.provider: Required value`

**现象**：安装失败，报错类似：

```text
BackupStorageLocation.velero.io "default" is invalid: spec.provider: Required value
VolumeSnapshotLocation.velero.io "default" is invalid: spec.provider: Required value
```

**原因**：上游 12.2.1 的 `values.yaml` 默认带一个占位存储位置（`configuration.backupStorageLocation[0]`、`configuration.volumeSnapshotLocation[0]`，`name` 为空、`provider: ""`），模板会无条件渲染；而 CRD 要求 `spec.provider` 必填，因此校验失败。

**处理**：

- 使用本仓库 **12.2.1 Pixiu 修订包**（`charts/velero-12.2.1.tgz`，已将这两项默认设为 `[]`，不创建默认存储位置）。
- 已导入旧包的平台：更新该版本的「默认配置」或在应用商店删除后重新导入本修订包；也可在安装 values 中将这两项改为 `[]`：

  ```yaml
  configuration:
    backupStorageLocation: []
    volumeSnapshotLocation: []
  ```

**说明**：Pixiu 备份模块会自动创建/更新 BackupStorageLocation（provider 固定 `aws`，兼容 S3 协议的对象存储），无需 chart 预置；chart 内的存储位置仅用于不使用 Pixiu 备份模块、需要自行预置的场景。

### 备份失败报 `unable to locate ObjectStore plugin named velero.io/aws`

**现象**：备份或 BSL 校验失败，报错类似：

```text
BackupStorageLocation "default" is unavailable: unable to locate ObjectStore plugin named velero.io/aws
```

**原因**：Velero Deployment 未配置对象存储插件 initContainer，server 进程未加载 AWS / S3 插件。

**处理**：

- 本仓库 **12.2.1 Pixiu 修订包已默认在 `initContainers` 中携带 `velero-plugin-for-aws`**，新安装直接使用修订包即可。
- 已安装实例：把 `initContainers` 补上后 `helm upgrade` 并重启 Deployment，或升级到修订包：

  ```yaml
  initContainers:
    - name: velero-plugin-for-aws
      image: swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero-plugin-for-aws:v1.13.1
      imagePullPolicy: IfNotPresent
      volumeMounts:
        - mountPath: /target
          name: plugins
  ```

### 同版本 Chart 不可重复上传

应用商店按 Chart 名称 + 版本判重，**同一版本已在平台导入过后，再次上传同版本包不会覆盖生效**。曾导入过旧 12.2.1 的环境，需要：

1. 在应用商店更新该版本的「默认配置」（写入新的 `backupStorageLocation: []`、`volumeSnapshotLocation: []` 与默认插件）；或
2. 删除该版本后重新导入 `charts/velero-12.2.1.tgz`。

否则平台继续使用旧的默认配置，本次修订不会生效。
