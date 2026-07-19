> **本讲目标：** 学会用规则稳定 AI 的输出风格，在 CodeBuddy 中建立一套个性化编码规范，让生成的代码更贴近你的习惯。

> 

> **预计时长：** 60 分钟

> 

> **难度等级：** 入门

## 自学导航卡

- **前置依赖：** 已完成第 1 讲，能在项目中创建文件与文件夹（无需编程基础）

- **预计耗时：** 新手 60-90 分钟｜有经验 45-60 分钟

- **完成标准：** 建立 10+ 条可验证规则，并验证同需求两次生成风格趋同

- **卡点入口：** 若规则不生效，先检查路径与“必须/禁止”约束写法

## 一、理解 AI 的"性格设定"

每一个 AI 对话都有一个隐藏的"人设说明书"，这就是 **System Prompt（系统提示词）**。

<img src='images/2-1.png' width=600px />

**System Prompt 决定了 AI 的：**

- 编码风格偏好（函数式 vs 面向对象）

- 语言/框架选择（TypeScript vs JavaScript）

- 注释习惯（中文 vs 英文、详细 vs 精简）

- 错误处理策略（静默处理 vs 抛出异常）

- 代码组织方式（单文件 vs 模块拆分）

## 二、为什么需要定制 System Prompt？

不定制 System Prompt = 每次都和一个"陌生人"合作：

| 场景 | 不定制 | 定制后 |

|------|--------|--------|

| 变量命名 | 可能用 `data`/`info`/`result` | 统一用你喜欢的命名规范 |

| 类型系统 | 可能给你 JS 也可能给 TS | 强制使用 TypeScript + 严格模式 |

| 样式方案 | 可能用 CSS Module、Styled 等 | 统一用 TailwindCSS |

| 注释语言 | 有时中文有时英文 | 统一中文注释 |

| 错误处理 | 可能忽略边界情况 | 强制处理所有异常 |

## 一、CodeBuddy 规则配置入口

在 CodeBuddy 中支持通过 **Rules（规则文件）** 来定制 AI 行为。

### 配置方式一：项目级规则（推荐）

在项目根目录创建 `.codebuddy/rules` 文件夹，添加规则文件：

```
项目根目录/

├── .codebuddy/

│ └── rules/

│ ├── coding-style.md # 编码风格规则

│ ├── project-context.md # 项目上下文

│ └── conventions.md # 命名约定

├── src/

└── ...
```

**两个方式来创建 `rules`**

<details>

<summary style="color:#0066CC; font-style:bold"><strong>方法 1:文件管理区新建文件</strong></summary>

<img src='images/2-2.png' width=300px />

</details>

<details>

<summary style="color:#0066CC; font-style:bold"><strong>方法 2:CodeBuddy 设置面板</strong></summary>

<img src='images/2-4.png' width=500px />

</details>

### 配置方式二：全局用户规则

通过 CodeBuddy 设置面板，配置适用于所有项目的全局规则。

## 二、编写你的第一份规则文件

创建 `.codebuddy/rules/coding-style.md`：

<details style="margin-bottom: 8px;">

<summary style="color: #f57c00; font-weight: 500; cursor: pointer;">详细文件内容</summary>

