# Cert-manager（cert-manager）

> 分类：网络与安全　|　用途：在 Kubernetes 中自动签发、续期和管理 TLS 证书（含 ACME / Let's Encrypt）。

| 项 | 值 |
| --- | --- |
| Chart | [cert-manager](https://github.com/cert-manager/cert-manager/tree/master/deploy/charts/cert-manager) |
| 仓库版本 | **v1.21.3**（`charts/cert-manager-v1.21.3.tgz`） |
| appVersion | **v1.21.3** |
| 来源 | [jetstack](https://charts.jetstack.io)（官方 Helm 仓库） |
| 镜像清单 | [cert-manager-images.md](../cert-manager-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| v1.21.3 | v1.21.3 | `charts/cert-manager-v1.21.3.tgz` | 要求 Kubernetes ≥1.22（Chart `kubeVersion` 约束） |

## 镜像

所有镜像已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/cert-manager/`）。

默认拉取 controller、cainjector、webhook、startupapicheck 四个镜像；acmesolver 仅在开启 ACME HTTP-01 挑战时由 controller 动态创建挑战 Pod 使用，建议一并同步到 mirror。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| controller | `.../pixiu-public/cert-manager/cert-manager-controller:v1.21.3` | 核心控制器 Deployment |
| cainjector | `.../pixiu-public/cert-manager/cert-manager-cainjector:v1.21.3` | CA 注入器 Deployment |
| webhook | `.../pixiu-public/cert-manager/cert-manager-webhook:v1.21.3` | 准入 webhook（Deployment + Service） |
| startupapicheck | `.../pixiu-public/cert-manager/cert-manager-startupapicheck:v1.21.3` | 安装后 API 校验 Job（helm install hook） |
| acmesolver | `.../pixiu-public/cert-manager/cert-manager-acmesolver:v1.21.3` | 可选，ACME HTTP-01 挑战 Pod 使用 |

完整镜像明细见镜像清单。

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
quay.io/jetstack/cert-manager-controller:v1.21.3
quay.io/jetstack/cert-manager-cainjector:v1.21.3
quay.io/jetstack/cert-manager-webhook:v1.21.3
quay.io/jetstack/cert-manager-startupapicheck:v1.21.3
quay.io/jetstack/cert-manager-acmesolver:v1.21.3
```

## 安装说明

- 前置条件：Kubernetes ≥1.22（Chart `kubeVersion` 约束）。
- CRD 是否随包安装由安装方式决定（`crds.enabled`）。

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 开启 ACME HTTP-01 后挑战 Pod 镜像拉取失败 | acmesolver 镜像未同步到 mirror；该镜像通过 controller 启动参数 `--acme-http01-solver-image` 注入 | 将 `.../pixiu-public/cert-manager/cert-manager-acmesolver:v1.21.3` 推送到 SWR mirror |

## 相关链接

- [镜像清单](../cert-manager-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/cert-manager/cert-manager
