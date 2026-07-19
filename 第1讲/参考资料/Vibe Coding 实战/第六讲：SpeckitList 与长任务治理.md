> **本讲目标：** 学会把复杂功能拆成可执行的小任务，并用 SpeckitList 管理进度，让 AI 按顺序推进；当结果跑偏时，优先回到 Speckit 做修正。

> 

> **预计时长：** 75 分钟

> 

> **难度等级：** 进阶

## 自学导航卡

- **预计耗时：** 新手 75-110 分钟｜有经验 50-75 分钟

- **完成标准：** 生成 8-12 条 SpeckitList 并完成前 3 条任务落地

- **卡点入口：** 若执行混乱，保持“同一时刻仅 1 个 in_progress 主任务”

## 一、AI 的"健忘症"

AI 大模型有一个天然弱点：**上下文窗口有限**。当任务复杂度超过一定阈值：

| 任务规模 | AI 表现 | 风险 |

|---------|---------|------|

| 小任务（1 个文件） | 优秀 | 几乎无风险 |

| 中任务（3-5 个文件） | 良好 | 偶尔遗漏 |

| 大任务（10+ 个文件） | 不稳定 | 经常丢失上下文 |

| 巨任务（整个功能模块） | 灾难 | 前后矛盾、遗漏严重 |

## 二、解决方案：SpeckitList

**SpeckitList = Speckit 文件 + 任务清单 + 状态跟踪**

<img src='images/6-3.png' width=800px />

## 三、核心原则

> **大任务拆成小任务，小任务逐个执行，每个任务都有明确的验收标准。**

## 一、拆解原则

| 原则 | 说明 | 示例 |

|------|------|------|

| **单一职责** | 每个任务只做一件事 | 不推荐：“创建组件并对接 API”；推荐：“创建组件” + “对接 API” |

| **可独立验证** | 完成后能立即验证 | 不推荐：“写一半的逻辑”；推荐：“完整的 Hook + 类型” |

| **有序依赖** | 后面的任务依赖前面的产出 | 类型 → API 层 → Hook → 组件 |

| **粒度适中** | 每个任务 10-30 分钟可完成 | 不推荐：太细“改一行代码”；不推荐：太粗“实现整个模块” |

## 二、标准拆解模板

对于一个完整的前端功能，标准拆解顺序为：

```
1. [ ] 定义 TypeScript 类型

2. [ ] 创建 API 请求函数

3. [ ] 创建自定义 Hook

4. [ ] 创建 UI 子组件

5. [ ] 创建页面组件（组合子组件）

6. [ ] 添加交互逻辑

7. [ ] 添加错误处理和 Loading 状态

8. [ ] 添加响应式适配

9. [ ] 添加动画和过渡效果

10. [ ] 集成测试和边界情况处理
```

## 一、生成任务清单

在 CodeBuddy 中：

```
请阅读以下 Speckit 文件：

@Files specs/feature-task-board.md

@Files specs/ui-task-board.md



根据 Speckit 的内容，帮我生成一份详细的开发任务清单（SpeckitList），要求：

1. 按依赖关系排序（先做的排前面）

2. 每个任务标注优先级（P0/P1/P2，与 Speckit 中的优先级对应）

3. 每个任务有明确的验收标准

4. 每个任务预估工作量（以"AI 生成轮数"为单位）

5. 用 Markdown Checkbox 格式
```

## 二、期望输出：任务清单

<details style="margin-bottom: 8px;">

<summary style="color: #f57c00; font-weight: 500; cursor: pointer;">AI 应该生成类似以下的清单：</summary>

