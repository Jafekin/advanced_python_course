# 第八讲：Agent 系统开发

> **设计说明**：本 PPT 共 38 张 Slide，聚焦概念与原理讲解，代码细节全部放到 notebook 中演示。每张 Slide 标注了对应的 notebook cell 编号，方便课堂对照。
>
> **使用约定**：标 `[notebook cX]` 表示对应 notebook 的第 X 个 cell。

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 6 讲
**副标题**：Agent 系统开发——从 RAG 到智能体
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航  `[notebook c1]`

**五大 Part，配套 Vibe Coding 工具：**

| Part | 主题 | 关键概念 | Vibe Coding 工具 |
|---|---|---|---|
| Part 1 | 从 RAG 到 Agent | 局限性 / 三大组件 / ReAct | Spec-driven |
| Part 2 | 工具调用 | Function Calling / 工具描述 | Prompt 工程延伸 |
| Part 3 | ReAct Agent 实战 | Agent / 记忆 / Gradio | Inline Edit + @文件 |
| Part 4 | 多 Agent 与协议 | MCP / A2A / ANP | 上下文工程 |
| Part 5 | Skill + 总结 | Skill 写法 / 工具链回顾 | 全工具链回顾 |

> 完成标准：能基于 LangChain 构建一个带 RAG 工具 + 多轮对话记忆的 Gradio 智能问答助手

---

### Slide 3｜承上启下：八讲完整路径

```
第1讲 数据处理 + Vibe Coding 入门  →  会用 Pandas + 会与 AI 对话
第2讲 数据可视化 + AI 辅助表达    →  会用 Matplotlib/Seaborn + AI 迭代
第3讲 Spec-driven + Python 工程化 →  会写规约 + 模块化/测试/质量
第4讲 NLP 基础 + Prompt 工程      →  会调 API + 会写 Prompt
第5讲 NLP 进阶 + 模型微调         →  能微调 BERT + 理解 Transformer
第6讲 大模型部署 + RAG 基础       →  能部署模型 + 能搭 RAG 流水线
第7讲 RAG 进阶 + Agent 记忆       →  高级检索 + 记忆系统
第8讲 Agent 系统开发（本讲）      →  能开发完整 AI 应用
```

**本讲完成最后一跃**：
- 第6-7讲 RAG："给我一篇文档，我帮你找答案"——**被动检索**
- 第8讲 Agent："给我一个目标，我自己想办法完成"——**主动行动**

---

## Part 1：从 RAG 到 Agent（概念原理） `[notebook c5-c8]`

### Slide 4｜RAG 的局限性  `[notebook c6]`

**回顾第6-7讲：RAG 问答系统的流水线**

```
用户提问 → 向量检索 → 拼 Prompt → LLM 生成回答
```

**但 RAG 有三个"不能"**：

| 能力 | RAG | Agent |
|---|---|---|
| 查资料 | 能（向量检索） | 能（RAG 作为工具之一） |
| 做计算 | ❌ 不能 | ✅ 能（调用计算器工具） |
| 多步推理 | ❌ 不能 | ✅ 能（ReAct 循环） |
| 自主决策 | ❌ 不能 | ✅ 能（决定用哪个工具） |
| 执行动作 | ❌ 不能 | ✅ 能（调 API、写文件） |

> 核心洞察：**RAG 是 Agent 的一个"器官"，不是 Agent 本身**

---

### Slide 5｜什么是 Agent？定义与架构

**定义**：Agent（智能体）是一个能够**感知环境 → 自主决策 → 执行行动 → 观察反馈**的闭环系统。

```
                    ┌──────────────┐
                    │   用户目标    │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │  LLM（大脑）  │ ◄── 规划（Planning）
                    └──────┬───────┘
                     ┌─────┼─────┐
                     ▼     ▼     ▼
                  ┌────┐┌────┐┌────┐
                  │工具1││工具2││工具3│ ◄── 工具（Tools）
                  └────┘└────┘└────┘
                           ▼
                    ┌──────────────┐
                    │   记忆系统    │ ◄── 记忆（Memory）
                    └──────────────┘
```

**公式**：`Agent = LLM + Tools + Memory + Planning`

