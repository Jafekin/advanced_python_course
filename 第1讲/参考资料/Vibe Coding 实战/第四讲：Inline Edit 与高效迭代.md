> **本讲目标：** 掌握 Cmd/Ctrl+K 行内编辑、Diff 预览和快速迭代的用法，把修改动作留在当前上下文里，减少打断。

> 

> **预计时长：** 60 分钟

> 

> **难度等级：** 技能

## 自学导航卡

- **前置依赖：** 已能运行基础项目，理解 Diff 基本概念

- **预计耗时：** 新手 60-90 分钟｜有经验 40-60 分钟

- **完成标准：** 完成至少 3 次有效 Inline Edit，且每次均通过 Diff 审查

- **卡点入口：** 若改动过大，切换为“选中更小代码块 + 单一指令”

## 一、程序员的心流

心理学家米哈里·契克森米哈赖（Csikszentmihalyi）定义的"心流"状态：

- 完全沉浸在任务中

- 时间感知消失

- 产出效率提升 2-5 倍

**心流的最大敌人 = 上下文切换。**

传统开发中打断心流的场景：

<img src='images/4-1.png' width=800px />

## 二、Inline Edit 如何保护心流

**Inline Edit（行内编辑）** 的核心价值：**在当前上下文中完成修改，不切换文件、不切换窗口。**

<img src='images/4-2.png' width=800px />

<img src='images/4-3.png' width=800px />

## 一、基本操作

| 操作 | 快捷键 | 说明 |

|------|--------|------|

| 唤起行内编辑 | `Cmd+K`（Mac）/ `Ctrl+K`（Windows） | 在光标位置或选中区域唤起 AI 编辑 |

| 接受修改 | 点击 Accept | 应用 AI 建议的修改 |

| 拒绝修改 | 点击 Reject | 撤销 AI 建议 |

| 查看 Diff | 自动展示 | 修改前后的对比视图 |

## 二、三种使用模式

### 模式 1：无选中 —— 生成新代码

光标放在空行，按 `Cmd+K`，输入指令：

```
创建一个 useDebounce Hook，接受 value 和 delay 参数
```

AI 会在光标位置直接生成代码。

上述内容在视频中实操展示：

<video src='video/4-1.mp4' controls width=800px ></video>

### 模式 2：选中代码 —— 修改现有代码

选中一段代码，按 `Cmd+K`，输入指令：

```
添加错误处理和 loading 状态
```

AI 会基于选中的代码生成修改版本，并展示 Diff。

上述内容在视频中实操展示：

<video src='video/4-2.mp4' controls width=800px ></video>

### 模式 3：选中代码 —— 解释 / 转换

选中代码后：

```
// 解释

解释这段代码的逻辑



// 转换

把这段 Class Component 转成 Hooks



// 优化

优化这段代码的性能
```

<div style="padding: 10px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px; margin: 10px 0;">

<strong>这一部分与模式 2 的操作流程相同，只是沟通的内容不同，则不再重复展示。</strong>

</div>

## 三、Diff 预览的正确使用方式

当 AI 生成修改建议时，会展示一个 **Diff 视图**：

<img src='images/4-4.png' width=600px />

其中，红色表示删除内容，绿色表示新增内容，未着色部分表示保持不变。

**审查 Diff 的重点：**

| 检查项 | 关注点 |

|--------|--------|

| **逻辑正确性** | 是否改动了原有业务逻辑，或引入了错误逻辑？ |

| **完整性** | 需要修改的内容是否已全部覆盖？ |

| **副作用** | 是否误改了与当前任务无关的代码？ |

| **风格一致性** | 是否与现有代码风格和命名规范保持一致？ |

## 一、局部重构

### 场景 1：提取函数

选中一段重复逻辑：

```typescript
// 选中以下代码

const fullName = `${user.firstName} ${user.lastName}`;

const initials = `${user.firstName[0]}${user.lastName[0]}`.toUpperCase();

const displayName = user.nickname || fullName;
```

按 `Cmd\Ctrl+K`：

```
将选中的逻辑提取为一个 formatUserName 工具函数
```

### 场景 2：简化条件判断

选中嵌套的 if-else：

```typescript
// 选中这段

if (user.role === 'admin') {

if (user.isActive) {

return <AdminDashboard />;

} else {

return <InactiveNotice />;

}

} else if (user.role === 'editor') {

if (user.isActive) {

return <EditorDashboard />;

} else {

return <InactiveNotice />;

}

} else {

return <UserDashboard />;

}
```

按 `Cmd+K`：

```
用 early return + 策略模式简化这段条件逻辑
```