```markdown
# 编码风格规则



## 语言与框架

- 始终使用 TypeScript，开启 strict 模式

- React 组件使用函数式组件 + Hooks

- 样式使用 TailwindCSS，不使用行内样式或 CSS Module

- 使用 Next.js App Router（不使用 Pages Router）



## 命名规范

- 组件文件：PascalCase（如 `LoginForm.tsx`）

- 工具函数文件：camelCase（如 `formatDate.ts`）

- 常量文件：UPPER_SNAKE_CASE（如 `API_ENDPOINTS.ts`）

- React 组件：PascalCase（如 `UserProfile`）

- 函数和变量：camelCase（如 `getUserById`）

- 布尔变量：以 is/has/should 开头（如 `isLoading`）

- 事件处理器：以 handle 开头（如 `handleSubmit`）



## 代码风格

- 优先使用 const，避免 let，禁止 var

- 使用箭头函数，除非需要 this 绑定

- 优先使用函数式编程范式（map/filter/reduce）

- 使用解构赋值

- 每个函数不超过 30 行

- 使用 early return 减少嵌套

- 所有注释使用中文



## 类型定义

- 为所有函数参数和返回值添加类型注解

- 使用 interface 定义对象类型（不使用 type 别名定义对象）

- 使用 type 定义联合类型和工具类型

- 导出所有在其他文件中使用的类型



## 错误处理

- API 请求必须有 try-catch

- 用户可见的错误信息使用中文

- 控制台日志使用 English

- 使用自定义 Error 类，不使用裸字符串



## 目录结构

- components/ —— 可复用组件

- app/ —— 页面路由（Next.js App Router）

- lib/ —— 工具函数和业务逻辑

- types/ —— TypeScript 类型定义

- hooks/ —— 自定义 React Hooks

- constants/ —— 常量定义
```

</details>

## 三、编写项目上下文规则

创建 `.codebuddy/rules/project-context.md`：

<details style="margin-bottom: 8px;">

<summary style="color: #f57c00; font-weight: 500; cursor: pointer;">详细文件内容</summary>

```markdown
# 项目上下文



## 项目概述

这是一个 Vibe Coding 实训项目，使用 Next.js 14 + TailwindCSS + TypeScript 构建。



## 技术栈版本

- Next.js: 14.x（App Router）

- React: 18.x

- TypeScript: 5.x

- TailwindCSS: 3.x

- Node.js: 20.x



## 重要约定

- 状态管理：简单状态用 useState，复杂状态用 useReducer，跨组件用 Context

- 数据获取：优先使用 Next.js Server Components + fetch

- 表单处理：使用 React Hook Form + Zod 验证

- UI 组件：优先使用 shadcn/ui

- 图标：使用 Lucide React



## API 约定

- RESTful 风格

- 统一响应格式：{ code: number, data: T, message: string }

- 错误码：200 成功，400 参数错误，401 未授权，500 服务器错误
```

</details>

## 四、验证规则生效

在 CodeBuddy 中测试：

```markdown
帮我创建一个用户资料编辑组件，包含姓名、邮箱和头像上传功能
```

完成后效果如下：

<img src='images/2-3.png' width=800px />

要实现上述效果，你只需要完成三步：

1. 配置 `rules`

2. 通过对话创建项目

3. 通过对话启动并运行项目

<div style="padding: 10px; background: #fff8e1; border-left: 4px solid #ffc107; border-radius: 4px; margin: 10px 0;">

<strong>重要提示：</strong> 你不必精通编程，但需要在每一轮都认真检查 AI 的输出是否符合你的预期；如不符合，就继续对话并明确指出需要调整的点，直到结果满足要求。

</div>

---

## 三、进阶：让 AI 学习你的现有代码风格

## 1）代码风格模仿术

如果你已经有一个成熟项目，可以让 AI 学习你的风格：

### Step 1：提供代码样本

```
请阅读以下两个文件，学习其中的编码风格和模式：



@Files src/components/UserCard.tsx

@Files src/hooks/useAuth.ts



记住这些文件中的：

1. 组件结构模式

2. Hook 封装方式

3. 类型定义习惯

4. 错误处理方式

5. 注释风格
```

### Step 2：要求风格一致

```
现在，按照你刚才学到的风格，帮我创建一个 ProductCard 组件，

展示商品信息（图片、标题、价格、标签），点击跳转到详情页。

要求和 UserCard 保持完全一致的代码风格。
```

### Step 3：对比验证

```
请对比 UserCard 和你刚生成的 ProductCard，

列出在编码风格上的差异点，并修正不一致的地方。
```

## 2）Prompt Template（模板化提示词）

为常见任务准备好模板，每次使用时填空即可：

### 模板 1：创建组件

```
创建一个 [组件名] 组件：

- 功能：[功能描述]

- Props：[接口定义]

- 状态：[需要管理的状态]

- 交互：[用户交互行为]

- 样式参考：[设计参考]
```

