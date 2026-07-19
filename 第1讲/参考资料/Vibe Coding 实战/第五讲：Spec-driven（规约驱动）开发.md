> **本讲目标：** 掌握 Speckit 的核心概念与标准工作流（`constitution → specify → clarify → plan → tasks → analyze → implement`），能够独立完成一次“从规约到实现”的开发闭环。

> 

> **预计时长：** 60 分钟

> 

> **难度等级：** 技能

## 自学导航卡

- **前置依赖：** 已能使用 AI 进行基础代码生成，理解需求、方案、任务三者关系

- **预计耗时：** 新手 60-90 分钟｜有经验 40-60 分钟

- **完成标准：** 至少完整执行 1 次 Speckit 全流程，并完成 1 次 `analyze` 一致性检查

- **卡点入口：** 若流程过长，先用“小功能快路径”练习（`plan → tasks → implement`），再补全完整链路

<img src='images/5-1.png' width=600px />

在 AI 编程中，最常见的不是“写不出代码”，而是“写得不稳定”：

1. **需求与实现脱节**：需求说了一套，代码做了另一套。

2. **多人协作风格混乱**：每个人提示词不同，产出像“拼接工程”。

3. **结果不可复现**：同样需求，不同时间生成结果差异很大。

Speckit 的本质不是“又一个命令”，而是把开发流程从：

- **直接让 AI 写代码**（快，但容易失控）

升级为

- **先写规约，再让 AI 按规约执行**（可控、可审计、可复现）

<div style="padding: 10px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px; margin: 10px 0;">

一句话：<strong>Speckit 是 AI 时代的工程化“护栏系统”。</strong>

</div>



## 一、规约驱动（Spec-driven）

先定义清楚“要做什么、不能做什么、验收标准是什么”，再进入实现。规约不只是文档，而是后续生成代码、任务拆解、质量检查的**源头依据**。

在规约驱动下：维护软件 = 维护规约（不是维护代码）、调试 = 修复规约（不是修复代码）、重构 = 重构规约（代码自动重新生成）流程变化：

<img src='images/5-3.png' width=800px />

<img src='images/5-4.png' width=800px />

## 二、Constitution（项目宪法）

项目最高原则，决定技术和质量底线，例如：

- 是否允许云端存储

- 测试覆盖最低要求

- UI/语言规范（如全中文）

- 安全与性能优先级

它的作用是：**防止 AI 在关键决策上“自由发挥”。**

## 三、“先规划后施工”闭环

<img src='images/5-2.png' width=800px />

| 命令 | 作用 | 产出 |

|---|---|---|

| `/speckit.constitution` | 定义项目不可协商原则 | `constitution.md` |

| `/speckit.specify` | 用业务语言写需求（WHAT） | `spec.md` |

| `/speckit.clarify` | 对模糊点提问并补齐边界 | 更新后的 `spec.md` |

| `/speckit.plan` | 生成技术方案（HOW） | `plan.md` / 数据模型等 |

| `/speckit.tasks` | 任务拆解与执行顺序 | `tasks.md` |

| `/speckit.analyze` | 检查 spec/plan/tasks 一致性 | 分析报告 |

| `/speckit.implement` | 按任务顺序落地代码 | 可运行代码 |

强调：

- `specify` 阶段只谈需求，不抢跑到实现细节。

- `clarify` 虽可选，但强烈建议执行。

- `analyze` 是“返工预防器”，尤其适合中大型项目。

当前 CodeBuddy IDE  和 CodeBuddy Code 都已支持 Spec-kit ，通过自定义指令 / 能力实现 Spec Coding，如下为快速入门上手，可根据需要进行选择对应的 CodeBuddy  形态工具使用。

## 一、环境准备

<!-- 信息提示（蓝色） -->

<div style="padding: 10px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px; margin: 10px 0;">

<strong>环境已配备，无需再次操作</strong>

</div>

1. 安装 CodeBuddy IDE 或 CodeBuddy Code