### 场景 3：类型安全增强

选中一个函数：

```
给这个函数添加完整的 TypeScript 类型注解，

包括参数类型、返回值类型和可能的错误类型
```

## 二、代码解释

当你接手一段不熟悉的代码时：

选中代码，按 `Cmd+K`：

```
用中文逐行解释这段代码的逻辑，特别说明：

1. 数据流向

2. 状态变化

3. 可能的边界情况
```

## 三、注释生成

### 函数级注释

选中函数，按 `Cmd+K`：

```
生成 JSDoc 风格的中文注释，包含：

- 函数描述

- @param 每个参数说明

- @returns 返回值说明

- @throws 可能的异常

- @example 使用示例
```

### 模块级注释

在文件顶部，按 `Cmd+K`：

```
为这个模块生成头部注释，说明：

- 模块职责

- 核心导出

- 依赖关系

- 使用示例
```

## 一、场景设定

你接到了一个 300 行的"上帝组件"，所有逻辑堆在一个文件里。目标：用 Vibe Coding 方式将它模块化。

## 二、原始代码（简化版示例）

假设有一个 `Dashboard.tsx` 文件，包含了：

- 数据获取逻辑

- 筛选/搜索逻辑

- 表格渲染

- 图表渲染

- 弹窗表单

- 导出功能

## 三、Step 1：让 AI 分析代码结构

在 CodeBuddy 对话中：

```
@Files src/components/Dashboard.tsx



请分析这个文件，列出：

1. 文件中包含了哪些独立的功能模块

2. 哪些逻辑可以抽取为自定义 Hook

3. 哪些 UI 可以抽取为子组件

4. 建议的拆分方案（文件名 + 职责）
```

## 四、Step 2：按方案逐步拆分

根据 AI 给出的拆分方案，使用 Inline Edit 逐步操作：

**拆分 Hook —— 选中数据获取相关代码：**

```
将选中的数据获取逻辑提取为 useDashboardData Hook，

放到 src/hooks/useDashboardData.ts，

在原文件中替换为 Hook 调用。
```

**拆分子组件 —— 选中表格渲染部分：**

```
将选中的表格 UI 提取为 DashboardTable 子组件，

放到 src/components/dashboard/DashboardTable.tsx，

Props 包含 data、onSort、onFilter。
```

**拆分工具函数 —— 选中数据转换逻辑：**

```
将选中的数据转换和格式化逻辑提取到 src/lib/dashboard-utils.ts，

每个函数都加上完整的类型注解和中文注释。
```

## 五、Step 3：验证拆分结果

```
现在请检查拆分后的 @Files src/components/Dashboard.tsx：

1. 是否还有超过 50 行的单个函数？

2. 是否所有 import 都正确？

3. 功能是否与拆分前完全一致？
```

## 六、重构前后对比

```
重构前：

Dashboard.tsx (300行)

├── 数据获取 (60行)

├── 筛选逻辑 (40行)

├── 表格渲染 (80行)

├── 图表渲染 (50行)

├── 弹窗表单 (40行)

└── 导出功能 (30行)



重构后：

Dashboard.tsx (60行) —— 只负责组合和布局

├── hooks/

│ ├── useDashboardData.ts (60行)

│ └── useDashboardFilter.ts (40行)

├── components/dashboard/

│ ├── DashboardTable.tsx (80行)

│ ├── DashboardChart.tsx (50行)

│ └── DashboardForm.tsx (40行)

└── lib/

└── dashboard-utils.ts (30行)
```

## 一、"3 分钟迭代环"

<img src='images/4-5.png' width='800px' />

## 二、常用迭代指令速查表

| 场景 | 快速指令 |

|------|---------|

| 添加 loading 状态 | `给这个组件加上 loading 骨架屏` |

| 添加错误处理 | `添加 try-catch 和错误提示 UI` |

| 响应式适配 | `让这个布局在移动端也能正常显示` |

| 性能优化 | `按“useMemo/useCallback/React.memo”最小改动优化这个组件，并说明每处优化依据` |

| 添加动画 | `给这个列表加上进入/退出动画` |

| 国际化 | `把硬编码的中文提取为 i18n 字符串` |

| 无障碍 | `添加 ARIA 属性和键盘导航支持` |

| 暗色模式 | `添加 dark mode 支持` |

**性能优化使用场景速记：**

- `useMemo`：用于**计算成本高**且依赖不频繁变化的值（如大列表过滤、复杂排序、统计聚合）。

- `useCallback`：用于把函数**传给子组件**（尤其子组件已做 `React.memo`）时，保持引用稳定，减少子组件重复渲染。