---

### Slide 6｜Agent 三大组件详解  `[notebook c7]`

| 组件 | 功能 | 类比 | 课程来源 |
|---|---|---|---|
| **规划（Planning）** | 任务拆解、推理决策、行动排序 | 大脑的"前额叶" | 第3讲 Prompt 工程延伸 |
| **工具（Tools）** | 执行具体动作（搜索、计算、API） | 人的"双手" | 第6-7讲 RAG 封装为工具 |
| **记忆（Memory）** | 保存对话历史、学习经验 | 人的"海马体" | 第6-7讲 Memory 概念落地 |

**第6-7讲已经准备好了什么？**
- RAG 流水线 → Agent 的**检索工具**
- Memory 系统概念 → Agent 的**记忆组件**
- Ollama 本地 LLM → Agent 的**大脑**

> 本讲做的是"组装"——把第6-7讲的零件拼成一个完整的 Agent

---

### Slide 7｜ReAct 范式：推理-行动循环  `[notebook c8]`

**ReAct = Reasoning + Acting**（Yao et al., ICLR 2023）

**核心思想**：把"思考"和"行动"显式结合，模仿人类解题过程

```
     ┌──────────────────────────────────┐
     │  Thought 1: 分析问题，决定行动     │
     └────────────┬─────────────────────┘
                  ▼
     ┌──────────────────────────────────┐
     │  Action 1: 调用工具                │
     └────────────┬─────────────────────┘
                  ▼
     ┌──────────────────────────────────┐
     │  Observation 1: 工具返回结果       │
     └────────────┬─────────────────────┘
                  ▼
          （结果追加到上下文）
                  ▼
     ┌──────────────────────────────────┐
     │  Thought 2: 基于观察，下一步...    │
     └────────────┬─────────────────────┘
                  ▼
              ... 循环 ...
                  ▼
     ┌──────────────────────────────────┐
     │  Final Answer: 最终回答            │
     └──────────────────────────────────┘
```

> 关键：思考指导行动，行动的结果又反过来修正思考

---

### Slide 8｜ReAct vs Plan-and-Execute 两种范式

**两种规划策略对比**：

| 范式 | 策略 | 流程 | 适用场景 | 类比 |
|---|---|---|---|---|
| **ReAct** | 边想边做 | Thought→Action→Observation 循环 | 信息不完整、需探索 | 即兴演讲 |
| **Plan-and-Execute** | 先想后做 | 先规划完整计划，再逐步执行 | 目标明确、步骤清晰 | 写论文按大纲 |

**Plan-and-Execute 流程**：
```
[规划阶段] Plan: Step1 → Step2 → Step3 → Step4
[执行阶段] Execute Step1 ✓ → Step2 ✓ → Step3 ✓ → Step4 ✓
```

> 本讲实战选用 **ReAct**：更适合"基于文档问答"这种探索性场景

---

## Part 2：工具调用（概念原理） `[notebook c9-c17]`

### Slide 9｜Function Calling：LLM 如何调用工具

**传统方式 vs Function Calling**：

```
传统方式（第3讲）：
  用户 → LLM → 纯文本回答（LLM 不知道有工具可用）

Function Calling（本讲）：
  用户 → LLM → "我需要调用 search 工具" → 执行工具 → 结果回传 LLM → 最终回答
```

**本质区别**：
- 传统：LLM 只能"说话"
- Function Calling：LLM 能"做事"——通过返回结构化 JSON 告诉程序该调哪个工具

> 这是 Agent 能力的基石：没有 Function Calling，就没有 Agent

---

### Slide 10｜Function Calling 完整 5 步流程

```
Step 1: 用户提问 + 工具定义 一起发给 LLM
         ↓
Step 2: LLM 判断"需要调用工具"，返回工具名 + 参数（JSON）
         ↓
Step 3: 程序解析 JSON，执行对应的函数
         ↓
Step 4: 函数返回结果，回传给 LLM（作为 tool 消息）
         ↓
Step 5: LLM 基于工具结果生成最终回答
```