```bash
# 安装 codebuddy-code 依赖 node  和 npm，可通过下面指令安装

https://nodejs.org/en/download/



# 安装 codebuddy-code，通过 iOA  登录，如无权限或未识别 iOA，腾讯用户选择 sso，输入 tencent 即可

https://copilot.tencent.com/ide/



#  本地终端安装

codebuddy-code npm install -g @tencent-ai/codebuddy-code
```

2. 在 Unix 系统中终端执行命令安装 Specify CLI

```bash
# 方式 1：持久化安装（推荐）

uv tool install specify-cli --from git+https://github.com/github/spec-kit.git 

# 方式 2：一次性使用

uvx --from git+https://github.com/github/spec-kit.git specify init my-project
```

<img src='images/5-5.png' width=600px />

3. 选择工具：以 CodeBuddy 为例进行选择和 Enter 确认

<img src='images/5-6.png' width=600px />

<br/>

<img src='images/5-7.png' width=600px />

## 二、初始化项目

<div style="padding: 10px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px; margin: 10px 0;">

<strong>开始实操</strong>

</div>

```bash
# 使用 CodeBuddy 进行项目初始化

specify init my-project
```

初始化过程，主要执行如下步骤：主要是下载模版安装包、解压和 Git  仓库初始化

<img src='images/5-8.png' width=600px />

初始化后提供一些命令， 输入 CodeBuddy ，即在 CodeBuddy Code中 使用了

<img src='images/5-9.png' width=600px />

初始项目之后，可以看到主要创建一下文件

<img src='images/5-10.png' width=200px />

## 标准化的开发流程

完成项目初始化之后，我们可以使用这个模板来进行标准化开发，主要有以下七个步骤。

| 步骤环节 | 角色/视角 | 核心目的 | 关键产出 | 实践建议 |

|---------|----------|---------|---------|---------|

| 1. 制定宪法 | 项目创始人 | 为项目建立最高准则，奠定所有技术决策的基石 | .specify/memory/constitution.md | 将团队技术栈偏好、部署要求、第三方库选用原则等写入宪法，约束AI的技术方案 |

| 2. 创建功能规范 | 产品经理 | 用自然语言清晰定义"做什么"，描述功能、用户故事和验收标准，不涉及技术实现 | specs/[功能名]/spec.md | 描述越具体越好，例如"按钮点击后，任务项变灰并移至底部"，而非笼统的"用户可以完成任务" |

| 3. 澄清需求 | 测试人员/产品经理（可选） | 消除 spec 中的模糊地带和歧义，通过提问来完善需求 | 对 spec.md 的补充和修正 | 强制自己在编码前想清楚所有边界情况和异常流程，有效减少后期返工 |

| 4. 生成技术方案 | 架构师 | 基于宪法和规范，设计"怎么做"，包括技术选型、架构设计、数据模型、API契约等 | plan.md、data-model.md 等设计文档 | 如果AI的方案（如库的选择）不符合预期，可以直接要求修改，你拥有最终决策权 |

| 5. 分析计划 | 审查者（可选） | 在分派任务前进行"沙盘推演"，检查所有工件（spec, plan）是否存在矛盾或遗漏 | 一份指出潜在问题的分析报告 | 强烈建议不要跳过。它像代码审查一样，能在早期发现许多高成本的错误 |

| 6. 生成任务列表 | 项目经理 | 将技术方案分解为详细、可执行、有依赖关系的具体施工步骤 | tasks.md | tasks.md 是与AI协作的核心界面。你可以随时介入，手动调整优先级或标记任务 |

| 7. 执行实现 | 程序员 | 根据任务列表，按顺序、有条不紊地执行开发任务，生成最终代码 | 可运行的应用程序代码 | 对于复杂任务，建议让AI一个一个地执行，以便随时检查每一步的产出，确保过程可控 |

### 1️⃣ /speckit.constitution：制定项目标准

```bash
命令：/speckit.constitution

作用：创建项目的"宪法"，这些原则和指南会指导所有后续的开发工作。
```

**示例输入：**以新项目为例

```bash
/speckit.constitution 这是一个 Nextjs 框架的问卷调研系统

 AI 生成的原则示例：- 所有数据只存本地，采用 Mock 的方式，不上传云端，计算过程透明- 面向普通用户，交互简单直观- 每个功能都能独立测试、渐进上线
```

