# Ingress NGINX（ingress-nginx）

> 分类：网络与安全　|　用途：Kubernetes 集群入口控制器，为 Service 提供 HTTP/HTTPS 反向代理与 Ingress 路由。

| 项 | 值 |
| --- | --- |
| Chart | [ingress-nginx](https://github.com/kubernetes/ingress-nginx/tree/main/charts/ingress-nginx) |
| 仓库版本 | **4.15.1**（`charts/ingress-nginx-4.15.1.tgz`） |
| appVersion | **1.15.1** |
| 来源 | [kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx)（社区官方 Helm 仓库） |
| 镜像清单 | [ingress-nginx-images.md](../ingress-nginx-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 4.15.1 | 1.15.1 | `charts/ingress-nginx-4.15.1.tgz` | 当前仓库收录版本，Ingress NGINX Controller 1.15.1 |

## 镜像

`global.image.registry` 与镜像路径已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/ingress-nginx/`），并清空 digest、按 tag 拉取。

默认拉取 controller 与 kube-webhook-certgen 两个镜像；defaultBackend 与 controller-chroot 变体默认不启用，开启后实际拉取列表会变化。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| controller | `.../pixiu-public/ingress-nginx/controller:v1.15.1` | Ingress NGINX Controller，默认拉取 |
| kube-webhook-certgen | `.../pixiu-public/ingress-nginx/kube-webhook-certgen:v1.6.9` | Admission Webhook 证书 Job，默认拉取 |
| defaultBackend | `.../pixiu-public/ingress-nginx/defaultbackend-amd64:1.5` | 可选，`defaultBackend.enabled=true` 时拉取 |
| controller-chroot | `.../pixiu-public/ingress-nginx/controller-chroot:v1.15.1` | 可选，`controller.image.chroot=true` 时使用 |

完整镜像明细见镜像清单。

## 原生镜像

上游原始镜像地址（含默认与可选组件），可直接批量 pull 后重新 tag / push 到私有仓库：

```text
registry.k8s.io/ingress-nginx/controller:v1.15.1
registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.9
registry.k8s.io/defaultbackend-amd64:1.5
registry.k8s.io/ingress-nginx/controller-chroot:v1.15.1
```

## 安装说明

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

暂无已记录的常见问题。

## 相关链接

- [镜像清单](../ingress-nginx-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/kubernetes/ingress-nginx