**关键点**：
- Step 2 中 LLM **不是返回文本，而是返回结构化的 tool_calls**
- Step 3 的执行权在**程序**手里，不是 LLM 直接执行
- Step 4 的结果必须回传，否则 LLM 会"以为自己做了但没做"

---

### Slide 11｜工具三要素  `[notebook c13]`

**每个工具必须包含三个信息**：

| 要素 | 说明 | 示例 |
|---|---|---|
| **名称（Name）** | 唯一标识符，LLM 在 Action 中引用 | `rag_search` |
| **描述（Description）** | 自然语言说明用途，**是 LLM 决策的关键依据** | "从航天产业报告中检索相关段落" |
| **执行逻辑（Function）** | 实际执行的 Python 函数 | `def rag_search(query): ...` |

**OpenAI Function Calling 的 JSON Schema**（概念）：

```json
{
  "name": "rag_search",
  "description": "从航天产业报告中检索与用户问题相关的段落",
  "parameters": {
    "type": "object",
    "properties": { "query": {"type": "string"} },
    "required": ["query"]
  }
}
```

> LangChain 的 `@tool` 装饰器会自动从 docstring 提取这些信息

---

### Slide 12｜工具描述的"Prompt 工程"  `[notebook c15]`

**工具描述 = 写给模型看的"使用说明书"**

| 维度 | 坏描述 | 好描述 |
|---|---|---|
| 内容 | "搜索工具" | "从航天产业报告中检索相关段落。当用户提问涉及航天数据、发射次数、企业信息时使用。" |
| 问题 | LLM 不知道什么时候该用 | LLM 清楚使用场景 |
| 后果 | 不该调时调，该调时不调 | 精准匹配用户意图 |

**工具描述的黄金法则**：
1. 说清楚**做什么**（功能）
2. 说清楚**什么时候用**（触发条件）
3. 说清楚**输入什么、输出什么**（参数语义）
4. 说清楚**不能做什么**（边界）

> Vibe Coding 视角：工具描述是 Prompt 工程从"对话层"到"工具层"的延伸

---

### Slide 13｜LangChain 工具定义三种方式（概念对比）

| 方式 | 语法 | 适用场景 | 代码量 |
|---|---|---|---|
| **@tool 装饰器** | `@tool` + docstring | 简单工具，快速定义 | 最少 |
| **BaseTool 子类** | 继承 `BaseTool` + `args_schema` | 复杂工具，需严格类型校验 | 中等 |
| **bind_tools** | `llm.bind_tools([tool1, tool2])` | 把工具绑定到 LLM | 一行 |

**三者关系**（不是三选一，而是组合使用）：

```
@tool / BaseTool  →  定义工具
        ↓
bind_tools        →  把工具绑到 LLM 上
        ↓
LLM 就能在回答时决定调用哪个工具
```

> 详见 notebook c14、c17 的代码演示

---

### Slide 14｜消息角色全景

| 角色 | 作用 | 示例 |
|---|---|---|
| `system` | 设定 Agent 行为规约 | "你是航天产业分析助手..." |
| `human` / `user` | 用户输入 | "2024年中国航天发射次数？" |
| `ai` / `assistant` | LLM 回复（可能含 tool_calls） | tool_calls: [{"name": "rag_search", ...}] |
| `tool` | 工具执行结果 | "根据报告，2024年完成约70次发射..." |

**消息流是 Agent 的"神经系统"**：

```
system → human → ai(tool_calls) → tool → ai(最终回答)
                                         ↑
                                    基于工具结果生成
```

> 所有信息通过消息传递，Agent 的每一步决策都基于消息历史

---

## Part 3：ReAct Agent 从零构建 `[notebook c18-c38]`

### Slide 15｜构建路线图  `[notebook c18]`

```
Step 1: 准备 LLM（复用第6-7讲 Ollama）         [c11-c12]
   ↓
Step 2: 构建 RAG 知识库（复用第6-7讲流水线）    [c19-c23]
   ↓
Step 3: 封装 RAG 工具 + 计算器工具            [c24-c26]
   ↓
Step 4: 构建 ReAct Agent（LangChain）         [c27-c28]
   ↓
Step 5: 测试 Agent（3个用例）                 [c29-c31]
   ↓
Step 6: 添加多轮对话记忆                      [c32-c34]
   ↓
Step 7: 上下文窗口管理                        [c35-c36]
   ↓
Step 8: Gradio 交互界面（最终交付物）         [c37-c38]
```

