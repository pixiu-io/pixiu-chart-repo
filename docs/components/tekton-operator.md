# Tekton Operator（tekton-operator）

> 分类：CI/CD　|　用途：以 Operator 方式在 Kubernetes 上安装、升级并管理 Tekton 全家族组件（Pipelines / Triggers / Chains / Results / Dashboard 等），为 Pixiu 提供云原生 CI/CD 能力。

| 项 | 值 |
| --- | --- |
| Chart | [tektoncd/operator](https://github.com/tektoncd/operator) |
| 仓库版本 | **0.82.0**（`charts/tekton-operator-0.82.0.tgz`） |
| appVersion | **v0.82.0** |
| 来源 | tektoncd/operator GitHub Releases 官方最新稳定 chart |
| 镜像清单 | [tekton-operator-images.md](../tekton-operator-images.md) |

## 版本

| Chart 版本 | appVersion | Chart 包 | 适用说明 |
|---|---|---|---|
| 0.82.0 | v0.82.0 | `charts/tekton-operator-0.82.0.tgz` | 官方最新稳定版；`kubernetesMinVersion` 下调至 v1.28.0 适配 Pixiu 1.28.x 集群 |

## 镜像

镜像已指向华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）。

Operator 通过 `TEKTON_REGISTRY_OVERRIDE` 把其安装的下游 Tekton 组件镜像统一改写为 SWR 前缀，便于离线/私有化部署。

## 部署前置条件

- Kubernetes 1.28 或更高；集群具备 cluster-admin 权限以安装 CRD 与 RBAC。
- 首次安装且集群无 Tekton CRD 时设置 `installCRDs: true`（默认 false），否则 webhook 会因 CRD 未就绪持续 CrashLoop。
- 按实际需要配置 `controllers`（默认安装 common + tektondashboard 全量组件），只需核心流水线时可裁剪。
- SWR 中需预先同步 operator 镜像及其下游组件镜像，详见镜像清单。

## 安装示例

```bash
helm install tekton-operator charts/tekton-operator-0.82.0.tgz \
  -n tekton-pipelines --create-namespace \
  --set installCRDs=true
```

## 验证方式

`kubectl get pods -n tekton-pipelines` 中 operator / webhook / webhook-proxy 均为 Running；`kubectl get tektonconfig` 出现 `config` 实例且状态 Ready；创建 TaskRun / PipelineRun 可正常调度执行。

## 备注

- Operator 采用 knative leader election，`operator.replicas` 设为 ≥2 可运行主备（避免重复写入）；
- `installCRDs: true` 在卸载 chart 时会级联删除所有 Tekton 资源，卸载前请先备份；
- 与 Pixiu 已上架的 kube-prometheus-stack 配套：设置 `service.createServiceMonitor=true` 后由 Prometheus Operator 抓取 webhook 指标。