<!-- 信息提示（蓝色） -->

<div style="padding: 10px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px; margin: 10px 0;">

<strong>这里优先给出两种操作方法，后续将只给出任意一个对话示例</strong>

</div>

<details style="margin-bottom: 8px;">

<summary style="color: #f57c00; font-weight: 500; cursor: pointer;">第一种：插件对话</summary>

<img src='images/5-11.png' width=800px />

</details>

<details style="margin-bottom: 8px;">

<summary style="color: #f57c00; font-weight: 500; cursor: pointer;">第二种：Code 对话</summary>

<img src='images/5-12.png' width=800px />

</details>

> PS: 如果是存量业务系统，可以直接输入 /constitution  使用 AI 进行生成。

### 2️⃣ /speckit.specify：说明项目功能

```bash
命令：/speckit.specify

作用：输出产品需求文档（PRD）

核心原则：只描述"要什么"，不讨论"怎么实现"
```

**示例输入：**

```markdown
/speckit.specify 我要做一个问卷系统。 

参考腾讯问卷，至少支持问卷新建、删除。

UI 设计要有活力感一点。

当完成问卷生成后，给一个大大的鼓励动画。
```

### 3️⃣ /speckit.clarify：补充说明（可选）

如果发现还有遗漏，可以使用`/speckit.clarify`命令让AI向我们询问相关细节的处理，将需求细节打磨完善。每个`spec.md`文件里都有一个`Review Checklist`，可以用来检查AI的交付物是否满足预期。

```bash
命令：/speckit.clarify

作用：Spec-Kit 开始针对需求不明确的点，向我们提问

无需额外输入，直接执行即可
```

**示例输入：**

```markdown
/speckit.specify 进行需求澄清，有无不足或未考虑到的地方
```

执行`/clarify`  后，执行后会提出五个问题，我们按自己的需求回答清楚就好。

### 4️⃣ /speckit.plan：定义技术方案

```bash
命令：/speckit.plan

作用：基于需求写技术方案和实施计划

无需额外输入，直接执行：
```

基于上述需求澄清，接下来执行生成项目实施计划

**示例输入：**

```markdown
/speckit.plan 执行
```

### 5️⃣ /speckit.tasks：制定任务列表

完成项目标准、需求分析和技术方案的编写之后，使用命令`/speckit.tasks`来让AI计划一份任务列表，指导接下来的开发流程。

```bash
命令：/tasks 

作用：拆解任务，分析 spec.md 和 plan.md、按阶段（Phase）拆解为多个子任务、每个任务包含明确的验收标准、估算完成时间

基于需求和技术方案，拆解出具体的任务无需额外输入，直接执行
```

**示例输入：**

```markdown
/speckit.tasks - 生成详细任务列表
```

### 6️⃣ /speckit.analyze：分析检查（可选）

使用`/speckit.analyze`命令，让AI检查一遍规范、计划、任务是否一致，提前发现并解决可能存在的问题。

```bash
命令：/analyze

作用：将所有文档全部审核一遍,检测 spec.md、plan.md 和 tasks.md 之间的不一致性、重复、歧义和欠指定项，将有问题的点全部找出来，生成报告并协助修复。

场景：通过前面这几步可以看到 spec-kit 已经给我们生成了茫茫多的文档。很难保证这些文档完全没有问题

无需额外输入
```

**示例输入：**

```markdown
/analyze  进行全面分析
```

### 7️⃣ /speckit.implement：开始构建项目

如果还有需要修改的地方，可以让Claude Code继续修改spec的文档。最后使用命令`/speckit.implement`,AI就会根据刚才的任务列表来编写代码，完成项目的开发。

```bash
命令：/implement

作用：开始写需求代码

使用方式： /implement ，AI 会按顺序执行 tasks.md 中的每个任务、每执行完一个任务 spec-kit 都会到我们的 task 文档里边打个勾、遇到测试失败会自动修复，最后所有任务完成后提示用户
```

**示例输入：**

```markdown
/speckit.implement  开始写代码
```

