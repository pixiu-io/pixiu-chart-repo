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

## 默认不启用（可选）

| 组件 | 默认镜像 | mirror 镜像 | 何时需要 |
| --- | --- | --- | --- |
| node-agent | `docker.io/velero/velero:v1.18.2` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero:v1.18.2` | `deployNodeAgent=true`（与 Server 同镜像，DaemonSet） |
| kubectl（CRD cleanup Job） | `registry.k8s.io/kubectl:<k8s-version>` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/kubectl:<k8s-version>` | `cleanUpCRDs=true`（生产慎用）；tag 未设置时取集群 Kubernetes 版本 |
| velero-plugin-for-aws | `docker.io/velero/velero-plugin-for-aws:v1.13.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero-plugin-for-aws:v1.13.1` | `initContainers` 配置 AWS 对象存储 / 快照插件 |
| velero-plugin-for-gcp | `docker.io/velero/velero-plugin-for-gcp:<tag>` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero-plugin-for-gcp:<tag>` | 使用 GCP 备份存储时 |
| velero-plugin-for-microsoft-azure | `docker.io/velero/velero-plugin-for-microsoft-azure:<tag>` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/velero/velero-plugin-for-microsoft-azure:<tag>` | 使用 Azure 备份存储时 |

> 至少需要配置一个对象存储插件（`initContainers`），否则 Velero 无法完成真实备份；Chart 默认 `initContainers: []`，需在安装 values 中按云厂商补充。

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

1. 至少拉取「默认会拉取的镜像」并推送到私有镜像仓库；若开启 node-agent、CRD cleanup 或对象存储插件，再补可选表中对应镜像。  
2. 安装时通过 values 覆盖 `image.repository` / `image.tag`、`kubectl.image.repository` / `kubectl.image.tag`（或改 `initContainers[].image`）。  
3. Chart 包内已把默认镜像写成 SWR mirror，离线安装无需额外覆盖 Server / kubectl 仓库前缀；若使用其他私有仓库，需按表中 mirror 列整体替换。

## 参考

- Chart 源码：<https://github.com/vmware-tanzu/helm-charts/tree/main/charts/velero>  
- Velero 项目：<https://github.com/vmware-tanzu/velero>  
- Helm 仓库：`helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts`  