### 模板 2：创建 API 接口

```
创建一个 API 路由 [路径]：

- 方法：[GET/POST/PUT/DELETE]

- 入参：[参数说明]

- 出参：[返回数据结构]

- 校验：[参数校验规则]

- 错误处理：[异常情况]
```

### 模板 3：创建 Hook

```
创建一个自定义 Hook [Hook名]：

- 用途：[解决什么问题]

- 输入：[参数]

- 输出：[返回值]

- 副作用：[需要处理的副作用]

- 清理：[需要清理的资源]
```

## 一、规则的分层策略

<img src='images/2-5.png' width=400px />

## 二、规则编写的 5 个原则

| 原则 | 说明 | 示例 |

|------|------|------|

| **具体** | 避免模糊表述 | 不推荐：“代码要简洁”；推荐：“每个函数不超过 30 行” |

| **可验证** | 能客观判断是否遵守 | 不推荐：“写好代码”；推荐：“启用 TypeScript strict 模式” |

| **有优先级** | 冲突时知道听谁的 | “性能和可读性冲突时，优先可读性” |

| **有例外** | 说明何时可以破例 | “除非是第三方库的回调，否则都用箭头函数” |

| **有示例** | 给出正反面代码示例 | 在规则中附上 Good/Bad 代码对比 |

## 三、常见反模式

**反模式 1：规则太多，AI 记不住**

```
# 不好：100+ 条细碎规则

- 缩进用 2 空格

- 字符串用单引号

- 分号必须加

- ... (还有 97 条)
```

**更合适的做法：聚焦关键规则，其余交给 ESLint**

```
# 好：20 条核心规则 + ESLint 配置

详见 .eslintrc.json 和 .prettierrc 配置文件。

以下仅列出 AI 需要特别注意的规则：

...
```

**反模式 2：规则自相矛盾**

```
- 优先使用函数式编程

- 所有组件用 Class Component ← 矛盾！
```

**反模式 3：规则没有上下文**

```
- 使用 useSWR ← AI 不知道什么场景用
```

**更合适的写法：**

```
- 客户端数据获取使用 useSWR，服务端数据获取使用 Next.js 内置 fetch
```

## 练习 1：创建你的规则文件（必做）

为你自己的项目创建一套完整的 CodeBuddy 规则文件：

1. 创建 `.codebuddy/rules/coding-style.md`

2. 至少包含以下章节：
- 语言与框架偏好

- 命名规范

- 代码风格

- 错误处理策略
3. 用 CodeBuddy 生成一个组件，验证规则是否生效

## 练习 2：风格模仿测试（进阶）

1. 找一个你喜欢的开源项目（如 shadcn/ui 的某个组件）

2. 把代码喂给 CodeBuddy，让它学习风格

3. 要求它用同样的风格生成一个新组件

4. 对比原始风格和 AI 生成的代码，找出差异

## 练习 3：Prompt 模板库（必做）

建立你自己的 Prompt 模板库，至少包含 5 个常用模板：

- 创建组件模板

- 创建 API 模板

- 创建 Hook 模板

- Bug 修复模板

- 代码重构模板

本讲结束时，你应该能做到：

- 理解 System Prompt 的作用与边界

- 在 CodeBuddy 中配置并维护项目级规则文件

- 用规则让代码风格更稳定、更一致

- 沉淀一份可复用的 Prompt 模板库

- 掌握规则编写的常见坑与最佳实践

## 核心收获

> **你的 Rules 文件 = 你的编码 DNA。**

> 一旦配置好，AI 生成的每一行代码都带着你的风格烙印。

> 这不是在"使用工具"，这是在"训练助手"。

## 下一讲预告

> **第 3 讲：Context is King —— 上下文精准投喂术**

> 

> 规则解决了"AI 的风格"问题，下一讲解决"AI 的视野"问题。你将学会用 `@` 符号精准控制 AI 能看到什么、不能看到什么。