### 8️⃣ 最后运行项目，验收结果即可

## Step 1：制定宪法（Constitution）

- **你要输入：** 项目底线规则（质量、风格、安全、边界）

- **系统产出：** `constitution.md`

- **验收标准：** 至少 5 条“可检查”的规则（不是口号）

- **不通过就这样改：** 把“代码要规范”改为“必须通过 ESLint 且无 error”这类可执行描述

## Step 2：创建功能规约（Specify）

- **你要输入：** 用户要完成的任务、场景、结果（只写 WHAT）

- **系统产出：** `spec.md`

- **验收标准：** 包含主流程、边界条件、异常场景

- **不通过就这样改：** 删除技术实现细节，改写为“用户行为 + 系统反馈”

## Step 3：澄清需求（Clarify）

- **你要输入：** 对关键问题的明确回答（默认值、边界、冲突优先级）

- **系统产出：** 补全后的 `spec.md`

- **验收标准：** 关键歧义问题已关闭（如空值、排序、删除策略）

- **不通过就这样改：** 对每个问题给出“明确规则 + 示例”

## Step 4：生成技术方案（Plan）

- **你要输入：** 技术偏好、约束条件、非功能要求（性能/可维护性）

- **系统产出：** `plan.md`（可含数据模型、接口草案）

- **验收标准：** 方案能完整覆盖 `spec.md` 的核心需求

- **不通过就这样改：** 先补齐缺失模块，再重跑 `plan`

## Step 5：生成任务清单（Tasks）

- **你要输入：** 按实现顺序的拆解要求

- **系统产出：** `tasks.md`

- **验收标准：** 每个任务都有目标与完成判定，且可按顺序执行

- **不通过就这样改：** 拆分过大的任务，补上验收动作

## Step 6：一致性检查（Analyze）

- **你要输入：** 对 `spec / plan / tasks` 做一致性分析

- **系统产出：** 冲突/遗漏分析结果

- **验收标准：** 无重大冲突（需求缺失、方案冲突、任务覆盖不足）

- **不通过就这样改：**

- 需求冲突：回改 `spec.md`

- 技术不可行：回改 `plan.md`

- 任务覆盖不足：重生 `tasks.md`

## Step 7：自动实现（Implement）

- **你要输入：** 按任务顺序执行实现

- **系统产出：** 可运行代码

- **验收标准：** 主流程可演示，关键边界可验证

- **不通过就这样改：** 回到对应上游文档修正后再实现

## 一、需求目标

- 新增任务（标题+描述）

- 删除任务

- 标记完成

- 状态筛选

- LocalStorage 持久化

## 二、宪法要点

- 中文界面

- 不使用“AI 味”泛滥的蓝紫渐变

- 代码风格统一（Lint/Format）

- 基础测试必须存在

## 三、执行路径

`constitution → specify → clarify → plan → tasks → analyze → implement`

## 四、验收清单

- 功能完整可用

- 刷新后数据不丢

- 文案与交互符合宪法

- 无关键流程报错

## 五、详细操作步骤

### Step 0:项目初始化

```bash
# 在工作目录下初始化项目

specify init todo-app
```

执行后选择使用 `CodeBuddy` 作为开发工具，按 Enter 确认。

---

### Step 1:制定宪法

使用 `/speckit.constitution` 命令为项目建立最高准则。

**示例输入：**

```bash
/speckit.constitution 这是一个任务清单管理系统
```

**AI 生成的原则示例：**

```
- 中文界面，所有文案使用简体中文

- 不使用"AI 味"泛滥的蓝紫渐变，采用清新简洁的设计风格

- 代码风格统一，配置 Lint/Format 工具

- 基础测试必须存在，确保核心功能稳定

- 纯前端实现，使用 LocalStorage 持久化数据
```

---

### Step 3:创建功能规范

使用 `/speckit.specify` 命令详细描述需求，只说"要什么"，不讨论"怎么实现"。

**示例输入：**