> 每一步都在前一步基础上叠加能力，从"能调用工具"到"能记住对话"到"能交互使用"

---

### Slide 16｜Step 1：LLM 作为 Agent 的大脑  `[notebook c11-c12]`

**核心概念**：Ollama 本地 LLM = Agent 的"大脑"

```
ChatOpenAI (LangChain)
    │
    ├─ model: qwen2.5:7b-instruct-q4_K_M
    ├─ base_url: http://localhost:11434/v1  ← Ollama 本地服务
    ├─ api_key: "ollama"                    ← Ollama 不需要真实 key
    └─ temperature: 0                       ← Agent 需要确定性输出
```

**与第3讲的区别**：

| 维度 | 第3讲（纯 LLM） | 第8讲（Agent 大脑） |
|---|---|---|
| 角色 | 回答问题 | 决策调用哪个工具 |
| 输出 | 纯文本 | 可能是 tool_calls（JSON） |
| 温度 | 可高可低 | 建议 0（要稳定决策） |

> 关键：temperature=0 让 Agent 的决策可复现——同样的输入应该走同样的工具路径

---

### Slide 17｜Step 2：RAG 知识库构建原理  `[notebook c19-c23]`

**复用第6-7讲流水线**（不重新发明轮子）：

```
航天产业报告.pdf
       ↓ markitdown 转换
    纯文本
       ↓ 递归字符分块
    文本块列表（chunk_size=500, overlap=100）
       ↓ sentence-transformers 向量化
    嵌入向量列表
       ↓ ChromaDB 存储
    向量数据库（可检索）
```

**为什么需要分块？（回顾第6-7讲原理）**：
- 嵌入模型有 512 token 限制
- 大段稀释语义
- 检索精度更高
- Prompt 长度可控

> 详见 notebook c20-c23 的完整代码实现

---

### Slide 18｜递归字符分块原理  `[notebook c22]`

**核心思想**：按分隔符优先级递归切分，保留语义边界

```
分隔符优先级（从高到低）:
  \n\n  →  \n  →  。  →  ；  →  空格  →  强制切分

文本: "第一章 概述\n\n商业航天是...\n\n第二章 数据\n\n2024年发射..."
       ↓ 按 \n\n 切
块1: "第一章 概述"（太短，合并）
块2: "商业航天是..."（500字以内，保留）
块3: "第二章 数据"（合并）
块4: "2024年发射..."（保留）
```

**overlap（重叠窗口）的作用**：
- 块之间保留 100 字重叠
- 避免关键信息被切到两个块之间丢失
- 提高检索的上下文完整性

---

### Slide 19｜向量化与 ChromaDB 存储原理  `[notebook c23]`

**向量化**：把文本变成高维向量（可计算相似度）

```
"2024年航天发射" → [0.12, -0.34, 0.56, ...]  （384维）
"商业航天发展"   → [0.15, -0.31, 0.52, ...]  （384维）
                                         ↑
                              语义相近 → 向量相近
```

**ChromaDB 四要素**（回顾第6-7讲）：

| 要素 | 类比 SQL | 说明 |
|---|---|---|
| `collection` | 表 | 向量库的命名空间 |
| `document` | 行 | 原始文本 |
| `embedding` | 索引 | 向量（用于相似度搜索） |
| `metadata` | 列 | 附加信息（来源、页码等） |

> 本实验用内存模式 `chromadb.Client()`，生产环境用 `PersistentClient` 持久化

---

### Slide 20｜Step 3：封装 RAG 工具  `[notebook c24-c26]`

**把检索能力变成 Agent 可调用的工具**：

```
RAG 流水线（函数）              LangChain Tool
─────────────────              ─────────────
def rag_search(query):    →   @tool
  embed = encode(query)       def rag_search(query):
  results = collection.query      """工具描述..."""
  return results                 # 原检索逻辑
                                 return results
```

**工具列表组合**：

