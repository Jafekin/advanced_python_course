> **本讲目标：** 了解 MCP 的基本概念与接入方式，把外部数据源（例如数据库结构）接到 AI 的上下文里，让生成的代码更贴近真实系统。

> 

> **预计时长：** 90 分钟

> 

> **难度等级：** 高阶

## 自学导航卡

- **前置依赖：** 已理解 Agent 工具调用，具备基本密钥安全意识

- **预计耗时：** 新手 90-140 分钟｜有经验 60-90 分钟

- **完成标准：** 成功连接 1 个 MCP Server，并完成一次元数据驱动代码生成

- **卡点入口：** 若连接失败，先独立验证 Server 进程与权限再接入 AI

## 一、AI 的"信息孤岛"问题

没有 MCP 之前，AI 的能力边界是：

AI 能做的：

- 读取项目文件

- 修改代码

- 运行终端命令

- 搜索项目内的代码

AI 做不到的（需要外部连接能力）：

- 查询数据库

- 调用第三方 API

- 读取实时数据

- 操作 GitHub Issues

- 访问 Figma 设计稿

- 查询生产环境日志

**MCP 的目标：打破这些限制，让 AI 能访问任何外部服务。**

## 二、什么是 MCP？

**MCP（Model Context Protocol，模型上下文协议）** 是由 Anthropic 提出的开放标准，用于连接 AI 模型与外部数据源和工具。

<img src='images/7-1.png' width=800px />

## 三、MCP 的核心概念

| 概念 | 类比 | 说明 |

|------|------|------|

| **MCP Host** | 浏览器 | AI 应用（CodeBuddy） |

| **MCP Client** | 网页的 JS | 在 Host 中负责连接 Server |

| **MCP Server** | Web 服务器 | 提供工具和数据的服务程序 |

| **Tool** | API 接口 | Server 暴露给 AI 的具体能力 |

| **Resource** | 网页内容 | Server 提供的数据（如数据库表结构） |

| **Prompt** | 页面模板 | Server 提供的预置 Prompt 模板 |

## 四、MCP 的工作流程

```
1. AI 收到用户请求："帮我写查询用户订单的 SQL"

↓

2. AI 判断需要外部信息（数据库表结构）

↓

3. AI 调用 MCP Client → 请求 MCP Server

↓

4. MCP Server 连接数据库 → 读取表结构

↓

5. MCP Server 返回表结构信息给 AI

↓

6. AI 基于真实表结构编写准确的 SQL/代码
```

## 一、常用 MCP Server 一览

| MCP Server | 连接目标 | 典型用途 |

|-----------|---------|---------|

| **Filesystem** | 本地文件系统 | 安全地访问指定目录 |

| **PostgreSQL** | PostgreSQL 数据库 | 读取表结构、执行查询 |

| **MySQL** | MySQL 数据库 | 读取表结构、执行查询 |

| **SQLite** | SQLite 数据库 | 本地数据库操作 |

| **GitHub** | GitHub API | 管理 Issues、PR、仓库 |

| **Brave Search** | Brave 搜索引擎 | 实时网络搜索 |

| **Puppeteer** | 浏览器 | 网页截图、自动化测试 |

| **Memory** | 持久化记忆 | 跨对话记住信息 |

| **Fetch** | 任意 URL | 获取网页内容 |

## 二、MCP 与 API 的区别

| 维度 | 传统 API 调用 | MCP 协议 |

|------|-------------|---------|

| 调用者 | 人类写代码调用 | AI 自主判断何时调用 |

| 认知层 | 开发者需要知道 API 细节 | AI 通过 Tool 描述自动理解 |

| 交互方式 | 程序化、固定流程 | 对话式、灵活路由 |

| 集成成本 | 每个服务单独对接 | 统一协议，即插即用 |

## 一、MCP 配置文件

在 Cloud Studio 中，MCP 配置文件位于项目根目录的 `/root/.codebuddy/mcp.json`：

```json
{

"mcpServers": {

"server-name": {

"command": "启动命令",

"args": ["参数1", "参数2"],

"env": {

"ENV_VAR": "值"

}

}

}

}
```

## 二、配置 SQLite MCP Server（入门级）

这是最简单的入门示例——让 AI 能直接读取和操作本地 SQLite 数据库。

### **Step 1：配置 MCP**