```markdown
/speckit.specify 我要做一个任务清单应用，包含以下功能：



1. 新增任务：支持输入任务标题和详细描述

2. 删除任务：可以删除不需要的任务

3. 标记完成：点击可切换任务的完成状态

4. 状态筛选：可按"全部/未完成/已完成"筛选任务显示

5. 数据持久化：使用 LocalStorage 保存数据，刷新页面后数据不丢失



UI 要求：

- 界面简洁清新，避免使用蓝紫渐变

- 任务列表清晰易读

- 操作按钮直观易用
```

---

### Step 4:澄清需求（可选）

如果发现还有遗漏或模糊的地方，使用 `/speckit.clarify` 命令让 AI 提问。

**示例输入：**

```bash
/speckit.clarify 进行需求澄清
```

执行后 AI 会提出相关问题，如：

- 任务描述是否必填？

- 删除任务是否需要确认弹窗？

- 完成状态切换是否需要动画效果？

根据实际需求回答这些问题。

---

### Step 5:生成技术方案

使用 `/speckit.plan` 命令，让 AI 基于宪法和规范设计技术方案。

**示例输入：**

```bash
/speckit.plan 执行
```

AI 会输出包含以下内容的技术方案：

- 技术选型（如 React + TypeScript）

- 项目结构设计

- 数据模型定义（Task 接口设计）

- 状态管理方案

- LocalStorage 存储策略

- 组件拆分方案

---

### Step 6:生成任务列表

使用 `/speckit.tasks` 命令，将技术方案拆解为可执行的具体任务。

**示例输入：**

```bash
/speckit.tasks 生成详细任务列表
```

AI 会生成类似以下的任务列表：

- **Phase 1**: 项目搭建

- 初始化项目结构

- 配置 ESLint/Prettier

- 创建基础组件

- **Phase 2**: 核心功能

- 实现任务数据模型

- 实现新增任务功能

- 实现删除任务功能

- 实现标记完成功能

- 实现状态筛选功能

- **Phase 3**: 数据持久化

- 实现 LocalStorage 存储逻辑

- 实现数据读取与同步

- **Phase 4**: 测试与优化

- 编写单元测试

- UI 细节调整

- 代码审查与优化

---

### Step 7:分析检查（可选）

使用 `/speckit.analyze` 命令，让 AI 检查所有文档的一致性。

**示例输入：**

```bash
/speckit.analyze 进行全面分析
```

AI 会检查：

- spec.md、plan.md、tasks.md 之间是否存在矛盾

- 是否有遗漏的功能点

- 任务分解是否合理

- 是否存在歧义描述

如有问题，AI 会生成分析报告并协助修复。

---

### Step 8:开始构建项目

使用 `/speckit.implement` 命令，让 AI 按顺序执行任务列表编写代码。

**示例输入：**

```bash
/speckit.implement 开始写代码
```

AI 会：

- 按顺序执行 tasks.md 中的每个任务

- 每完成一个任务在文档中打勾 ✓

- 自动修复测试失败

- 实时反馈进度

执行过程中可以随时暂停检查，确保每一步都符合预期。

---

### Step 9:运行与验收

```bash
# 启动开发服务器

npm run dev
```

按照验收清单逐项检查：

- [ ]功能完整可用（新增、删除、标记、筛选）

- [ ]刷新页面后数据不丢失

- [ ]界面文案为中文，设计风格清新

- [ ]控制台无关键报错信息

- [ ]基础测试通过

---

## 六、常见问题

**Q: 如何修改任务优先级？**

A: 可以直接编辑 `specs/xxx/tasks.md` 文件，调整任务顺序后重新执行 `/speckit.implement`。

**Q: 如何中途暂停实现？**

A: 在 `/speckit.implement` 执行过程中，可以直接打断对话，下次使用 `/speckit.implement --continue` 继续执行。

**Q: LocalStorage 数据如何清空？**

A: 可以在浏览器开发者工具的 Application 面板中手动清空，或在代码中添加清空按钮。

## 场景

页面某区域图片显示异常、产品项缺失。

## 推荐流程（简化版）：

1. 在旧项目执行 `specify init .`

2. `/speckit.specify` 描述缺陷与期望结果

3. `/speckit.plan` 输出修复策略

4. `/speckit.tasks` 生成修复任务

5. `/speckit.implement` 落地修复

