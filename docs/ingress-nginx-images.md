# Ingress NGINX 镜像列表

对应 Chart：`ingress-nginx`

| 项 | 值 |
| --- | --- |
| Chart | [ingress-nginx](https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx) |
| Chart 版本 | **4.15.1**（仓库文件：`charts/ingress-nginx-4.15.1.tgz`） |
| appVersion | **1.15.1**（Ingress NGINX Controller） |
| 来源 | [kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx) |
| Pixiu 默认调整 | `global.image.registry` 与镜像路径已替换为华为云 SWR（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/ingress-nginx/`）；已清空 digest，按 tag 拉取 |

> 下列镜像按本仓库 Chart 包内 **默认 values** 整理。开启 defaultBackend / 额外模块或覆盖 `registry`/`image`/`tag` 后，实际拉取列表会变化。

## 默认会拉取的镜像

| 组件 | 镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| controller | `registry.k8s.io/ingress-nginx/controller:v1.15.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/ingress-nginx/controller:v1.15.1` | Ingress NGINX Controller |
| kube-webhook-certgen | `registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.9` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/ingress-nginx/kube-webhook-certgen:v1.6.9` | Admission Webhook 证书 Job（`controller.admissionWebhooks.patch.enabled=true`） |

## 默认不启用（可选）

| 组件 | 默认镜像 | mirror 镜像 | 何时需要 |
| --- | --- | --- | --- |
| defaultBackend | `registry.k8s.io/defaultbackend-amd64:1.5` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/ingress-nginx/defaultbackend-amd64:1.5` | `defaultBackend.enabled=true` |
| controller (chroot) | `registry.k8s.io/ingress-nginx/controller-chroot:v1.15.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/ingress-nginx/controller-chroot:v1.15.1` | `controller.image.chroot=true`（需另行推送 chroot 变体） |

## 原生镜像

上游原始镜像地址（含默认与可选组件），可直接批量 pull 后重新 tag / push 到私有仓库：

```text
registry.k8s.io/ingress-nginx/controller:v1.15.1
registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.9
registry.k8s.io/defaultbackend-amd64:1.5
registry.k8s.io/ingress-nginx/controller-chroot:v1.15.1
```

## 离线 / 私有仓库建议

1. 至少拉取「默认会拉取的镜像」并推送到私有镜像仓库。  
2. 安装时可通过 values 覆盖 `global.image.registry` 与各组件 `image` / `tag`。  
3. Chart 包内已写成 SWR mirror，离线安装无需额外改仓库前缀；若使用其他私有仓，按表中 mirror 列整体替换。

## 参考

- Chart 源码：<https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx>  
- Helm 仓库：`helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx`  