| 工具名 | 功能 | 触发场景 |
|---|---|---|
| `rag_search` | 检索航天报告 | 用户问航天事实 |
| `calculator` | 数学计算 | 需要数值运算 |

> 详见 notebook c25-c26 的 `@tool` 定义和工具列表组装

---

### Slide 21｜Step 4：构建 ReAct Agent  `[notebook c27-c28]`

**LangChain 的两个核心组件**：

| 组件 | 作用 | 类比 |
|---|---|---|
| `create_react_agent` | 创建 ReAct 推理逻辑 | Agent 的"大脑皮层" |
| `AgentExecutor` | 运行 Agent，管理循环 | Agent 的"执行神经" |

**AgentExecutor 的关键参数**：

| 参数 | 作用 | 推荐值 |
|---|---|---|
| `verbose` | 打印推理过程 | `True`（教学用） |
| `max_iterations` | 最大推理步数 | `5`（防止无限循环） |
| `handle_parsing_errors` | 解析失败时容错 | `True`（必开） |

> `max_iterations` 是 Agent 的"安全阀"——防止 Agent 在错误中无限循环

---

### Slide 22｜ReAct Prompt 模板结构  `[notebook c28]`

**ReAct 的 Prompt 必须包含格式说明**（让 LLM 按固定格式输出）：

```
你是一个航天产业分析助手。

你可以使用以下工具：{tools}

请严格按照以下格式回答：
Question: 用户的问题
Thought: 分析问题，决定下一步行动
Action: 工具名称（必须是以下之一：{tool_names}）
Action Input: 工具的输入参数
Observation: 工具返回的结果
... （可重复）
Thought: 我已经有了足够信息
Final Answer: 最终回答

开始！
Question: {input}
{agent_scratchpad}
```

**三个占位符的作用**：
- `{tools}` / `{tool_names}`：注入工具列表
- `{input}`：用户问题
- `{agent_scratchpad}`：Agent 的"草稿本"——累积的 Thought/Action/Observation

---

### Slide 23｜Agent 运行机制：决策过程  `[notebook c29-c31]`

**为什么 Agent 知道要调用 rag_search 而不是 calculator？**

```
用户问题: "2024年中国商业航天的发射情况如何？"
                    ↓
LLM 看到工具描述:
  - rag_search: "从航天产业报告中检索...航天数据、发射次数..."  ← 匹配！
  - calculator: "执行数学计算...加减乘除..."                  ← 不匹配
                    ↓
LLM 决策: 调用 rag_search
```

**这就是为什么 Part 2 反复强调：工具描述 = 写给模型的 Prompt**

**三个测试用例的决策路径**（见 notebook c29-c31）：

| 测试 | 问题类型 | Agent 决策路径 |
|---|---|---|
| 测试1 | 纯检索 | rag_search → 回答 |
| 测试2 | 纯计算 | calculator → 回答 |
| 测试3 | 多步推理 | rag_search → calculator → 回答 |

---

### Slide 24｜Step 6：多轮对话记忆  `[notebook c32-c34]`

**问题**：默认 Agent 是"金鱼记忆"——每次调用都从零开始

**解决方案**：用 `ChatMessageHistory` + `RunnableWithMessageHistory` 包装

```
用户: "报告中提到了哪些航天企业？"     → Agent 回答 A
                                        ↓ 存入 history
用户: "这些企业中哪个最活跃？"         → Agent 看 history
    ↑                                       ↓
    理解"这些企业"指代第1轮的结果    结合上下文回答 B
```

**Session 隔离机制**：

```
session_id = "user_001"  → 独立的 history
session_id = "user_002"  → 另一个独立的 history
```

> 不同用户的对话互不干扰——这是生产环境的基础要求

---

### Slide 25｜上下文窗口管理  `[notebook c35-c36]`

**问题**：对话越来越长，Token 会爆

```
4K tokens ≈ 3000 汉字 ≈ 10轮简单对话
8K tokens ≈ 6000 汉字 ≈ 20轮简单对话
```

**三种管理策略对比**：