6. 回归验证 + 对照需求确认

## 详细操作步骤

### Step 1: 初始化旧项目

进入有 bug 的旧项目根目录，执行初始化命令：

```bash
specify init .
```

执行过程：

- 下载模板安装包并解压

- 初始化 Git 仓库

- 选择 CodeBuddy 作为开发工具并确认

初始化后会生成 `.specify` 目录及相关配置文件。

---

### Step 2: 描述缺陷与期望

使用 `/speckit.specify` 命令清晰描述问题，只说"要什么"，不讨论"怎么实现"。

**示例输入：**

```markdown
/speckit.specify 发现两个问题需要修复：



1. 产品列表页面，图片显示异常

- 现状：图片区域显示为空白或破碎图标

- 期望：图片正常显示，支持懒加载



2. 产品数据缺失

- 现状：某些产品项在列表中不显示

- 期望：所有产品项都能正确展示



验收标准：

- 图片加载正常，无破碎图标

- 产品列表数据完整，无遗漏

- 控制台无图片加载错误
```

AI 会生成 `spec.md` 文档，详细记录问题描述和验收标准。

---

### Step 3: 生成修复策略

使用 `/speckit.plan` 命令，让 AI 基于现有代码分析问题并设计修复方案。

**示例输入：**

```bash
/speckit.plan 执行
```

AI 会分析现有代码结构，输出包含以下内容的技术方案：

- 问题根因分析（如图片路径错误、数据过滤逻辑问题）

- 技术选型（如使用适当的图片加载库）

- 修复策略设计（如修正图片路径、调整数据查询逻辑）

- 兼容性考虑（确保不影响其他功能）

---

### Step 4: 生成修复任务

使用 `/speckit.tasks` 命令，将修复策略拆解为可执行的具体任务。

**示例输入：**

```bash
/speckit.tasks 生成详细任务列表
```

AI 会生成类似以下的任务列表：

- **Phase 1**: 问题定位

- 分析图片加载逻辑

- 检查数据查询代码

- **Phase 2**: 代码修复

- 修正图片路径配置

- 修复数据过滤逻辑

- **Phase 3**: 测试验证

- 手动测试图片显示

- 验证数据完整性

- 回归测试相关功能

---

### Step 5: 执行修复

使用 `/speckit.implement` 命令，让 AI 按顺序执行任务列表进行修复。

**示例输入：**

```bash
/speckit.implement 开始修复
```

AI 会：

- 按顺序执行 tasks.md 中的每个任务

- 修改相关代码文件

- 每完成一个任务在文档中打勾 ✓

- 遇到问题自动尝试修复

执行过程中可以随时暂停检查，确保修改符合预期。

---

### Step 6: 回归验证

修复完成后，运行项目并验证：

```bash
npm run dev
```

按照验收清单逐项检查：

- [ ]图片正常显示，无破碎图标

- [ ]所有产品项都能正确展示

- [ ]控制台无图片加载错误

- [ ]相关功能不受影响

- [ ]代码风格保持一致

---

## 实战示例

假设有一个电商产品列表页面存在上述问题，完整的修复流程如下：

```bash
# 1. 初始化项目

specify init .



# 2. 描述问题

/speckit.specify 产品列表页面图片显示异常，部分产品项缺失



# 3. 生成修复方案

/speckit.plan



# 4. 生成任务列表

/speckit.tasks



# 5. 执行修复

/speckit.implement



# 6. 验证结果

npm run dev

# 在浏览器中打开页面，检查图片和产品数据是否正常
```

---

## 价值

把"拍脑袋修 bug"变成"有依据的修复闭环"。

- Speckit 的核心不是"多一套命令"，而是**开发范式升级**。

- 在 AI 时代，最重要能力之一是：**把需求转成可执行规约**。

- 真正稳定的 AI 开发链路应是：**先规约，后实现；先一致，后加速**。

### 下一讲预告

> **第 6 讲：SpeckitList 动态管理**

> 

> SpeckitList 的核心是"动态管理"。下一讲将学习如何通过列表操作、筛选排序等实用功能，高效管理和操控代码片段。
