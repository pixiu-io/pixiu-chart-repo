# DOC-001 应用商店 Chart 添加说明

- **分类**：应用商店 / Chart 管理
- **涉及组件**：应用商店（charts / chart_versions）、Helm Chart 包、镜像仓库
- **最后更新**：2026-10-29

## 适用范围

- 给 Pixiu 应用商店上架新 Chart、发布新版本
- 上传 / 删除 Chart、修改平台默认配置仅 root/admin 可操作
- 当前仅支持**本地上传 .tgz**，不支持从 Chart 仓库 URL 导入
- `library` 类型 chart 不可安装，上传后会被拒绝

## 前置条件

- 操作账号为 root/admin
- 已产出 Helm Chart 打包产物 .tgz（Helm 3）
- 目标集群可访问 values 中配置的镜像仓库
- **打包工具**：默认使用 `helm package`（见下方标准流程）；禁止本机裸 `tar czf` 作为常规手段
- **macOS 打包环境**：须避免把 AppleDouble（`._*`）元数据打进包（见「打包卫生」）

## 标准流程（后续复用）

上架 / 合入本仓库 `charts/` 时，按下列顺序执行（可整段复制）：

```bash
# 0) 准备：上游拉取或本地 chart 目录
#    helm pull <repo>/<chart> --version <ver>   # 或 git clone / 已有目录
#    解压后修改 values（镜像改为 SWR mirror 等）

# 1) 依赖（有子 chart 时）
helm dependency build ./mychart

# 2) 打包 —— 标准方式：必须用 helm package
COPYFILE_DISABLE=1 helm package ./mychart
# 产物：./mychart-<version>.tgz

# 3) 自检（无 ._* / .DS_Store / __MACOSX，且 helm 可读）
python3 scripts/check-chart-tgz.py ./mychart-*.tgz
helm show chart ./mychart-*.tgz
helm template test ./mychart-*.tgz -n default >/dev/null

# 4) 归档到本仓库并补文档
mv ./mychart-*.tgz charts/
# 新增/更新 docs/<chart>-images.md、根 README 组件表、docs/README 索引
```

**为何规定用 `helm package`：**

| 方式 | 结论 |
| --- | --- |
| `COPYFILE_DISABLE=1 helm package ./chart` | **标准 / 默认**。不产生 `._*`；按 `Chart.yaml` 命名；带上 `charts/` 依赖；尊重 `.helmignore` |
| `helm pull` / OCI 拉取上游包 | 可作起点；**改完 values 后仍须再 `helm package` 一次**产出最终包 |
| 本机裸 `tar -czf` | **禁止作为常规流程**。macOS 易打入 AppleDouble，导致 Helm 报 `content outside the base directory` |

仅在无法使用 Helm 的例外场景才允许 `tar`，且必须：

```bash
xattr -cr ./mychart
find ./mychart \( -name '._*' -o -name '.DS_Store' \) -delete
COPYFILE_DISABLE=1 tar --exclude='._*' --exclude='.DS_Store' --exclude='__MACOSX' -czf mychart-x.y.z.tgz mychart
python3 scripts/check-chart-tgz.py ./mychart-x.y.z.tgz
```

## 操作步骤

### 1. 制作 Chart 包

- `Chart.yaml` 必须包含 `name`、`version`（Helm loader 会校验语义化版本）；建议同时填写 `appVersion`、`description`、`icon`（icon 会展示在商店卡片）
- `type` 必须为 `application` 或留空（留空视为 application）
- 依赖的子 chart 必须已打入包内 `charts/` 目录（`helm dependency build`），否则安装时会尝试联网拉取依赖，离线环境会失败
- 单包大小上限由 `appstore.max_upload_mb` 控制，默认 32MB，超限上传返回 413
- 包内 `values.yaml` 会在上传时被提取为「平台默认配置」的初始内容
- 打包命令见上方「标准流程」——**默认且优先：`helm package`**

### 1.1 打包卫生（禁止 macOS 元数据残留）

macOS 在复制到不支持 xattr 的介质、或用普通 `tar` 打包时，会生成 AppleDouble 兄弟文件（`._Chart.yaml`、`._velero` 等）。Helm `LoadArchive` 对无 `/` 的顶层条目（如 `._velero`）会报：

`chart illegally contains content outside the base directory`

**硬性要求（上架 / 合入本仓库 `charts/` 前必须满足）：**

1. 使用 `helm package` 产出最终 `.tgz`（例外见标准流程）
2. 包内不得包含：`._*`、`.DS_Store`、`__MACOSX/`
3. `helm show chart <file.tgz>` 必须成功
4. 用仓库脚本自检通过：`python3 scripts/check-chart-tgz.py charts/*.tgz`

**自检 / 清理命令：**