| 策略 | 原理 | 优点 | 缺点 |
|---|---|---|---|
| **滑动窗口** | 只保留最近 N 轮 | 简单 | 丢失早期信息 |
| **Token 截断** | 保留最近 K 个 token | 精确控制 | 可能切断语义 |
| **摘要压缩** | LLM 把旧对话总结 | 保留要点 | 增加 LLM 调用成本 |

**工程建议**：
- 教学/演示：滑动窗口（最简单）
- 生产环境：Token 截断 + 始终保留 system message
- 长期对话：摘要压缩 + 向量化存储

> 详见 notebook c36 的 `trim_messages` 演示

---

### Slide 26｜Step 8：Gradio 交互界面  `[notebook c37-c38]`

**Gradio = 快速构建 ML/AI 应用的 Web 界面**

```
┌─────────────────────────────────────┐
│     航天产业智能问答助手             │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │  对话窗口（Chatbot）         │   │
│  │  用户: 2024年航天发射？      │   │
│  │  Agent: 根据报告，约70次...  │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │  输入框 + 发送按钮           │   │
│  └─────────────────────────────┘   │
│  [发送]  [清除对话]                 │
│  示例: 2024年发展趋势？             │
└─────────────────────────────────────┘
```

**界面要素**：
- Chatbot 窗口（展示多轮对话）
- 输入框 + 发送按钮
- 清除对话按钮（重置 history）
- 示例问题（降低使用门槛）

> 这是课程的最终交付物——学生能拿出一个"能用的 AI 应用"

---

### Slide 27｜完整 Agent 架构图（总结）

```
                    ┌─────────────────────────────┐
                    │      Gradio 界面             │
                    │  用户输入 ←→ 对话展示        │
                    └────────────┬────────────────┘
                                 │
                    ┌────────────▼────────────────┐
                    │   AgentExecutor              │
                    │   (ReAct 推理循环)            │
                    │                              │
                    │  Thought → Action →          │
                    │  Observation → ... →          │
                    │  Final Answer                │
                    └───┬──────────┬──────────┬───┘
                        │          │          │
                   ┌────▼───┐ ┌───▼────┐ ┌──▼──────┐
                   │  LLM   │ │ Tools  │ │ Memory  │
                   │(Ollama)│ │        │ │         │
                   │ qwen2.5│ │rag     │ │ chat    │
                   │        │ │search  │ │ history │
                   │        │ │calc    │ │         │
                   └────────┘ └───┬────┘ └─────────┘
                                  │
                          ┌───────▼───────┐
                          │  ChromaDB     │
                          │  向量数据库    │
                          │ (航天产业报告) │
                          └───────────────┘
```

> 从第1讲的 Pandas 到现在的完整 Agent——八讲的积累都在这张图里

---

## Part 4：多 Agent 协作与通信协议 `[notebook c39-c43]`

### Slide 28｜为什么需要多 Agent？  `[notebook c40]`

**单 Agent 的局限**：

```
用户: "帮我调研商业航天行业，写一份分析报告"

单 Agent 需要：搜索资料 → 整理数据 → 分析趋势 → 撰写报告 → 检查质量
全部由一个 Agent 完成 → 容易出错、效率低、上下文爆
```

**多 Agent 的优势**：

```
研究员 Agent: 搜索和整理资料      ──→ 把资料传给分析师
分析师 Agent: 数据分析和趋势判断  ──→ 把分析结果传给撰写员
撰写员 Agent: 撰写报告            ──→ 把报告传给审核员
审核员 Agent: 检查质量和修改建议  ──→ 最终交付
```

> 类比人类团队：分工明确、各司其职、协作完成

---

### Slide 29｜多 Agent 协作四种模式

| 模式 | 描述 | 适用场景 | 图示 |
|---|---|---|---|
| **顺序协作** | A → B → C 流水线 | 步骤明确的流程 | `A→B→C` |
| **并行协作** | A 和 B 同时工作 | 独立子任务 | `A,B → 合并` |
| **监督协作** | Manager 分配任务给 Worker | 复杂项目管理 | `Manager → W1,W2,W3` |
| **辩论协作** | 多个 Agent 给出不同观点 | 需要多视角分析 | `A↔B↔C` |

**LangGraph 的图结构**（概念）：

