# Cert-manager 镜像列表

对应 Chart：`cert-manager`

| 项 | 值 |
| --- | --- |
| Chart | [cert-manager](https://github.com/cert-manager/cert-manager/tree/master/deploy/charts/cert-manager) |
| Chart 版本 | **v1.21.3**（仓库文件：`charts/cert-manager-v1.21.3.tgz`） |
| appVersion | **v1.21.3** |
| 来源 | [jetstack](https://charts.jetstack.io)（官方 Helm 仓库） |
| Pixiu 默认调整 | 所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/`） |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。Chart 要求 Kubernetes >= 1.22（`kubeVersion` 约束），并默认安装 CRD（`crds.enabled` 由安装方式决定）。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| controller | `quay.io/jetstack/cert-manager-controller:v1.21.3` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/cert-manager-controller:v1.21.3` | 核心控制器 Deployment |
| cainjector | `quay.io/jetstack/cert-manager-cainjector:v1.21.3` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/cert-manager-cainjector:v1.21.3` | CA 注入器 Deployment |
| webhook | `quay.io/jetstack/cert-manager-webhook:v1.21.3` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/cert-manager-webhook:v1.21.3` | 准入 webhook（Deployment + Service） |
| startupapicheck | `quay.io/jetstack/cert-manager-startupapicheck:v1.21.3` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/cert-manager-startupapicheck:v1.21.3` | 安装后 API 校验 Job（helm install hook） |

## 默认不启用（可选）

| 组件 | 原生镜像 | 何时需要 |
| --- | --- | --- |
| acmesolver | `quay.io/jetstack/cert-manager-acmesolver:v1.21.3` | ACME HTTP-01 挑战时由 controller 动态创建挑战 Pod 使用；镜像引用通过 controller 启动参数 `--acme-http01-solver-image` 注入，取自本 chart `acmesolver.image`（本包已指向 mirror），**建议一并同步到 mirror**：`swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/cert-manager-acmesolver:v1.21.3` |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/jetstack/cert-manager-controller:v1.21.3
quay.io/jetstack/cert-manager-cainjector:v1.21.3
quay.io/jetstack/cert-manager-webhook:v1.21.3
quay.io/jetstack/cert-manager-startupapicheck:v1.21.3
quay.io/jetstack/cert-manager-acmesolver:v1.21.3
```

## 离线 / 私有仓库建议

1. 将上面的原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/`（保持 tag 不变）；
2. Chart 包内默认 values 已通过各组件 `image.repository` 整体覆盖指向 SWR mirror，离线环境开箱即用；
3. 若使用其他私有仓库，替换 `image.repository`、`cainjector.image.repository`、`webhook.image.repository`、`startupapicheck.image.repository`、`acmesolver.image.repository` 五处即可。

## 备注

- Chart v1.21.3 为 jetstack 官方仓库当前最新稳定版。
- acmesolver 镜像引用由 chart 通过 `--acme-http01-solver-image` 启动参数传给 controller，取自 `acmesolver.image.repository`（本包已覆盖为 SWR mirror），离线环境开启 ACME HTTP-01 前确保该镜像已在 mirror 中。

## 参考

- Chart 源码：<https://github.com/cert-manager/cert-manager/tree/master/deploy/charts/cert-manager>
- Cert-manager 项目：<https://github.com/cert-manager/cert-manager>
- Helm 仓库：`helm repo add jetstack https://charts.jetstack.io`