```bash
# 自检（有残留则非 0 退出）
python3 scripts/check-chart-tgz.py charts/*.tgz

# 发现残留后：过滤并用 helm package 重打（推荐）
python3 scripts/check-chart-tgz.py --fix charts/velero-12.2.1.tgz
```

### 2. 处理镜像（离线 / 私有仓必做）

- 将 values 中各组件 `image` 改为目标集群可达的私有仓库地址（离线部署需提前推送）
- 参考同目录镜像文档（如 [prometheus-images.md](./prometheus-images.md)、[velero-images.md](./velero-images.md)、[gpu-operator-images.md](./gpu-operator-images.md)、[ingress-nginx-images.md](./ingress-nginx-images.md)）的「mirror 镜像」列与「原生镜像」清单
- 验证：`helm template <包> -n <ns> | grep image:`，确认无上游不可达地址
- 改完 values 后按「标准流程」用 **`helm package` 重新打包**，不要只用 `tar` 盖回去

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

## 安装与验证实操（平台 API）

应用商店安装为**异步任务**：入队即返回，通过 installs 接口轮询结果。以下为实测有效流程（2026-10-29，console.cloud.pixiuio.com，集群 pixiu-fmqyrwig）。

### 登录获取 token（有效期约 1 小时）

```bash
TOKEN=$(curl -s -X POST https://console.cloud.pixiuio.com/pixiu/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"name":"admin","password":"<密码>"}' | python3 -c \
  'import sys,json;print(json.load(sys.stdin)["result"]["token"])')
```

后续请求统一带 `Authorization: Bearer $TOKEN`。

### 安装（异步）

```bash
CLUSTER=pixiu-fmqyrwig
curl -X POST "https://console.cloud.pixiuio.com/pixiu/apps/clusters/$CLUSTER/namespaces/pixiu-system/releases" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"chart_id": <ID>, "release_name": "loki", "version": "7.5.0", "values": { ... }}'
```

轮询状态：

```bash
curl -s "https://console.cloud.pixiuio.com/pixiu/apps/clusters/$CLUSTER/installs" \
  -H "Authorization: Bearer $TOKEN"
# deploy_status: pending → installing → success / failed（failed 时 message 有原因）
```

卸载：`DELETE .../namespaces/<ns>/releases/<release_name>`（异步；失败记录删除后可同名重装）。

集群内验证走平台 K8s 代理：`https://console.cloud.pixiuio.com/pixiu/proxy/$CLUSTER/api/v1/namespaces/<ns>/pods`。

### 平台级踩坑（多 chart 安装实测）

1. **chart 包文件丢失（`chart package not found: stat /etc/pixiu/appstore/charts/xxx.tgz`）**：后端多副本部署，DB 共享但 chart 目录是实例本地磁盘；上传落在 A 实例、安装任务由 B 实例执行时找不到文件。解决：**「删 Chart → 重传 → 重装」循环重试**，直到上传与任务执行落在同一实例。建议平台侧把 appstore data_dir 迁共享存储（NFS/S3/OSS）。
2. **Longhorn 卷 faulted（`precheck new replica failed: insufficient storage`）**：Longhorn 按**卷声明大小**做调度预检，不看实际占用。磁盘 39.3GiB、storageReserved 30%（11.8GiB）→ 可调度上限 27.5GiB；已有卷 + 新卷超限即 faulted，Pod 卡 `FailedAttachVolume`。解决：调低磁盘保留（PATCH `longhorn.io/v1beta2 .../nodes/<node>` 的 `spec.disks.<id>.storageReserved`），Longhorn 自动恢复。**单节点小磁盘装大容量应用前，先看可调度余量而不是剩余磁盘；新应用 PVC 5Gi 起步。**
3. **release 命名空间与实际部署不一致**：平台安装记录显示 `pixiu-system`（helm release secret 也在 pixiu-system），但部分 chart（elasticsearch、minio）的资源实际创建在 `default`。验证 Pod 时别只盯记录里的命名空间（`kubectl get sts -A`）。
4. **节点 requests 打满（`0/1 nodes are available: Insufficient memory`）**：实际用量可能很低，但各 Pod **requests 汇总**占满 allocatable 即调度失败。安装前核对 requests 余量；必要时压低应用 requests（注意 patch 的 requests 会被下次 helm upgrade 覆盖）。
5. **经 K8s 服务代理测 HTTPS 应用时 Authorization 头冲突**：`Authorization: Bearer` 头被 apiserver 消费，无法同时给后端应用传 Basic auth。解决：起一次性 Job（用集群内已有镜像）在集群内 curl 验证，再经代理读 Pod 日志取结果。

### 实测结果（loki / promtail / elasticsearch 三件套）

loki 的默认 values 与 Chart 级踩坑见 [loki-images.md](./loki-images.md)「应用商店安装实录」章节。三个应用均 deployed 且功能验证通过：Loki 网关查询正常并收到 promtail 日志流（push 204）；ES `_cluster/health` = green（https + basic auth）。