```
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("reviewer", reviewer_agent)
workflow.add_edge("researcher", "writer")    # 研究员 → 撰写员
workflow.add_edge("writer", "reviewer")      # 撰写员 → 审核员
```

> 详见 notebook c41 的简化版多 Agent 示例

---

### Slide 30｜通信协议：为什么需要标准？  `[notebook c42]`

**没有标准协议的世界**：

```
Agent A 想调用天气 API     → 写一个 WeatherTool 类
Agent A 想调用数据库       → 写一个 DatabaseTool 类
Agent A 想调用 GitHub API  → 写一个 GitHubTool 类
...
每接入一个新服务，都要从头写适配器代码
```

**有了标准协议的世界**：

```
Agent A 通过 MCP 协议 → 自动发现并调用任何 MCP 兼容的服务
Agent B 通过 A2A 协议 → 直接与 Agent A 对话协作
Agent C 通过 ANP 协议 → 在网络中发现需要的 Agent 服务
```

> 类比：USB-C 统一了充电接口，HTTP 统一了网页通信，MCP/A2A/ANP 统一了 Agent 通信

---

### Slide 31｜三种协议对比  `[notebook c42]`

| 维度 | MCP | A2A | ANP |
|---|---|---|---|
| **全称** | Model Context Protocol | Agent-to-Agent Protocol | Agent Network Protocol |
| **提出者** | Anthropic | Google | 开源社区 |
| **解决什么** | Agent ↔ 工具通信 | Agent ↔ Agent 通信 | 大规模 Agent 网络 |
| **类比** | USB-C 接口 | 对讲机 | 互联网路由 |
| **成熟度** | 较成熟（1000+ Server） | 早期（有 SDK） | 概念阶段 |
| **使用场景** | 接入外部服务 | 多 Agent 协作 | Agent 服务发现 |

**三种协议的定位层次**：

```
        工具层           协作层           网络层
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │   MCP    │    │   A2A    │    │   ANP    │
    │ Agent    │    │ Agent    │    │ Agent 发 │
    │  ↕       │    │  ↔       │    │ 现与路由 │
    │ Tool     │    │ Agent    │    │          │
    └──────────┘    └──────────┘    └──────────┘
    "USB-C接口"      "对讲机"       "互联网路由"
```

> 本课重点掌握 MCP（已落地，Proma 在用），A2A/ANP 了解原理即可

---

### Slide 32｜MCP 架构与实战  `[notebook c43]`

**MCP = Model Context Protocol**（Anthropic 提出）

**三层架构**：

| 层级 | 职责 | 示例 |
|---|---|---|
| **Host（宿主）** | 管理对话流程 | Claude Desktop / **Proma** |
| **Client（客户端）** | 与 Server 通信 | 内置在 Host 中 |
| **Server（服务器）** | 提供具体工具能力 | 文件系统 / 数据库 / API |

**MCP 的核心价值**：

```
传统方式（硬编码）:
  Agent ──自定义代码──→ 天气 API
  Agent ──自定义代码──→ 数据库

MCP 方式（标准化）:
  Agent ──MCP Client──→ MCP Server（天气）
  Agent ──MCP Client──→ MCP Server（数据库）
  Agent ──MCP Client──→ MCP Server（GitHub）
```

**本课程的 MCP 实践**：
- Proma 工作区配置 `mcp.json` → 自动发现 MCP Server
- 课程已用：nowledge-mem、notion、scansci-pdf、tavily
- 详见 notebook c43 的概念演示

---

## Part 5：Skill + 课程总结 `[notebook c44-c47]`

### Slide 33｜什么是 Skill？  `[notebook c45]`

**Skill = 可复用的 Agent 能力单元**

```
Skill = Prompt 模板 + 工具集 + 行为约束 + 输出格式
```

| 组成 | 说明 | 示例 |
|---|---|---|
| **Prompt 模板** | 定义角色和任务 | "你是航天产业分析师..." |
| **工具集** | 可用的工具列表 | [rag_search, calculator] |
| **行为约束** | 做什么、不做什么 | "必须基于报告数据，不可编造" |
| **输出格式** | 回答的结构要求 | "使用中文，包含数据来源" |