```markdown
# SpeckitList: 任务看板功能



## Phase 1: 基础设施（P0）



### 1.1 类型定义

- [ ] 创建 `src/types/task.ts`

- 定义 Task, TaskStatus, Priority 类型

- 定义 API 请求/响应类型

- **验收标准：** TypeScript 编译通过，无 any 类型

- **预估：** 1 轮



### 1.2 API 层

- [ ] 创建 `src/lib/api/task.ts`

- 实现 getTasks, createTask, updateTask, moveTask, deleteTask

- 统一错误处理

- **验收标准：** 所有函数有完整类型注解，能正确发送请求

- **预估：** 1 轮



### 1.3 自定义 Hook

- [ ] 创建 `src/hooks/useTasks.ts`

- 实现数据获取、缓存、乐观更新

- **验收标准：** Hook 返回 data, isLoading, error，支持筛选参数

- **预估：** 2 轮



## Phase 2: 核心 UI（P0）



### 2.1 任务卡片组件

- [ ] 创建 `src/components/board/TaskCard.tsx`

- 展示标题、优先级、标签、头像、日期

- 支持 hover 和拖拽效果

- **验收标准：** 匹配 UI Speckit 中的卡片规格

- **预估：** 2 轮



### 2.2 看板列组件

- [ ] 创建 `src/components/board/BoardColumn.tsx`

- 列标题 + 数量 + 卡片列表 + 新建按钮

- 支持拖拽放置区域

- **验收标准：** 卡片可拖入拖出

- **预估：** 2 轮



### 2.3 看板画布

- [ ] 创建 `src/components/board/BoardCanvas.tsx`

- 横向排列所有列，支持横向滚动

- 集成拖拽库（dnd-kit）

- **验收标准：** 4 列正常展示，可横向滚动

- **预估：** 2 轮



### 2.4 页面组装

- [ ] 创建 `src/app/board/page.tsx`

- 组合 Header + Canvas

- 连接 useTasks Hook

- **验收标准：** 页面加载数据并展示看板

- **预估：** 1 轮



## Phase 3: 交互功能（P0）



### 3.1 拖拽排序

- [ ] 实现拖拽逻辑

- 跨列移动 + 列内排序

- 乐观更新 + 错误回滚

- **验收标准：** 拖拽流畅，状态正确更新

- **预估：** 3 轮



### 3.2 创建任务

- [ ] 实现任务创建流程

- 内联表单 + 弹窗详细表单

- 表单验证

- **验收标准：** 创建后卡片立即出现在对应列

- **预估：** 2 轮



### 3.3 任务详情

- [ ] 创建 `TaskDetailDrawer` 组件

- 侧边抽屉展示完整信息

- 支持编辑和删除

- **验收标准：** 点击卡片展开抽屉，编辑后保存

- **预估：** 2 轮



## Phase 4: 增强功能（P1）



### 4.1 筛选与搜索

- [ ] 实现 FilterBar 和 SearchInput

- 按指派人、优先级、标签筛选

- 搜索防抖

- **验收标准：** 筛选结果正确，搜索响应及时

- **预估：** 2 轮



### 4.2 自定义列

- [ ] 支持添加/删除/重命名列

- **验收标准：** 列配置持久化

- **预估：** 2 轮



## Phase 5: 体验优化（P1）



### 5.1 空状态和 Loading

- [ ] 各种状态的 UI 处理

- **预估：** 1 轮



### 5.2 动画效果

- [ ] 拖拽、过渡、列表动画

- **预估：** 2 轮



### 5.3 响应式适配

- [ ] 移动端列表视图

- **预估：** 2 轮



---

**总计预估：25 轮 AI 交互**
```

</details>

模型输出最后总结截图：

<img src='images/6-1.png' width=600px />

## 三、分步执行

有了任务清单后，逐个任务和 AI 对话：

```
我正在执行 SpeckitList 中的任务 1.1：类型定义。



请参考：

@Files specs/feature-task-board.md（数据模型章节）



创建 src/types/task.ts，严格按照 Speckit 中的字段定义。



完成后我会将该任务标记为已完成。
```

上述示例片段截图如下：

<img src='images/6-2.png' width=400px />

每完成一个任务就更新清单：

```markdown
### 1.1 类型定义

- [x] 创建 `src/types/task.ts`（已完成，2024-01-15）
```

## 一、问题检测：AI 跑偏的信号

| 信号 | 表现 | 原因 |

|------|------|------|

| 自由发挥 | AI 添加了 Speckit 中没有的功能 | Prompt 约束不够 |

