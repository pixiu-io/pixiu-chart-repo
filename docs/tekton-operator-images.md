# Tekton Operator 镜像列表

对应 Chart：`tekton-operator`

| 项 | 值 |
| --- | --- |
| Chart | [tektoncd/operator](https://github.com/tektoncd/operator)（Tekton 官方仓库 `charts/tekton-operator`） |
| Chart 版本 | **0.82.0**（仓库文件：`charts/tekton-operator-0.82.0.tgz`） |
| appVersion | **v0.82.0** |
| 来源 | [tektoncd/operator GitHub Releases](https://github.com/tektoncd/operator/releases/tag/tekton-operator-0.82.0) 官方最新稳定 chart |
| Pixiu 默认调整 | 所有镜像替换为华为云 SWR mirror（`swr.cn-north-4.myhuaweicloud.com/pixiu-public/`，保留上游组织命名空间）；`kubernetesMinVersion` 下调至 v1.28.0 以适配目标集群 |

## 默认会拉取的镜像

| 组件 | 原生镜像 | mirror 镜像 | 说明 |
| --- | --- | --- | --- |
| Operator | `ghcr.io/tektoncd/operator/operator-303303c315a48490ba6517859ef65b77:v0.82.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/tektoncd/operator/operator-303303c315a48490ba6517859ef65b77:v0.82.0` | k8s 版本 operator 控制器 |
| Webhook | `ghcr.io/tektoncd/operator/webhook-f2bb711aa8f0c0892856a4cbf6d9ddd8:v0.82.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/tektoncd/operator/webhook-f2bb711aa8f0c0892856a4cbf6d9ddd8:v0.82.0` | operator webhook |
| Webhook Proxy | `ghcr.io/tektoncd/operator/proxy-webhook-f6167da7bc41b96a27c5529f850e63d1:v0.82.0` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/tektoncd/operator/proxy-webhook-f6167da7bc41b96a27c5529f850e63d1:v0.82.0` | `IMAGE_PIPELINES_PROXY` 注入 |
| Pruner (tkn) | `ghcr.io/tektoncd/plumbing/tkn:v20240913-fb9957bd48` | `swr.cn-north-4.myhuaweicloud.com/pixiu-public/tektoncd/plumbing/tkn:v20240913-fb9957bd48` | `IMAGE_JOB_PRUNER_TKN` 注入 |

> Operator 通过 `TEKTON_REGISTRY_OVERRIDE`（values.registry）把其安装的全部 Tekton 组件镜像（Pipelines / Triggers / Chains / Results / Dashboard 等）统一改写为 SWR 前缀。这些下游组件镜像由 operator 运行时按 override 拼接，**不在本 chart 的渲染产物中**，需按实际启用的组件批量同步到 SWR 对应命名空间。

## 原生镜像

上游原始镜像地址，可直接批量 pull 后重新 tag / push 到私有仓库：

```text
ghcr.io/tektoncd/operator/operator-303303c315a48490ba6517859ef65b77:v0.82.0
ghcr.io/tektoncd/operator/webhook-f2bb711aa8f0c0892856a4cbf6d9ddd8:v0.82.0
ghcr.io/tektoncd/operator/proxy-webhook-f6167da7bc41b96a27c5529f850e63d1:v0.82.0
ghcr.io/tektoncd/plumbing/tkn:v20240913-fb9957bd48
```

## 离线 / 私有仓库建议

1. 将上面 4 个 operator 镜像 push 到 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/tektoncd/` 对应路径，tag 保持不变；tkn 使用语义 tag `v20240913-fb9957bd48`（其内容与官方 chart 原锁定的 digest `sha256:233de6c8...` 完全一致）；
2. 按 `controllers` 启用的组件，同步 Tekton 下游镜像（Pipelines / Triggers / Chains 等）到 SWR，路径规则为 `swr.cn-north-4.myhuaweicloud.com/pixiu-public/<原路径去掉 host>`；
3. Chart 包内 values 已做镜像地址替换，`helm template` 渲染验证全部指向 SWR；
4. 若集群无 Tekton CRD，需保持 `installCRDs: true`（首次安装），否则 webhook 会因 CRD 未就绪而 CrashLoop。

## 备注

- `kubernetesMinVersion` 默认为 v1.34.0（该 operator 版本 vendored 的 knative/pkg 最低要求），Pixiu 包下调为 v1.28.0 以适配 1.28.x 集群；生产集群若版本 ≥1.34 可按需调回。
- `installCRDs` 默认 false；卸载 chart 时设为 true 会级联删除所有 Tekton 资源，需谨慎。