- `React.memo`：用于纯展示型或稳定输入组件，避免父组件更新导致的**不必要重渲染**。

可直接用这条指令让 AI 选择策略：

```text
请检查这个组件的渲染热点：

1) 高成本计算改为 useMemo；

2) 传给子组件的回调改为 useCallback；

3) 对稳定 props 的子组件使用 React.memo。

要求：给出每一处优化的原因与前后差异。
```

## 三、批量修改技巧

当需要跨文件的统一修改时，使用 Chat 模式而不是 Inline Edit。

先看一个基础案例：

```
请在以下所有组件中统一添加 ErrorBoundary 包裹：

@Files src/components/UserList.tsx

@Files src/components/ProductList.tsx

@Files src/components/OrderList.tsx



使用统一的 ErrorFallback 组件显示错误信息。
```

再看 3 个更复杂、真实项目常见的批量修改场景：

### 场景 A：跨文件 API 调用统一错误处理

```
请统一改造以下 API 调用文件的错误处理策略：

@Files src/lib/api/user.ts

@Files src/lib/api/order.ts

@Files src/lib/api/product.ts



要求：

1. 所有请求统一用 ApiError 结构抛错（code/message/requestId）；

2. 401 统一触发 logoutAndRedirect；

3. 5xx 统一上报 logError，并返回用户友好提示；

4. 不修改函数签名与返回类型。



最后输出：

- 修改文件清单

- 统一后的错误处理流程图（文字版）

- 可能的兼容性风险
```

### 场景 B：多个组件统一国际化提取

```
请把以下组件中的硬编码中文提取到 i18n 资源：

@Files src/components/UserList.tsx

@Files src/components/OrderList.tsx

@Files src/components/CheckoutPanel.tsx



要求：

1. 使用现有 i18n 命名空间：common、user、order；

2. 文案 key 按 "模块.场景.语义" 命名；

3. 保持原有 UI 结构与样式不变；

4. 缺失 key 时给出兜底文案。



最后输出：

- 新增/修改的 locale 文件

- 组件中的替换点位统计

- 未覆盖文案清单
```

### 场景 C：批量补齐 TypeScript 类型定义

```
请为以下模块补齐缺失的 TypeScript 类型，并消除 any：

@Files src/hooks/useUsers.ts

@Files src/hooks/useOrders.ts

@Files src/components/UserTable.tsx

@Files src/components/OrderTable.tsx



要求：

1. 优先复用 @Files src/types 下已有类型；

2. 新增类型统一放在 @Files src/types/view-model.ts；

3. 不改变运行时行为；

4. 所有对外 Props、Hook 返回值必须显式标注类型。



最后输出：

- 新增类型定义列表

- any -> 具体类型的映射表

- 仍无法确定类型的位置与原因
```

## 练习 1：Inline Edit 速度挑战（必做）

1. 创建一个简单的 Todo List 组件（让 AI 生成初版）

2. 用 Inline Edit 连续完成以下 8 个修改：
- 添加完成状态切换

- 添加删除功能

- 添加编辑功能

- 添加优先级标签

- 添加拖拽排序

- 添加筛选（全部/已完成/未完成）

- 添加本地存储持久化

- 添加批量操作
3. 记录总耗时，目标：**30 分钟内完成**

## 练习 2：屎山重构挑战（进阶）

1. 找一个你项目中最"臃肿"的组件

2. 用本讲学到的方法重构它

3. 记录：重构前行数 vs 重构后主文件行数

## 练习 3：建立你的迭代指令库（必做）

整理你在日常开发中最常用的 10 个 Inline Edit 指令，形成你的"快速指令手册"。

本讲结束时，你应该能做到：

- 熟练使用 Cmd+K 行内编辑的几种常见用法

- 会看 Diff，并能用清单做快速审查

- 能把一个复杂组件拆出更清晰的子组件或 Hook

- 建立一套可复用的“短周期迭代”习惯

- 知道什么时候用 Chat，什么时候用 Inline Edit

## 核心收获

> **心流 = 连续性 × 效率**

> 

> Inline Edit 保护了你的连续性（不切换上下文），

> AI 提供了效率（秒级生成修改方案）。

> 二者结合 = 10 倍效率的心流编程。

## 下一讲预告

> **第 5 讲：Speckit—从“氛围编程到“规约编程”**

> 

> 前 4 讲你学会了怎么和 AI 高效沟通。但面对复杂项目，光靠对话不够了。你需要一个 Speckit 来约束 AI，这就是 Speckit 开发。