<img src='images/7-4.png' width=500px />

`/root/.codebuddy/mcp.json` 内容如下：

```json
{

"mcpServers": {

"sqlite": {

"command": "npx",

"args": [

"-y",

"mcp-server-sqlite",

"data/app.db"

]

}

}

}
```

### **Step 2：重启 CodeBuddy**

配置完成后需要重新加载 CodeBuddy，让 MCP 连接生效。

### **Step 3：创建示例数据库**

先让 Agent 创建一个测试数据库：

```
帮我创建一个 SQLite 数据库 data/app.db，包含以下表：



users 表：id, name, email, role, created_at

products 表：id, name, price, category, stock, created_at

orders 表：id, user_id(外键), total_price, status, created_at

order_items 表：id, order_id(外键), product_id(外键), quantity, price



每个表插入 10-20 条测试数据。
```

<img src='images/7-2.png' width=400px />

### **Step 4：验证连接**

在 CodeBuddy 中测试：

```
请列出当前数据库中的所有表及其字段结构
```

**如果配置正确，AI 会通过 MCP Server 查询数据库，返回真实的表结构信息。如下图所示：**

<img src='images/7-3.png' width=500px />

## 三、配置 GitHub MCP Server

### **Step 1：获取 GitHub Token**

1. 进入 GitHub → Settings → Developer settings → Personal access tokens（[快速链接点我](https://github.com/settings/personal-access-tokens)）

2. 创建一个 Token，勾选 `repo`, `issues`, `pull_requests` 权限

3. 保存 Token 值，替换下述的 `your-github-token`

### **Step 2：配置 MCP**

在 `/root/.codebuddy/mcp.json` 中添加：

```json
{

"mcpServers": {

"sqlite": {

"command": "npx",

"args": [

"-y",

"mcp-server-sqlite",

"data/app.db"

]

},

"github": {

"command": "npx",

"args": [

"-y",

"@teolin/mcp-github"

],

"env": {

"GITHUB_TOKEN": "your-github-token"

}

}

}

}
```

### **Step 3：使用示例**

```
帮我查看 GitHub 仓库 my-org/my-project 的最近 5 个 open issues，

然后根据 issue 描述，创建对应的 SpeckitList。
```

**反馈截图如下（由于示例中演示的仓库没有 issue，所以无返回）：**

<img src='images/7-5.png' width=500px />

## 四、配置搜索 MCP Server

```json
{

"mcpServers": {

"duckduckgo-search": {

"command": "npx",

"args": ["-y", "@anthropic/mcp-server-duckduckgo-search"]

}

}

}
```

使用示例：

```
我遇到了这个错误：[粘贴错误信息]

请搜索一下最新的解决方案，然后帮我修复。
```

## 五、常见问题

<details style="margin-bottom: 8px;">

<summary style="color: red; font-weight: 500; cursor: pointer;">如何查看我配置的 MCP 服务器？</summary>

<img src='images/7-7.png' width=500px />

</details>

<details style="margin-bottom: 8px;">

<summary style="color: red; font-weight: 500; cursor: pointer;">MCP 配置出错该如何解决？</summary>

如果你的 MCP 配置文件中存在错误，可在我的 MCP 中查看，点击复制日志后，给到 CodeBuddy 帮助修复。

<img src='images/7-6.png' width=500px />

</details>

<details style="margin-bottom: 8px;">

<summary style="color: red; font-weight: 500; cursor: pointer;">配置好的 MCP 服务如何关闭/使用?</summary>

可点击如下图所示对应的 MCP 服务右侧的按钮，进行关闭/开启操作。

<img src='images/7-8.png' width=500px />

</details>

## 一、传统流程 vs MCP 流程

**传统流程（繁琐）：**

```text
1. 你打开数据库客户端

2. 查看表结构

3. 手动复制到文档

4. 把文档喂给 AI

5. AI 基于文档写代码

6. 发现有遗漏，再回去查...
```

**MCP 流程（丝滑）：**

```text
1. 你说“帮我写用户订单查询接口”

2. AI 自动查询数据库表结构

3. AI 基于真实表结构写代码

4. 一次走通（减少来回补信息）
```

## 二、实战演练

<div style="padding: 10px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px; margin: 10px 0;">

<strong>使用数据：</strong> 在 `data` 文件夹下有一些示例数据库文件，可以用于测试和练习。

</div>

### 场景 1：自动生成 Prisma Schema

```text
请通过 MCP 读取数据库的完整表结构，

然后生成对应的 Prisma Schema 文件（prisma/schema.prisma）。



要求：

1. 正确识别所有外键关系

2. 添加中文注释说明每个字段

3. 添加 @@index 和 @@map 注解

4. 输出“字段来源证据”（说明来自哪张表/字段）
```

### 场景 2：自动生成 CRUD 接口

```text
请读取数据库中 users 表的结构，

然后在 src/app/api/users/ 目录下生成完整的 CRUD 接口：



1. GET /api/users - 列表（分页 + 搜索）

2. GET /api/users/:id - 详情

3. POST /api/users - 创建

4. PUT /api/users/:id - 更新

5. DELETE /api/users/:id - 删除



使用 Prisma 作为 ORM，每个接口有完整的类型安全和错误处理。

并附上每个接口的入参/出参示例。
```

### 场景 3：智能查询生成

```text
我需要一个报表查询：

“统计每个分类下的商品数量、平均价格、总销售额，按总销售额降序排列”。



请先查看相关表结构，确认字段名和关联关系，

然后生成 Prisma 查询代码，并解释每个聚合字段来自哪里。
```

## 三、高级场景：数据库变更自动同步代码

```text
我刚在数据库中给 users 表添加了一个 phone 字段（varchar(20)，可空）。



请：

1. 通过 MCP 确认数据库当前 users 表结构

2. 更新 prisma/schema.prisma 中的 User 模型

3. 更新 src/types/user.ts 中的 TypeScript 类型

4. 更新相关 API（创建和更新接口支持 phone）

5. 更新前端表单组件，添加手机号输入框

6. 输出“变更影响清单 + 回归检查项”
```

**这就是 MCP 的威力：AI 能直接感知数据库变化，并在代码侧同步落地。**

## 练习 1：SQLite MCP 配置（必做）

1. 创建一个包含至少 4 张表的 SQLite 数据库

2. 配置 SQLite MCP Server

3. 让 AI 通过 MCP 读取表结构

4. 让 AI 基于真实表结构生成 Prisma Schema

## 练习 2：MCP 驱动的 CRUD 生成（必做）

1. 基于练习 1 的数据库

2. 让 AI 通过 MCP 自动生成完整的 CRUD 接口

3. 验证生成的代码是否能正确运行

## 练习 3：编写自定义 MCP Server（进阶）

编写一个 MCP Server，提供以下能力之一：

- 读取项目的 Git 历史（最近 20 条 commit）

- 分析项目的依赖树（package.json 的依赖关系）

- 读取 ESLint 检查结果

> **MCP = AI 的"感官延伸"。**

> 

> 没有 MCP，AI 只能看到你给它的文件。

> 有了 MCP，AI 能直接"看到"数据库、"触摸"GitHub、"搜索"互联网。

> AI 从"封闭空间的助手"变成了"连接一切的 Agent"。

### 下一讲预告

> **第 10 讲：终极实战 —— Speckit + Agent 自动完成全栈项目**

> 

> 最后一讲，我们将综合运用前 9 讲所有技能，从 0 到 1 完成一个完整的全栈项目——"AI 驱动的自动化营销看板"，全程不写逻辑代码，只维护 Speckit 和 Agent。

本讲结束时，你应该能做到：

- 说清楚 MCP 的作用、边界与基本工作方式

- 配置并连通一个可用的 MCP Server（例如 SQLite）

- 走通“读取元数据→生成代码→验证”的最小闭环

- 了解自定义 MCP Server 的基本思路

- 明白在密钥、权限与稳定性方面需要注意什么

### 核心收获

> **MCP = AI 的"感官延伸"。**

> 

> 没有 MCP，AI 只能看到你给它的文件。

> 有了 MCP，AI 能直接"看到"数据库、"触摸"GitHub、"搜索"互联网。

> AI 从"封闭空间的助手"变成了"连接一切的 Agent"。

### 下一讲预告

> **第 8 讲：Agent Skills**

> 

> 下一讲将理解 Agent Skills 的核心价值与触发机制，掌握 `SKILL.md` 的基础结构，并能在 CodeBuddy 中完成一次可复现的 Skill 配置与调用。
