> **重要提示**：这些是演示应用程序，仅供本地开发使用，不应部署到生产环境或大规模使用。

本仓库包含多个 [CodeBuddy Agent SDK](https://www.codebuddy.cn/docs/cli/sdk) 的演示项目，展示了使用 CodeBuddy 构建 AI 驱动应用的不同方式。

## 可用示例

### 👋 [快速入门](./quick-start)

一个简单的入门示例，帮助你了解 CodeBuddy Agent SDK 的基础知识。

### 🔄 [V2 会话示例](./v2-session)

展示 V2 Session API 的使用，支持多轮对话和会话恢复。

### 📝 [档案生成器](./profile-builder)

使用网络搜索研究人物背景，自动生成专业简历。

### 💬 [智能聊天演示](./chat-demo)

一个完整的聊天应用，带有 React 前端和 Express 后端，展示 SDK 集成。

### 🔬 [研究助理](./research-assistant)

一个多智能体研究系统，协调专门的子智能体来研究主题并生成综合报告：

- 将研究请求拆分为子主题

- 并行生成研究员智能体搜索网络

- 生成数据可视化图表

- 将发现整合成 PDF 报告

### 📊 [表格助手](./spreadsheet-assistant)

使用 CodeBuddy 处理电子表格和 Excel 文件的演示桌面应用。

### 📧 [邮件助理](./mail-assistant)

一个 IMAP 邮件助理，可以：

- 显示收件箱

- 执行智能搜索来查找邮件

- 提供 AI 驱动的邮件辅助功能

## 快速开始

每个示例都有自己的目录和专门的设置说明。导航到特定的示例文件夹，按照其 README 进行设置和使用。

## 前置条件

- [Bun](https://bun.sh) 运行时（或 Node.js 18+）

- 已安装并认证的 CodeBuddy CLI

## 开始使用

1. **克隆仓库**

```bash
git clone https://cnb.cool/codebuddy/agent-sdk-demos

cd agent-sdk-demos
```

2. **选择一个示例并进入其目录**

```bash
cd quick-start # 或 chat-demo、research-assistant 等
```

3. **按照示例专属的 README** 进行设置和使用

## 资源

- [CodeBuddy Agent SDK 文档](https://www.codebuddy.cn/docs/cli/sdk)

## 支持

这些是按原样提供的演示应用程序。如有问题请参考：

- **CodeBuddy Agent SDK**: [SDK 文档](https://www.codebuddy.cn/docs/cli/sdk)

## 许可证

MIT - 这是用于演示目的的示例代码。

一个简单的示例，演示如何使用 CodeBuddy Agent SDK 创建可以与 CodeBuddy 交互的自主智能体。

## 概述

CodeBuddy Agent SDK 允许您以编程方式构建具有 CodeBuddy 功能的 AI 智能体。SDK 将 CodeBuddy Code 进程作为子进程启动，并与其通信以自主执行任务。

## 安装

```bash
npm install @tencent-ai/agent-sdk typescript @types/node tsx zod
```

## 设置

1. 将您的 CodeBuddy API 密钥设置为环境变量：

```bash
cd quick-start #进入项目文件夹

export CODEBUDDY_API_KEY="your-api-key" # 本教程提供了一个示例的apikey,通过项目文件夹下的key.txt获取
```

2. 创建所需的目录结构：

```bash
mkdir -p agent/custom_scripts
```

`agent` 目录用作 CodeBuddy 智能体的工作目录，`custom_scripts` 是 JavaScript/TypeScript 文件必须写入的位置（由示例中的钩子强制执行）。

## 工作原理

### 基本结构

SDK 使用 `query()` 函数返回消息的异步可迭代对象：

```typescript
import { query } from '@tencent-ai/agent-sdk';



const q = query({

prompt: '您的提示词',

options: { /* 配置 */ }

});



for await (const message of q) {

// 处理消息

}
```

### 关键组件

#### 1. 查询选项

- **`maxTurns`**: 最大对话轮数（默认：100）

- **`cwd`**: 智能体的工作目录（必须存在）

- **`model`**: 使用的模型（`"claude-4.5"`、`"claude-opus-4.5"`、`"claude-haiku-4.5"` 或 `"inherit"`）

- **`executable`**: Node.js 二进制文件路径（使用 `process.execPath` 获取当前运行时）

- **`allowedTools`**: 智能体可以使用的工具名称数组

#### 2. 可用工具

智能体可以使用各种工具，包括：

- **文件操作**: `Read`、`Write`、`Edit`、`MultiEdit`、`NotebookEdit`

- **搜索**: `Glob`、`Grep`、`WebSearch`

- **执行**: `Bash`、`Task`

- **实用工具**: `TodoWrite`、`WebFetch`、`BashOutput`、`KillBash`

- **规划**: `ExitPlanMode`

#### 3. 钩子

钩子允许您拦截和控制工具的使用。示例中包含一个 `PreToolUse` 钩子，强制 `.js` 和 `.ts` 文件只能写入 `custom_scripts` 目录：

```typescript
hooks: {

PreToolUse: [

{

matcher: "Write|Edit|MultiEdit",

hooks: [

async (input: any): Promise<HookJSONOutput> => {

// 验证逻辑

// 返回 { continue: true } 表示允许

// 返回 { decision: 'block', stopReason: '...', continue: false } 表示拒绝

}

]

}

]

}
```

#### 4. 消息类型

SDK 返回三种类型的消息：

- **`system`**: 系统级消息和提示

- **`assistant`**: CodeBuddy 的响应（包含实际消息内容）

- **`result`**: 工具执行结果

提取 CodeBuddy 的文本响应：

```typescript
if (message.type === 'assistant' && message.message) {

const textContent = message.message.content.find((c: any) => c.type === 'text');

if (textContent && 'text' in textContent) {

console.log(textContent.text);

}

}
```

### 架构

1. SDK 将 CodeBuddy Code CLI 进程作为子进程启动

2. 它使用 `executable` 中指定的 Node.js 二进制文件（默认为 `"node"`）

3. 通过 stdin/stdout 与子进程通信

4. 智能体在指定的 `cwd` 目录中运行

5. 钩子可以在执行前拦截和修改工具调用

## 运行示例

```bash
npx tsx quick-start.ts
```

## 常见问题

### "Failed to spawn CodeBuddy Code process: spawn node ENOENT"

**解决方案**: 将 `executable` 选项设置为 `node`：

```typescript
options: {

executable: "node",

// ... 其他选项

}
```

### spawn 时出现 "ENOENT" 错误

**解决方案**: 确保 `cwd` 目录存在：

```bash
mkdir -p agent
```

### 文件操作的权限错误

**解决方案**: 检查您的钩子配置，确保智能体拥有必要的 `allowedTools`。

## 资源

- [CodeBuddy Agent SDK 文档](https://www.codebuddy.cn/docs/cli/sdk)

演示 Session API 的核心能力：**多轮对话上下文保持**。

## 什么是 Session

Session 是 CodeBuddy Agent SDK 中用于多轮对话交互的核心 API，允许在应用程序中维持持久化的对话上下文。

### 与 query() API 的区别

| 特性 | query() API | Session API |

|------|-------------|-------------|

| 多轮对话 | 需要手动管理上下文 | 原生支持 |

| 会话恢复 | 不支持 | 支持（通过 session_id） |

| 运行方式 | 启动本地子进程 | 直接连接云服务 |

| 认证 | 自动（继承 CLI 认证） | 需要先登录 |

### 核心特性

- **上下文保持**：在多轮对话中保留之前的交互历史

- **会话管理**：通过会话 ID 继续或恢复现有对话

- **状态维护**：在整个对话生命周期中维护 Agent 的状态

### 适用场景

| 场景 | 说明 |

|------|------|

| 多轮代码审查 | 初始审查后，用户可以追问具体问题 |

| 交互式调试 | 逐步调试问题，每轮对话基于前面的分析结果 |

| 需求澄清 | 在需求分析过程中进行多轮问答 |

| 代码重构 | 分阶段进行重构，保持整体策略的连贯性 |

## 快速开始

### 1. 安装依赖

```bash
cd multi-turn-session # 进入示例目录

npm install
```

### 2. 配置认证

Session API 直接连接云服务，需要配置 API Key。

**获取 API Key：**

| 版本 | 获取地址 |

|------|---------|

| 海外版 | https://www.codebuddy.ai/profile/keys |

| 中国版 | https://copilot.tencent.com/profile/iOA |

**设置环境变量：**

```bash
# 海外版

export CODEBUDDY_API_KEY="your-api-key"



# 中国版（需额外设置环境标识）

export CODEBUDDY_API_KEY="your-api-key"

export CODEBUDDY_INTERNET_ENVIRONMENT=internal
```

### 3. 运行示例

```bash
npx tsx examples.ts basic # 基础会话

npx tsx examples.ts multi-turn # 多轮对话（核心场景）

npx tsx examples.ts one-shot # 单次查询便捷函数

npx tsx examples.ts resume # 会话恢复
```

## API 用法

```typescript
import {

unstable_v2_createSession,

unstable_v2_resumeSession,

unstable_v2_prompt,

} from '@tencent-ai/agent-sdk';



// 创建会话（使用 await using 自动关闭）

await using session = unstable_v2_createSession({ model: 'claude-4.5' });



// 发送消息并接收响应

await session.send('你好！');

for await (const msg of session.stream()) {

// 处理消息

}



// 恢复已有会话

await using session = unstable_v2_resumeSession(sessionId, { model: 'claude-4.5' });



// 单次查询（直接返回结果，无需管理会话）

const result = await unstable_v2_prompt('问题？', { model: 'claude-4.5' });
```

## 示例说明

### basic - 基础会话

演示最基本的会话创建和消息收发流程。

### multi-turn - 多轮对话

Session 的核心价值演示：智能体在多轮对话中自动保持上下文，后续问题可以引用前面的对话内容。

### one-shot - 单次查询

适合不需要多轮交互的简单场景，`unstable_v2_prompt()` 直接返回结果。

### resume - 会话恢复

演示如何跨会话保持上下文：关闭会话后，使用会话 ID 恢复，智能体仍然记得之前的对话内容。

使用 CodeBuddy Agent SDK 和网络搜索功能生成专业简历。

## 功能

- 使用网络搜索研究一个人（LinkedIn、公司页面、新闻、GitHub）

- 生成专业的单页简历，格式为 `.docx` 文件

- 使用 `docx` 库生成 Word 文档

## 使用方法

```bash
cd profile-builder #进入示例文件夹

npm install

npm start "人名"
```

## 工作原理

1. 使用 `WebSearch` 研究此人的职业背景

2. 收集有关其当前职位、过往经历、教育背景和技能的信息

3. 生成一个使用 `docx` 库创建简历的 JavaScript 文件

4. 执行脚本生成 `.docx` 文件

## 输出

生成的简历保存到 `agent/custom_scripts/resume.docx`

一个使用 CodeBuddy Agent SDK 的演示聊天应用，带有 React 前端和 Express 后端。

<img src='images/diagram.png' width=800px />

## 开始使用

### 前置条件

- Node.js 18+

- CodeBuddy Agent SDK 凭据（设置 `CODEBUDDY_API_KEY` 环境变量）

### 安装

```bash
cd chat-demo # 进入示例目录

npm install
```

### 运行

```bash
npm run dev
```

这将同时启动：

- **后端**（Express + WebSocket）在 http://localhost:3001

- **前端**（Vite + React）在 http://localhost:5173

在浏览器中打开 http://localhost:5173。

## 生产环境注意事项

这是一个用于演示目的的示例应用。对于生产使用，请考虑：

1. **隔离 Agent SDK** - 将 SDK 移到单独的容器/服务中。这提供更好的安全隔离，因为智能体可以访问 Bash、文件系统操作和网络请求等工具。

2. **持久化存储** - 用数据库替换内存中的 `ChatStore`。目前所有聊天在服务器重启时都会丢失。

3. **会话记录同步** - 为了使 Agent Sessions 在服务器重启后持久化，您需要持久化和恢复 SDK 的对话记录。SDK 维护多轮对话的内部状态，必须与您的存储同步。

4. **身份验证** - 添加用户身份验证和授权。目前任何人都可以访问任何聊天。

一个多智能体研究系统，协调专门的子智能体来研究任何主题，并生成带有数据可视化的综合 PDF 报告。

## 快速开始

```bash
# 进入示例目录



cd research-assistant



# 安装依赖



uv sync



# 设置 API 密钥

export CODEBUDDY_API_KEY="your-api-key"



# 运行智能体

uv run python research_agent/agent.py
```

然后输入："研究 2025 年的量子计算发展"

## 工作原理

1. **主智能体**将您的请求拆分为 2-4 个子主题

2. 并行生成**研究员**子智能体搜索网络

3. 每个研究员将发现保存到 `files/research_notes/`

4. 生成**数据分析师**提取指标并在 `files/charts/` 中生成图表

5. 生成**报告撰写者**在 `files/reports/` 中创建最终 PDF 报告

## 智能体

| 智能体 | 工具 | 用途 |

|--------|------|------|

| **主智能体** | `Task` | 协调研究，委派给子智能体 |

| **研究员** | `WebSearch`、`Write` | 从网络收集信息 |

| **数据分析师** | `Glob`、`Read`、`Bash`、`Write` | 提取指标，生成图表 |

| **报告撰写者** | `Skill`、`Write`、`Glob`、`Read`、`Bash` | 创建带有嵌入式可视化的 PDF 报告 |

## 斜杠命令

| 命令 | 描述 |

|------|------|

| `/research <主题>` | 开始对任何主题进行重点研究 |

| `/competitive-analysis <公司>` | 分析公司或产品 |

| `/market-trends <行业>` | 研究行业趋势 |

| `/fact-check <声明>` | 验证声明和陈述 |

| `/summarize` | 总结所有当前研究发现 |

## 示例查询

- "研究量子计算的发展"

- "可再生能源的当前趋势是什么？"

- `/competitive-analysis 特斯拉`

- `/market-trends 人工智能`

## 输出结构

```
files/

├── research_notes/ # 研究员的 Markdown 文件

├── data/ # 分析师的数据摘要

├── charts/ # PNG 可视化图表

└── reports/ # 最终 PDF 报告



logs/

└── session_YYYYMMDD_HHMMSS/

├── transcript.txt # 人类可读的对话记录

└── tool_calls.jsonl # 结构化的工具使用日志
```

## 使用钩子跟踪子智能体

系统使用 SDK 钩子跟踪所有工具调用。

### 跟踪内容

- **谁**：哪个智能体（RESEARCHER-1、DATA-ANALYST-1 等）

- **什么**：工具名称（WebSearch、Write、Bash 等）

- **何时**：时间戳

- **输入/输出**：参数和结果

### 工作原理

钩子在执行前后拦截每个工具调用：

```python
hooks = Hooks(

pre_tool_use=[tracker.pre_tool_use_hook],

post_tool_use=[tracker.post_tool_use_hook]

)
```

`parent_tool_use_id` 将工具调用链接到其子智能体：

- 主智能体通过 `Task` 工具生成研究员 → 获得 ID "task_123"

- 该研究员的所有工具调用都包含 `parent_tool_use_id = "task_123"`

- 钩子使用此 ID 识别是哪个子智能体发起的调用

### 日志输出

**transcript.txt** - 人类可读：

```
[RESEARCHER-1] → WebSearch

输入: query='量子计算 2025'

[DATA-ANALYST-1] → Bash

输入: python matplotlib 图表生成
```

**tool_calls.jsonl** - 结构化 JSON：

```json
{"event":"tool_call_start","agent_id":"RESEARCHER-1","tool_name":"WebSearch",...}

{"event":"tool_call_complete","success":true,"output_size":15234}
```

> **重要提示**：这是一个演示应用程序，仅供本地开发使用，不应部署到生产环境或大规模使用。

一个由 CodeBuddy 和 [CodeBuddy Agent SDK](https://www.codebuddy.cn/docs/cli/sdk) 驱动的演示 Web 应用程序，展示了 AI 驱动的电子表格创建、分析和操作功能。

## 本演示展示的内容

这个基于 Web 的应用程序演示了如何：

- 创建带有公式、格式和多个工作表的复杂 Excel 电子表格

- 分析和操作现有电子表格数据

- 使用 CodeBuddy 协助数据组织和电子表格设计

- 使用 Python 脚本生成复杂的电子表格结构

- 将 CodeBuddy Agent SDK 与桌面应用程序集成

### 示例用例

`agent/` 文件夹包含 Python 示例，包括：

- **健身追踪器**：带有自动汇总统计和多个工作表的健身日志

- **预算追踪器**：带有公式和数据验证的财务跟踪

- 带有样式、边框和条件格式的自定义电子表格生成

## 前置条件

- [Node.js 18+](https://nodejs.org)

- CodeBuddy API 密钥

- Python 3.9+（用于 Python 智能体示例）

- LibreOffice（可选，用于公式重新计算）

## Web 应用程序示例

1. 安装依赖：

```bash
cd spreadsheet-assistant-web

npm install
```

2. 配置您的 CodeBuddy API 密钥：
- 复制 `.env.example` 到 `.env`

- 在 `.env` 文件中设置 `CODEBUDDY_API_KEY`
3. 运行 Web 应用程序：

```bash
# 开发模式（热重载）

npm run dev



# 生产模式

npm run build

npm start
```

应用将在 `3000`端口 运行。

<img src='images/image.png' width='800'>

## 功能

- **AI 驱动的电子表格生成**：让 CodeBuddy 根据您的需求创建复杂的电子表格

- **公式管理**：处理 Excel 公式、计算和自动重新计算

- **专业样式**：生成带有标题、颜色、边框和格式的电子表格

- **多工作表工作簿**：创建包含多个相关工作表的工作簿

- **数据分析**：分析现有电子表格并提取见解

- **文件上传支持**：支持上传 Excel (.xlsx, .xls)、PDF、Word (.docx, .doc) 文档进行分析

- **实时通信**：基于 WebSocket 的实时 AI 响应

- **Web 访问**：通过浏览器访问，支持跨平台使用

## 项目结构

```
spreadsheet-assistant/

├── agent/ # Python 示例和 Excel 智能体设置

│ ├── create_workout_tracker.py

│ ├── create_budget_tracker.py

│ └── README.md # Excel 智能体文档

├── src/

│ ├── client/ # React 前端组件

│ └── server/ # Express 后端服务器

├── dist/ # 构建输出目录

└── package.json
```

## 使用 Python 示例

`agent/` 目录包含演示电子表格生成的 Python 脚本：

### 设置 Python 环境

```bash
cd agent

python -m venv .venv

source .venv/bin/activate # Windows 上：.venv\\Scripts\\activate

pip install -r requirements.txt
```

### 运行示例脚本

```bash
# 创建健身追踪器

python create_workout_tracker.py



# 创建预算追踪器

python create_budget_tracker.py
```

有关 Excel 智能体设置和功能的更多详细信息，请参阅 [agent/README.md](./agent/README.md)。

## 资源

- [CodeBuddy Agent SDK 文档](https://www.codebuddy.cn/docs/cli/sdk)

- [React 文档](https://react.dev/)

- [Express 文档](https://expressjs.com/)

- [Vite 文档](https://vitejs.dev/)

- [openpyxl 文档](https://openpyxl.readthedocs.io/)（使用的 Python 库）

## 支持

这是一个按原样提供的演示应用程序。如有问题请参考：

- **CodeBuddy Agent SDK**: [SDK 文档](https://www.codebuddy.cn/docs/cli/sdk)

## 许可证

MIT - 这是用于演示目的的示例代码。

---

构建于 [CodeBuddy Agent SDK](https://www.codebuddy.cn/docs/cli/sdk)

> **重要提示**：这是一个演示应用程序，仅供本地开发使用，不应部署到生产环境或大规模使用。

一个由 CodeBuddy 和 CodeBuddy Agent SDK 驱动的演示邮件客户端，展示了 AI 驱动的邮件管理功能。

## 架构

<img src='images/architecture.png' width=800px />

## 🔒 安全警告

**此应用程序仅应在您的个人电脑上本地运行。** 它：

- 以纯文本环境变量存储邮件凭据

- 没有身份验证或多用户支持

- 不是为生产安全标准设计的

## 前置条件

- [Bun](https://bun.sh) 运行时（或 Node.js 18+）

- 已安装并认证的 CodeBuddy CLI

- 启用了 IMAP 访问的邮箱账户

## 安装

1. 克隆仓库：

```bash
git clone https://cnb.cool/codebuddy/agent-sdk-demos

cd codebuddy-agent-sdk-demos/mail-assistant
```

2. 安装依赖：

```bash
bun install

# 或 npm install
```

3. 创建环境文件：

```bash
cp .env.example .env
```

4. 在 `.env` 中配置您的凭据（参见下方 IMAP 设置）

5. 运行应用程序：

```bash
bun run dev

# 或 npm run dev
```

6. 在浏览器中打开 `http://localhost:3000`

## IMAP 设置指南

### Gmail 设置

Gmail 需要使用**应用专用密码**而非您的常规密码：

1. **启用两步验证**（应用专用密码的前提条件）：
- 前往 [Google 账户安全](https://myaccount.google.com/security)

- 点击"两步验证"并按照步骤设置
2. **生成应用专用密码**：
- 前往 [Google 应用专用密码](https://myaccount.google.com/apppasswords)

- 从下拉菜单中选择"邮件"

- 选择您的设备（或选择"其他"并命名为"Email Agent"）

- 点击"生成"

- **复制 16 位密码**（您不会再次看到它！）
3. **配置 `.env`**：

```env
EMAIL_USER=your-email@gmail.com

EMAIL_PASSWORD=your-16-char-app-password # 不是您的常规密码！

IMAP_HOST=imap.gmail.com

IMAP_PORT=993
```

## 支持

这是一个按原样提供的演示应用程序。如有问题请参考：

- **CodeBuddy Agent SDK**: [SDK 文档](https://www.codebuddy.cn/docs/cli/sdk)

## 许可证

MIT 许可证 - 这是用于演示目的的示例代码。

---

构建于 [CodeBuddy Agent SDK](https://www.codebuddy.cn/docs/cli/sdk)
