# MySQL Operator 镜像列表

对应 Chart：`mysql-operator`

| 项 | 值 |
| --- | --- |
| Chart | [mysql-operator](https://github.com/mysql/mysql-operator) |
| Chart 版本 | **2.3.1**（仓库文件：`charts/mysql-operator-2.3.1.tgz`） |
| appVersion | **26.10.0-2.3.1**（对应 MySQL 26.10.0 / Operator 2.3.1） |
| 来源 | [mysql.github.io/mysql-operator](https://mysql.github.io/mysql-operator/)（Oracle 官方 Helm 仓库最新稳定版） |
| Pixiu 默认调整 | 镜像与实例默认镜像仓库均已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/mysql-operator/`） |

> 本 chart 只部署 **MySQL Operator** 本体（InnoDB Cluster 方案）。安装后通过 `InnoDBCluster` CR 创建 MySQL 实例；实例镜像（`community-server` + `community-operator` sidecar）由 Operator 按 `MYSQL_OPERATOR_DEFAULT_REPOSITORY` 注入的默认仓库解析，本包内 values 已指向 SWR mirror。

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| mysql-operator | `container-registry.oracle.com/mysql/community-operator:26.10.0-2.3.1` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/mysql-operator/community-operator:26.10.0-2.3.1` | Operator Deployment；创建 InnoDBCluster 后同镜像作为实例 sidecar |

## 创建实例后才会拉取（由 CR 触发）

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| mysql-server | `container-registry.oracle.com/mysql/community-server:26.10.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/mysql-operator/community-server:26.10.0` | InnoDBCluster 节点（StatefulSet），版本随 CR `spec.version`，Operator 默认用与 appVersion 一致的 server 版本 |

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
container-registry.oracle.com/mysql/community-operator:26.10.0-2.3.1
container-registry.oracle.com/mysql/community-server:26.10.0
```

## 离线 / 私有仓库建议

1. 将上面两个原生镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/mysql-operator/`（保持 tag 不变）；
2. Chart 包内 values 已做两处替换：
   - `image.registry` → SWR mirror（Operator 本体镜像）；
   - `envs.imagesDefaultRegistry` → SWR mirror（渲染为 Operator 容器环境变量 `MYSQL_OPERATOR_DEFAULT_REPOSITORY`，决定其创建的实例默认从哪个仓库解析 `community-server` / `community-operator`）；
3. 若 InnoDBCluster CR 显式指定 `podSpec.containers[*].image`，需保证该镜像也存在于目标集群可达仓库。

## 备注

- Chart 2.3.1 是 Oracle MySQL Operator 官方 Helm 仓库当前最新稳定版；MySQL Operator 基于 InnoDB Cluster（Group Replication），提供高可用、自动故障转移与滚动升级。
- 镜像来源为 Oracle Container Registry（container-registry.oracle.com），国内拉取慢/不稳定，私有化务必走 mirror。
- 安装本 chart 不会创建任何 MySQL 实例，需再提交 `InnoDBCluster` CR。
- Operator 默认集群级安装（RBAC 集群角色），单集群只装一套。

## 参考

- Chart 源码：<https://github.com/mysql/mysql-operator>
- 项目文档：<https://dev.mysql.com/doc/mysql-operator/en/>
- Helm 仓库：`helm repo add mysql-operator https://mysql.github.io/mysql-operator/`