| 前后矛盾 | 新生成的代码和之前的不兼容 | 上下文丢失 |

| 过度设计 | 简单功能搞出复杂架构 | 方案边界没收住 |

| 忽略约束 | 不符合 Speckit 中的非功能需求 | 缺少明确的非功能约束与验收口径 |

## 二、纠偏策略：修改 Speckit，而不是修改代码

<details>

<summary style="color:#0066CC; font-style:bold">传统方式（修改代码）：</summary>

<img src='images/6-5.png' width=800px />

</details>

<details>

<summary style="color:#0066CC; font-style:bold">自愈式开发（修改 Speckit）：</summary>

<img src='images/6-4.png' width=800px />

</details>

## 三、实操示例

### 场景

AI 在实现拖拽时用了 react-beautiful-dnd（你想用 @dnd-kit）。

**不推荐：手动改代码**

```
// 把 AI 的 react-beautiful-dnd 代码手动改成 dnd-kit

// ... 改了 200 行 ...

// 结果：下次让 AI 改东西时，它还是按 react-beautiful-dnd 来
```

**推荐：更新 Speckit**

更新 `specs/feature-task-board.md`，添加技术选型约束：

```markdown
## 技术选型约束

- 拖拽库：必须使用 @dnd-kit/core + @dnd-kit/sortable（不用 react-beautiful-dnd）

- 原因：更好的 TypeScript 支持和更小的包体积
```

然后重新生成：

```
Speckit 中的技术选型已更新，请重新看一下：

@Files specs/feature-task-board.md



然后重新实现任务 3.1（拖拽排序），使用 @dnd-kit 而不是 react-beautiful-dnd。
```

## 四、Speckit 的动态更新流程

<img src='images/6-6.png' width=800px />

## 一、完整的 Speckit + SpeckitList 工作流

```
Day 1: 需求 & 设计

├── 写 Feature Speckit

├── 写 UI Speckit

├── 让 AI 审查 Speckit 完整性

└── 确定最终 Speckit



Day 2-3: 拆解 & 执行

├── 让 AI 生成 SpeckitList

├── 审查并调整任务清单

├── 逐个执行任务

│ ├── 每个任务引用相关 Speckit 章节

│ ├── 完成后打钩

│ └── 发现问题则更新 Speckit

└── Phase 1-2 完成



Day 4-5: 深入 & 优化

├── 继续执行 Phase 3-5

├── 维护问题日志

├── 更新 Speckit 变更记录

└── 最终集成验证
```

## 练习 1：SpeckitList 生成（必做）

1. 拿出你在第 5 讲写的 Feature Speckit

2. 让 CodeBuddy 生成对应的 SpeckitList

3. 审查并调整任务拆解的粒度

## 练习 2：分步执行 3 个任务（必做）

从你的 SpeckitList 中选 3 个连续的任务：

1. 按顺序逐个执行

2. 每个任务完成后更新清单状态

3. 如果遇到问题，练习"修改 Speckit 而不是修改代码"

## 练习 3：完整项目管理（进阶）

用 SpeckitList 管理一个完整的小型功能开发（至少 10 个任务）：

1. 维护进度追踪

2. 记录问题日志

3. 记录 Speckit 变更

4. 最终输出一份"项目复盘报告"

eckit 的人"。**

> 

> 当 AI 输出不符合预期时，90% 的情况是 Speckit 不够清晰，

> 而不是 AI 不够聪明。完善 Speckit 比修改代码有效 10 倍。

本讲结束时，你应该能做到：

- 解释清楚为什么大型任务需要 SpeckitList 才能稳定推进

- 把一个功能拆成 8-12 个可执行、可验收的小任务

- 让 AI 基于 Speckit 自动生成任务清单，并按顺序推进

- 当结果跑偏时，能回到 Speckit 修正约束，再重新生成

- 形成一套可追踪的进度概览、问题日志和变更记录

### 核心收获

> 你不是"帮 AI 改 Bug 的人"，你是"维护 Sp

### 下一讲预告

> **第 7 讲：MCP 协议**

> 

> 学习 MCP 协议的工作原理和应用