promtail 与 elasticsearch 安装时需传入的 values 实测参考：

```json
// promtail 6.17.1：Loki 多租户下必须带 tenant_id，否则推送 401 no org id
{"config": {"clients": [
  {"url": "http://loki-gateway/loki/api/v1/push", "tenant_id": "pixiu"}
]}}
```

```json
// elasticsearch 8.5.1：单节点瘦身（默认 3 副本 + 2C4G + 30Gi 在小规格集群装不下）
{"replicas": 1, "minimumMasterNodes": 1, "esJavaOpts": "-Xms512m -Xmx512m",
 "resources": {"requests": {"cpu": "200m", "memory": "512Mi"}, "limits": {"cpu": "1", "memory": "2Gi"}},
 "volumeClaimTemplate": {"resources": {"requests": {"storage": "5Gi"}}}}
```

> 后续将 values 层面的修复内化到了 loki Chart 默认值（SingleBinary + filesystem + schemaConfig + 5Gi，见 loki-images.md「Pixiu 默认调整」），新装 loki 已无需传自定义 values；**promtail、elasticsearch 保持上游默认 values**，按上方实测参考传 values。

## 验证方式

1. 本地：`python3 scripts/check-chart-tgz.py <包>`（无 `._*` / `.DS_Store` / `__MACOSX`）
2. 本地：`helm show chart <包>`、`helm lint <包>`、`helm template <包> -n <ns>` 通过
3. 上传后：应用商店列表出现该 chart，详情中版本、appVersion、大小、sha256 与本地包一致
4. 在测试集群安装（选集群 + 命名空间 + 版本），检查 Pod 状态与镜像地址是否为预期仓库
5. 离线验证：`helm template` 输出中无上游镜像地址

## 常见问题

| 现象 | 根因 | 解决方案 |
|---|---|---|
| `chart illegally contains content outside the base directory: "._xxx"` | 包内含 macOS AppleDouble（`._*`） | 用 `helm package` 重打，或 `scripts/check-chart-tgz.py --fix`；禁止裸 `tar czf` |
| `helm show chart` 失败 / 上传解析失败 | 同上，或包损坏 | 自检脚本 + 重打包 |
| 上传返回 400 `chart type "library" is not installable...` | `Chart.yaml` 为 library 类型 | 改为 application 或删除 `type` |
| 上传返回 400 `invalid chart archive` / `chart name and version are required` | 不是合法 Helm 3 包，或 `Chart.yaml` 缺 name/version | 用 `helm package` 重新打包并补全字段 |
| 上传返回 413 `chart package exceeds max size N MB` | 超过 `appstore.max_upload_mb` | 精简包（剔除无关文件）或调大配置 |
| 上传返回 409 `chart X version Y already exists` | 同版本重复 | 提升 `Chart.yaml` 的 version |
| 上传返回 409 `identical chart package already exists as version Z` | 包内容与历史版本完全相同（sha256 一致） | 确认是否改了内容；仅改版本号不算新包 |
| 安装报 `chart package not found: stat /etc/pixiu/appstore/charts/xxx.tgz` | 多副本后端 chart 目录为实例本地盘，上传与安装执行不在同一实例 | 「删 Chart → 重传 → 重装」循环重试；根治需迁共享存储 |
| Pod 卡 `FailedAttachVolume`，Longhorn 卷 `robustness=faulted`（insufficient storage） | Longhorn 按卷声明大小预检，可调度余量不足 | 调低节点磁盘 storageReserved；新应用 PVC 5Gi 起步 |
| 安装报 `0/1 nodes are available: Insufficient memory` | Pod requests 汇总占满 allocatable（与实际用量无关） | 压低应用 requests / 释放其它组件 requests / 扩节点 |
| 安装报 `an error occurred while checking for chart dependencies ...` | 子 chart 未打入 `charts/` | `helm dependency build` 后重新打包上传 |
| 安装后 Pod `ImagePullBackOff` | 镜像未推送到目标集群可达仓库 | 按 mirror 清单推送并修正 values |
| 删除返回 409 `has N in-flight install operation(s)` | 仍有进行中的任务 | 等待任务结束后重试 |

## 备注

- 平台默认配置按「版本」维度存储，不同版本可分别维护
- 存量版本若平台默认配置为空，安装时直接使用包内 values.yaml
- chart 包源文件维护在本仓库 `charts/` 目录，上架前先在此留档
- 本仓库 `charts/*.tgz` 合入前须通过 `python3 scripts/check-chart-tgz.py charts/*.tgz`
- 最终归档包统一由 **`helm package`** 产出；改 values / 清残留后同样用 `helm package` 重打，避免 `tar` 二次引入 `._*`
