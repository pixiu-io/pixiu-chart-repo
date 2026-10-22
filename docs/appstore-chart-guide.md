# DOC-001 应用商店 Chart 添加说明

- **分类**：应用商店 / Chart 管理
- **涉及组件**：应用商店（charts / chart_versions）、Helm Chart 包、镜像仓库
- **最后更新**：2026-10-22

## 适用范围

- 给 Pixiu 应用商店上架新 Chart、发布新版本
- 上传 / 删除 Chart、修改平台默认配置仅 root/admin 可操作
- 当前仅支持**本地上传 .tgz**，不支持从 Chart 仓库 URL 导入
- `library` 类型 chart 不可安装，上传后会被拒绝

## 前置条件

- 操作账号为 root/admin
- 已产出 Helm Chart 打包产物 .tgz（Helm 3）
- 目标集群可访问 values 中配置的镜像仓库

## 操作步骤

### 1. 制作 Chart 包

- `Chart.yaml` 必须包含 `name`、`version`（Helm loader 会校验语义化版本）；建议同时填写 `appVersion`、`description`、`icon`（icon 会展示在商店卡片）
- `type` 必须为 `application` 或留空（留空视为 application）
- 依赖的子 chart 必须已打入包内 `charts/` 目录（`helm dependency build`），否则安装时会尝试联网拉取依赖，离线环境会失败
- 单包大小上限由 `appstore.max_upload_mb` 控制，默认 32MB，超限上传返回 413
- 包内 `values.yaml` 会在上传时被提取为「平台默认配置」的初始内容
- 打包示例：`helm dependency build ./mychart && helm package ./mychart`

### 2. 处理镜像（离线 / 私有仓必做）

- 将 values 中各组件 `image` 改为目标集群可达的私有仓库地址（离线部署需提前推送）
- 参考同目录镜像文档（如 [prometheus-images.md](./prometheus-images.md)、[velero-images.md](./velero-images.md)、[gpu-operator-images.md](./gpu-operator-images.md)）的「mirror 镜像」列与「原生镜像」清单
- 验证：`helm template <包> -n <ns> | grep image:`，确认无上游不可达地址

### 3. 上传到应用商店

- 页面：应用商店 → 右上角「上架应用」→ 选择「分类」（可选）+ 拖入 .tgz → 确定
- 分类可选值（前端下拉）：可观测性、网络、安全、数据库、存储、CI/CD、镜像仓库、服务网格
- 接口（等价）：`POST /pixiu/apps/charts`，`multipart/form-data`，字段 `file`（.tgz）、`category`（可选）
- 后端行为：
  - 解析包并校验 name/version、类型；失败返回 400
  - 同名同版本已存在 → 409；包内容 sha256 与任一历史版本相同 → 409（即使改了版本号）
  - 新 chart 以包内 name 建目录项；同名 chart 再上传不同版本即追加版本，并更新 `latest_version`
  - 包体存储到 `appstore.data_dir/charts/<name>-<version>.tgz`
  - 同一次上传会把包内 values.yaml 原文写入该版本的平台默认配置

### 4. 维护平台默认配置

- 入口：应用商店 → 点开 chart 详情 → 默认配置编辑区（弹窗标题「编辑默认配置」），需 root/admin
- 「恢复默认」会用包内 values.yaml 覆盖平台默认配置（二次确认后执行）
- 安装时的值合并优先级：**用户在安装表单填写的值 > 平台默认配置 > chart 内置 values.yaml**；数组合并规则为整体替换
- 升级时的值合并优先级：**本次请求值 > 当前 release 的 values > 平台默认配置**

### 5. 发布新版本

- 修改 `Chart.yaml` 的 `version`（同一 chart 版本号不能重复），重新打包、上传同一个 name
- 上传成功后 `latest_version` 更新；已有安装可在应用商店对 release 执行升级，并选择目标版本
- 升级使用上面「升级」的合并优先级

### 6. 删除 Chart

- 需 root/admin；存在进行中的安装/升级/卸载任务时拒绝删除（409）
- 删除会移除该 chart 的所有版本记录与存储中的包文件

## 验证方式

1. 本地：`helm lint <包>` 与 `helm template <包> -n <ns>` 渲染通过
2. 上传后：应用商店列表出现该 chart，详情中版本、appVersion、大小、sha256 与本地包一致
3. 在测试集群安装（选集群 + 命名空间 + 版本），检查 Pod 状态与镜像地址是否为预期仓库
4. 离线验证：`helm template` 输出中无上游镜像地址

## 常见问题

| 现象 | 根因 | 解决方案 |
|---|---|---|
| 上传返回 400 `chart type "library" is not installable...` | `Chart.yaml` 为 library 类型 | 改为 application 或删除 `type` |
| 上传返回 400 `invalid chart archive` / `chart name and version are required` | 不是合法 Helm 3 包，或 `Chart.yaml` 缺 name/version | 用 `helm package` 重新打包并补全字段 |
| 上传返回 413 `chart package exceeds max size N MB` | 超过 `appstore.max_upload_mb` | 精简包（剔除无关文件）或调大配置 |
| 上传返回 409 `chart X version Y already exists` | 同版本重复 | 提升 `Chart.yaml` 的 version |
| 上传返回 409 `identical chart package already exists as version Z` | 包内容与历史版本完全相同（sha256 一致） | 确认是否改了内容；仅改版本号不算新包 |
| 安装报 `an error occurred while checking for chart dependencies ...` | 子 chart 未打入 `charts/` | `helm dependency build` 后重新打包上传 |
| 安装后 Pod `ImagePullBackOff` | 镜像未推送到目标集群可达仓库 | 按 mirror 清单推送并修正 values |
| 删除返回 409 `has N in-flight install operation(s)` | 仍有进行中的任务 | 等待任务结束后重试 |

## 备注

- 平台默认配置按「版本」维度存储，不同版本可分别维护
- 存量版本若平台默认配置为空，安装时直接使用包内 values.yaml
- chart 包源文件维护在本仓库 `charts/` 目录，上架前先在此留档
