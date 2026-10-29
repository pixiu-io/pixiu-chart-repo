# MySQL Operator（mysql-operator）

> 分类：数据库与中间件　|　用途：基于 InnoDB Cluster 的 MySQL Operator，负责 MySQL 高可用实例的创建、故障转移与滚动升级。

| 项 | 值 |
| --- | --- |
| Chart | [mysql-operator](https://github.com/mysql/mysql-operator) |
| 仓库版本 | **2.3.1**（`charts/mysql-operator-2.3.1.tgz`） |
| appVersion | **26.10.0-2.3.1** |
| 来源 | [mysql.github.io/mysql-operator](https://mysql.github.io/mysql-operator/)（Oracle 官方 Helm 仓库最新稳定版） |
| 镜像清单 | [mysql-operator-images.md](../mysql-operator-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 2.3.1 | 26.10.0-2.3.1 | `charts/mysql-operator-2.3.1.tgz` | 对应 MySQL 26.10.0 / Operator 2.3.1，基于 InnoDB Cluster |

## 镜像

镜像与实例默认镜像仓库均已替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/mysql-operator/`）。

本 Chart 只部署 MySQL Operator 本体；实例镜像（community-server + community-operator sidecar）在创建 `InnoDBCluster` CR 后由 Operator 按 `MYSQL_OPERATOR_DEFAULT_REPOSITORY` 注入的默认仓库解析，本包内 values 已指向 SWR mirror。

| 组件 | mirror 镜像 | 说明 |
|---|---|---|
| mysql-operator | `.../pixiu-public/mysql-operator/community-operator:26.10.0-2.3.1` | Operator Deployment；创建 InnoDBCluster 后同镜像作为实例 sidecar |
| mysql-server | `.../pixiu-public/mysql-operator/community-server:26.10.0` | InnoDBCluster 节点（StatefulSet），由 CR 触发拉取 |

完整镜像明细见镜像清单。

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
container-registry.oracle.com/mysql/community-operator:26.10.0-2.3.1
container-registry.oracle.com/mysql/community-server:26.10.0
```

## 安装说明

- 本 Chart 只部署 MySQL Operator 本体，安装后需再提交 `InnoDBCluster` CR 才会创建 MySQL 实例。
- Operator 默认集群级安装（RBAC 集群角色），单集群只装一套。

> 暂无安装实录，可直接按应用商店默认配置安装；Chart 上架与打包规范见 [appstore-chart-guide.md](../appstore-chart-guide.md)。

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 拉取 community-server / community-operator 镜像慢或失败 | 镜像来源为 Oracle Container Registry（container-registry.oracle.com），国内访问慢且不稳定 | 使用 Chart 包内已配置的 SWR mirror 前缀，或整体替换为可用的私有仓库 |

## 相关链接

- [镜像清单](../mysql-operator-images.md)
- [上架与打包规范](../appstore-chart-guide.md)
- [返回组件列表](../../README.md)
- 上游：https://github.com/mysql/mysql-operator