**Skill 解决了什么问题？**
- 不同用户面对同一 Agent，可以给它不同的 Skill 来适应不同场景
- 一个 Agent + 多个 Skill = 一个多面手助手
- Skill 可以分享、复用、版本管理

---

### Slide 34｜Skill 的结构（写法概览）  `[notebook c46]`

**一个 Skill 的四段结构**：

```
┌─────────────────────────────────────┐
│ 1. 身份定义（name + description）    │
│    "我是谁，我能做什么"              │
├─────────────────────────────────────┤
│ 2. System Prompt（角色 + 流程）      │
│    "我该怎么工作"                    │
│    - 工作流程步骤                    │
│    - 行为约束规则                    │
├─────────────────────────────────────┤
│ 3. 工具集（tools）                   │
│    "我能用什么"                      │
│    - rag_search, calculator          │
├─────────────────────────────────────┤
│ 4. 输出格式（output_format）         │
│    "我的产出长什么样"                │
│    - 分析结论 / 数据依据 / 来源      │
└─────────────────────────────────────┘
```

> 详见 notebook c46 的 Python 字典实现示例

---

### Slide 36｜课程完整闭环

```
第1讲                第2讲                第3讲
数据处理 ──────→ 机器学习 ──────→ NLP 基础
Pandas             Scikit-learn        API + Prompt
Vibe Coding 入门   Spec-driven         上下文工程

                                          │
                                          ▼
第8讲                第6-7讲                第4讲
Agent 系统 ◄────── 部署 + RAG ◄────── NLP 进阶
LangChain Agent    Ollama + ChromaDB    BERT + LoRA
Skills + MCP       Spec-driven 部署     HuggingFace
```

**你学会了什么？**
- 会用 Python 处理数据和训练模型
- 会调用和微调大语言模型
- 会部署模型并搭建 RAG 系统
- 会开发完整的 AI Agent 应用
- 会用 Vibe Coding 工具链高效协作

---

## 收尾

### Slide 37｜Agent 能力边界与安全意识

**Agent 不是万能的，需要注意**：

| 风险 | 说明 | 防护 |
|---|---|---|
| **幻觉** | Agent 可能编造工具不存在的结果 | 工具结果必须来自真实执行 |
| **无限循环** | Agent 可能在同一步骤反复尝试 | 设置 `max_iterations` |
| **工具误用** | Agent 可能调用错误的工具 | 写清楚工具描述和边界 |
| **越权行动** | Agent 可能执行超出预期的操作 | Speckit 约束 + 工具白名单 |
| **上下文丢失** | 长对话中 Agent 忘记早期信息 | 记忆管理 + 摘要压缩 |

**安全准则**：
1. Agent 能调用的工具必须是**白名单制**
2. 高风险操作（删除、发送、支付）需要**人工确认**
3. 始终设置**最大迭代次数**防止失控
4. 生产环境 Agent 必须有**日志和审计**

---

### Slide 38｜知识点速查 + 实验八说明 + 课程寄语

**核心概念速查表**：

| 概念 | 一句话解释 |
|---|---|
| Agent | 感知 → 决策 → 行动 → 观察的闭环系统 |
| ReAct | Thought-Action-Observation 的推理-行动循环 |
| Function Calling | LLM 返回"调哪个工具 + 什么参数"的 JSON |
| Tool Description | 写给 LLM 看的工具使用说明，决定调用准确率 |
| MCP | Agent ↔ Tool 的标准通信协议（USB-C） |
| Skill | Prompt + 工具 + 约束 = 可复用的 Agent 能力单元 |

**实验八**（课程最终实验）：
- 基于航天产业报告构建智能问答 Agent
- 5 个任务：RAG 工具封装 / ReAct Agent / 多轮记忆 / Gradio 界面 / 行为分析
- 满分 100 分，综合运用第1-6讲所学

**课程寄语**：

> 六讲之前：你是一个 Python 初学者
> 六讲之后：你能开发完整的 AI Agent 应用
>
> Vibe Coding 告诉你：未来的开发者不是被 AI 替代的人，
> 而是善于与 AI 协作的人。
>
> **Keep coding, keep vibing!**

