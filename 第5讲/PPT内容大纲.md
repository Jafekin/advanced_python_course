# 第五讲：大模型部署与检索增强生成（RAG）
---

### Slide 1｜封面

**标题**：Python 进阶 · 第 5 讲
**副标题**：大模型部署 × 检索增强生成（RAG）
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航

**两大板块，配套 Vibe Coding 工具：**

| 模块 | 主题 | 关键技术 | Vibe Coding 工具 |
|---|---|---|---|
| Part 1 | 大模型部署 | Ollama / 量化 / vLLM | Spec-driven（deploy_speckit.md） |
| Part 2 | RAG 基础 | 三段式 / 三代演进 | 两段式 Prompt |
| Part 3 | RAG 流水线 | 分块 / 向量化 / ChromaDB | Inline Edit + @文件引用 |
| Part 4 | 高级检索 + 记忆 | MQE / HyDE / 记忆四类型 | Prompt 调优 / 上下文工程 |

> 完成标准：能从零搭一个领域文档问答系统，并理解 Agent 记忆的工程地位

---

### Slide 3｜承上启下：从第4讲到第5讲

```
第3讲 NLP 基础与 Prompt 工程   →  会调 OpenAI 兼容 API
第4讲 NLP 进阶与模型微调        →  能白盒定制 BERT
第5讲 大模型部署与 RAG（本讲）  →  让模型"用得上、答得准"
第6讲 Agent 系统开发            →  让模型"思考+行动"
```

**本讲解决两个问题**：
1. 模型训练好了，怎么变成一个**可调用的服务**？（部署）
2. 模型知识过期、会幻觉，怎么让它**基于真实文档回答**？（RAG）

---

## Part 0：本讲路线图（5min）

### Slide 4｜为什么需要部署和检索？

**问题一：模型在哪跑？**
- 训练好的模型权重是几个 GB 的文件，怎么变成 HTTP API？
- 云端 API 贵且数据出域 → 需要本地部署
- 手机/边缘设备算力有限 → 需要量化

**问题二：模型答得准吗？**
- 模型训练数据有截止日期（GPT-4 截止 2023 年）
- 问"2024 年中国商业航天发射次数"→ 模型不知道或幻觉乱答
- 把航天产业报告喂给模型 → 让它基于报告回答

---

### Slide 5｜本讲路线图

```
Part 1 部署（18min）              Part 2-3 RAG（52min）
┌──────────────────┐              ┌──────────────────────┐
│ 部署全景 + 选型  │              │ Part 2 RAG 基础       │
│ 量化原理         │     →        │ Part 3 流水线从零实现  │
│ vLLM 深入        │              └──────────────────────┘
└──────────────────┘                        ↓
                                  Part 4 高级+记忆（12min）
                                  ┌──────────────────────┐
                                  │ MQE/HyDE 原理        │
                                  │ 记忆系统概览 → 第6讲 │
                                  └──────────────────────┘
```

---

## Part 1：大模型部署（18min）

### Slide 6｜部署全景：从权重到服务

**为什么要部署？**
- 模型权重（.safetensors / .gguf）是文件，不能直接被业务系统调用
- 需要一个**推理服务**把权重加载进显存，对外暴露 HTTP API

**部署 = 推理服务**（不是训练）：

```
模型权重文件 ──┐
              ├──→ 推理引擎 ──→ HTTP API ──→ 业务系统调用
配置文件     ──┘     (加载到显存)    (OpenAI 兼容)
```

> 本讲聚焦"把模型跑起来并暴露 API"，不涉及训练/微调（第4讲已讲）

---

### Slide 7｜主流部署方案对比

| 方案 | 定位 | 硬件 | 优势 | 场景 |
|---|---|---|---|---|
| **Ollama** | 一键式 | 4GB+显存/CPU | 零配置、模型库丰富 | 个人/原型/教学 |
| **vLLM** | 高性能 | NVIDIA GPU | PagedAttention、高并发 | 生产/企业 |
| **llama.cpp** | 极致轻量 | CPU/低配GPU | 纯CPU流畅、GGUF量化 | 嵌入式/边缘 |
| **TGI** | HF 官方 | 多 GPU | 工程化、容器友好 | 企业 HF 生态 |
| **LM Studio** | GUI 可视化 | 6GB+显存 | 零命令行 | 普通用户 |

> 本讲概念讲 Ollama + 深入讲 vLLM；Ollama 实操命令见 notebook 自学

---

### Slide 8｜Ollama：本地一键起服务（概念页）

**Ollama 三大特点**：
- 一行命令拉模型（自动选量化版）：`ollama pull qwen2.5:7b-instruct-q4_K_M`
- 自动暴露 OpenAI 兼容 API：`/v1/chat/completions`
- CPU/GPU 自动切换（没 GPU 也能跑）

**调用方式**（关键：只改 `base_url`，第3讲学的 openai 库调用方式完全适用）：

```python
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # 本地服务，任意字符串即可
)
response = client.chat.completions.create(
    model="qwen2.5:7b-instruct-q4_K_M",
    messages=[{"role": "user", "content": "你好"}],
)
```

> 安装、pull、serve 的完整命令流见 `课程代码案例.ipynb` Part 1

---

### Slide 9｜Vibe Coding 工具：Spec-driven 部署规约

**deploy_speckit.md**（轻量 Speckit）：

```markdown
# 部署规约

## Constitution（硬约束）
- 端口：11434
- 模型：qwen2.5:7b-instruct-q4_K_M
- 上下文长度：32768
- 必须 OpenAI 兼容
- 必须支持流式输出

## Context（环境）
- 部署环境：CloudStudio / 本地 macOS
- GPU：可选（无 GPU 退化到 CPU 模式）
```

**用法**：每次与 AI 对话部署问题时 `@deploy_speckit.md`，AI 全程遵守约束

> 对比"每轮重复说端口和模型" vs "Speckit 一次锁定"

---

### Slide 10｜量化原理：为什么要量化？

**问题**：7B 模型 FP16 需要多少显存？

```
7B 参数 × 2 字节（FP16） = 14 GB
```

消费级显卡（RTX 3060 = 12GB）跑不动！

**量化 = 降低参数精度，换取显存和速度**

| 精度 | 每参数字节 | 7B 显存 | 精度损失 |
|---|---|---|---|
| FP16 | 2 | 14 GB | 基准 |
| INT8 | 1 | 7 GB | < 1% |
| INT4 | 0.5 | **4 GB** | < 3% |

> INT4 后 7B 模型 4GB 显存可跑，RTX 3060 也能用；MMLU 损失 < 3%

---

### Slide 11｜GGUF 量化格式：Q4_K_M 是什么？

**GGUF**：llama.cpp/Ollama 使用的量化文件格式

**K-Quants 量化级别**（不是简单均匀量化）：

| 格式 | 显存 | 精度 | 说明 |
|---|---|---|---|
| Q4_0 | 最小 | 较低 | 最简单的 4-bit |
| **Q4_K_M** | 小 | **好** | 推荐：重要层用更高精度 |
| Q5_K_M | 中 | 更好 | 5-bit，平衡型 |
| Q8_0 | 较大 | 很好 | 8-bit，接近 FP16 |

**K-Quants 思想**：不是所有层都用同样精度——注意力层等重要层保留更高精度，FFN 层用低精度

> 选型经验：教学/原型用 Q4_K_M，生产高精度场景用 Q5_K_M 或 Q8_0

---

### Slide 12｜量化方法：PTQ vs QAT

| 方法 | 全称 | 原理 | 成本 | 精度 |
|---|---|---|---|---|
| **PTQ** | 训练后量化 | 模型训练完直接量化 | 低（分钟级） | 略降 |
| **QAT** | 量化感知训练 | 训练时就模拟量化 | 高（需重新训练） | 更好 |

**实际工程**：90% 场景用 PTQ（足够好且快）；QAT 用于对精度要求极高的场景

**显存计算公式**：

```
显存 ≈ 参数量 × 每参数字节数
7B × INT4(0.5字节) = 3.5 GB
7B × FP16(2字节)   = 14 GB
```

---

### Slide 13｜vLLM 深入（一）：PagedAttention

**问题**：传统推理的 KV Cache 显存碎片严重
- 每个请求预分配最大长度显存（如 2048 token）
- 实际生成可能只用了 200 token → 90% 显存浪费

**PagedAttention 思想**（类比 OS 虚拟内存）：

```
传统：连续分配              PagedAttention：分页分配
┌──────────────┐            ┌──┬──┬──┬──┬──┬──┐
│  请求1       │            │P1│P2│P1│P3│P2│P1│  按需分配
│  (2048 tok) │            └──┴──┴──┴──┴──┴──┘  消除碎片
└──────────────┘
```

- KV Cache 像"内存页"，按需分配/回收
- 显存利用率从 ~30% 提升到 ~95%
- 同样显存能跑更多并发请求

---

### Slide 14｜vLLM 深入（二）：连续批处理

**传统静态批处理**：等齐一批再一起推理，长请求拖慢短请求

```
请求1(短) ─┐
请求2(长) ─┤── 等齐 ──→ 一起推理 ── 请求1 等请求2 完成
请求3(短) ─┘
```

**连续批处理**（Continuous Batching）：动态拼批

```
请求1 完成 → 立刻返回 → 位置空出 → 新请求填入
请求2 继续推理 → 不阻塞其他请求
```

**效果**：吞吐量提升 2-10 倍，并发越高优势越大

---

### Slide 15｜vLLM vs Ollama 性能对比

**实测数据**（RTX 3090，Qwen3 8B，FP16）：

| Batch Size | Ollama 响应(s) | vLLM 响应(s) | Ollama tok/s | vLLM tok/s |
|---|---|---|---|---|
| 1 | 5.68 | 5.44 | 45.1 | 47.1 |
| 8 | 7.64 | 5.82 | 268.0 | 351.9 |
| 16 | 15.6 | 6.42 | 262.9 | **638.4** |

**结论**：
- 单请求（Batch=1）：两者接近
- 高并发（Batch=16）：vLLM 吞吐是 Ollama 的 **2.4 倍**
- vLLM 显存略高，但吞吐优势巨大

> 数据来源：博客园《Ollama和vLLM大模型推理性能对比实测》

---

### Slide 16｜vLLM 部署命令

```bash
# 单 GPU 启动 Qwen2.5 7B
vllm serve Qwen/Qwen2.5-7B-Instruct \
    --port 8000 \
    --tensor-parallel-size 1

# 多 GPU（2 卡）
vllm serve Qwen/Qwen2.5-7B-Instruct \
    --tensor-parallel-size 2 \
    --port 8000

# API 调用（OpenAI 兼容）
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"Qwen/Qwen2.5-7B-Instruct",
         "messages":[{"role":"user","content":"你好"}]}'
```

> vLLM API 协议与 OpenAI 完全兼容，业务代码无需修改

---

### Slide 17｜部署选型决策树

```
你的场景？
├── 个人开发 / 原型 / 教学
│   └── Ollama（一键起服务，CPU/GPU 自适应）
├── 生产高并发 / 企业 API 服务
│   └── vLLM（PagedAttention + 连续批处理）
├── CPU only / 嵌入式 / 边缘设备
│   └── llama.cpp（GGUF 量化，纯 CPU 流畅）
├── HuggingFace 生态 / 容器化
│   └── TGI（HF 官方，工程化好）
└── 普通用户 / 不想敲命令
    └── LM Studio（GUI 可视化）
```

> 本讲实验用 Ollama；生产场景推荐 vLLM

---

## Part 2：RAG 基础与三段式（15min）

### Slide 18｜RAG 定义：检索 + 增强 + 生成

**RAG = Retrieval-Augmented Generation**

- **检索（Retrieve）**：从知识库查询相关内容
- **增强（Enhance）**：把检索结果融入 Prompt，辅助模型生成
- **生成（Generate）**：输出兼具准确性与透明度的答案

```
用户提问 → [检索知识库] → [拼进 Prompt] → [LLM 生成] → 带引用的回答
```

> 核心思想：生成前先查资料，让模型"开卷考试"

---

### Slide 19｜三种问答方案对比

| 方案 | 原理 | 优势 | 劣势 |
|---|---|---|---|
| **传统检索 QA** | 关键词匹配（TF-IDF/BM25） | 可靠、可溯源 | 死板、不理解语义 |
| **纯 LLM** | 直接问模型 | 灵活、自然 | 幻觉、知识过期 |
| **RAG** | 检索 + LLM 生成 | 准确、可溯源、灵活 | 系统复杂 |

**演示**：问"2024 年中国商业航天发射次数"
- 传统检索：找不到（文档写"商业发射"，查询是"商业航天发射"）
- 纯 LLM：幻觉乱答（"约 50 次"——错，实际 30 次）
- RAG：基于报告回答"30 次，同比增加 50%"[OK]

---

### Slide 20｜RAG 完整工作流（两阶段）

**数据准备阶段**（离线一次）：

```
文档(PDF/Word/...) → 分块 → 向量化 → 存入向量库
```

**查询应用阶段**（在线每次）：

```
用户提问 → 查询向量化 → 语义检索 top-k → 拼 Prompt → LLM 生成
```

```
┌─────────────────────────────────────────────────┐
│  离线：文档 → 分块 → 向量化 → 向量库              │
│  在线：提问 → 向量化 → 检索 top-k → 拼 Prompt → 生成  │
└─────────────────────────────────────────────────┘
```

> 关键：知识库建一次，查询每次跑

---

### Slide 21｜RAG 三代演进

| 代际 | 时间 | 检索方式 | 生成方式 | 痛点 |
|---|---|---|---|---|
| **Naive RAG** | 2020-2021 | TF-IDF/BM25 关键词 | 直接拼接 | 字面不匹配就漏 |
| **Advanced RAG** | 2022-2023 | 稠密嵌入语义检索 | 查询重写 + 重排序 | 召回率仍不够 |
| **Modular RAG** | 2023-至今 | 混合检索 + MQE + HyDE | CoT + 自我反思 | 模块组合复杂 |

**演进逻辑**：每代解决上一代痛点
- Naive → Advanced：从"字面匹配"到"语义理解"
- Advanced → Modular：从"单次检索"到"多策略融合"

---

### Slide 22｜RAG vs 微调对比

| 维度 | RAG | 微调 |
|---|---|---|
| 适合场景 | 知识常更新 / 长尾 / 需引用 | 风格 / 格式 / 特定任务 |
| 知识更新 | 改知识库即可（秒级） | 需重新训练（小时级） |
| 显存需求 | 推理即可 | 训练需大显存 |
| 可解释性 | 高（有引用） | 低（黑盒） |
| 成本 | 低 | 高 |

**选型建议**：
- 知识常变 → RAG（如新闻、政策、企业文档）
- 风格固定 → 微调（如客服话术、代码风格）
- 两者结合 → 先 RAG 注入知识，再微调改风格

---

## Part 3：RAG 流水线从零实现（37min · 核心）

### Slide 24｜RAG 流水线六环节

```
1. 文档加载    PDF/Word/Excel → Markdown
2. 文本分块    切成 500-1000 字符的小段
3. 向量化      每段转成 384 维向量
4. 向量库存储   存入 ChromaDB
5. 语义检索    查询向量 → top-k 最相似段落
6. Prompt 拼接  检索结果 + 问题 → LLM 生成
```

**本讲从零实现，不使用 LangChain/LlamaIndex 的 RAG 链**——每一步学生都能看懂、能改、能调试

---

### Slide 25｜环节1：文档加载与清洗

**工具**：`markitdown`（微软开源，统一文档转换）

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("航天产业报告.pdf")
markdown_text = result.text_content
print(len(markdown_text), "字符")
```

**支持格式**：PDF / Word / Excel / PPT / 图片(OCR) / 音频(转录) / CSV / JSON / HTML

---

### Slide 26｜环节2：为什么要分块？

**原因1：嵌入模型输入长度限制**
- `all-MiniLM-L6-v2` 最大输入 512 token
- 一篇 2 万字报告远超限制

**原因2：检索精度**
- 整篇文档向量化 → 语义被稀释
- 分块后每段聚焦一个主题，检索更准

**原因3：Prompt 长度控制**
- top-5 检索结果拼进 Prompt，每段 500 字 → 2500 字（可控）
- 不分块直接塞整篇 → 超出上下文窗口

```
整篇文档(20000字) ──向量化──→ 1个向量（语义稀释）
                ↓ 分块
500字 × 40段 ──向量化──→ 40个向量（语义聚焦）
```

---

### Slide 27｜分块策略1：固定字符分块

```python
def chunk_fixed(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # 重叠窗口
    return chunks
```

**优点**：简单
**缺点**：可能切断语义（如把"2024年"切成"2024"和"年"）

**重叠窗口（overlap）作用**：防止语义在边界断裂

```
块1: [...航天发射 30 次，同比]
块2: [同比增加 50%...]
         ↑ 重叠部分保证语义连续
```

---

### Slide 28｜分块策略2：递归字符分块（推荐）

**思路**：按分隔符优先级递归切分，保持段落完整

```python
def chunk_recursive(text, chunk_size=500, overlap=50):
    separators = ["\n\n", "\n", "。", "；", "，", " "]
    # 先按段落分（\n\n），段落太大再按行分（\n），再按句号分...
    ...
```

**分隔符优先级**：`\n\n`（段落）→ `\n`（行）→ `。`（句）→ `；`（分句）→ `，`（逗号）→ ` `（空格）

**优点**：保持语义完整，不会切断句子
**LangChain 的 `RecursiveCharacterTextSplitter` 就是这个思路**

---

### Slide 29｜分块策略3：Token 分块

**思路**：按 token 数切分，与嵌入模型对齐

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def chunk_by_token(text, max_tokens=500, overlap=50):
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens - overlap):
        chunk_tokens = tokens[i:i+max_tokens]
        chunks.append(tokenizer.decode(chunk_tokens))
    return chunks
```

**优点**：精确控制 token 数，不超嵌入模型限制
**缺点**：需要 tokenizer，速度慢

---

### Slide 30｜chunk_size 调参经验

| 场景 | chunk_size | overlap | 说明 |
|---|---|---|---|
| **问答场景** | 500-800 字符 | 50-100 | 小块聚焦，检索准 |
| **长文摘要** | 1000-1500 字符 | 100-200 | 大块保留上下文 |
| **代码文档** | 按函数/类分 | 0 | 语义天然边界 |
| **表格数据** | 按行分 | 0 | 保持行完整 |

**经验法则**：
- overlap = chunk_size × 10-20%
- 宁可小块多检索，不要大块塞满 Prompt
- 用 Inline Edit 快速改 chunk_size 对比检索效果

---

### Slide 31｜环节3：向量化——句子嵌入

**句子嵌入 vs 词嵌入**（第4讲已讲 token embedding）：
- 词嵌入：每个词一个向量（如 "航天" → 768维）
- 句子嵌入：整句话一个向量（如 "航天发射 30 次" → 384维）

**句子嵌入原理**（sentence-transformers）：

```
输入句子 → BERT 编码 → 每个token一个向量 → mean pooling → 1个句子向量
```

**模型选型**：

| 模型 | 维度 | 大小 | 语言 | 备注 |
|---|---|---|---|---|
| `all-MiniLM-L6-v2` | 384 | 80MB | 英文为主 | 教学/原型推荐 |
| `bge-large-zh` | 1024 | 1.3GB | 中文优秀 | 中文场景推荐 |
| `bge-m3` | 1024 | 2.3GB | 多语言 | 生产场景 |

---

### Slide 32｜sentence-transformers 实操

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# 单句编码
vec = model.encode("航天发射 30 次")
print(vec.shape)  # (384,)

# 批量编码
sentences = ["航天发射 30 次", "商业航天井喷", "卫星互联网组网"]
vectors = model.encode(sentences)
print(vectors.shape)  # (3, 384)

# 计算相似度
from sentence_transformers import util
sim = util.cos_sim(
    model.encode("法国出口", normalize_embeddings=True),
    model.encode("法兰西出口", normalize_embeddings=True)
)
print(sim)  # 0.85+ 语义相似
```

> "法国"≈"法兰西"——这是 RAG 能命中同义词的关键

---

### Slide 33｜环节4：ChromaDB 向量库

**ChromaDB**：轻量级开源向量数据库，纯 Python，本地持久化

**五要素**：

| 概念 | 类比 SQL | 说明 |
|---|---|---|
| collection | 表 | 一个知识库一个 collection |
| id | 主键 | 每个 chunk 的唯一 ID |
| document | 行内容 | chunk 原文 |
| embedding | 索引 | chunk 的向量 |
| metadata | 列字段 | 来源、页码、章节等 |

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_collection("aerospace_report")

collection.add(
    ids=["chunk_0", "chunk_1"],
    documents=["航天发射 30 次...", "商业航天井喷..."],
    embeddings=[[0.1, ...], [0.2, ...]],
    metadatas=[{"page": 1}, {"page": 1}]
)
```

---

### Slide 34｜环节5：语义检索

```python
# 查询向量化
query_vec = model.encode("2024 年商业航天发射多少次")

# 检索 top-5
results = collection.query(
    query_embeddings=[query_vec],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)

for i, (doc, meta, dist) in enumerate(zip(
    results['documents'][0],
    results['metadatas'][0],
    results['distances'][0]
)):
    print(f"[{i+1}] dist={dist:.3f} page={meta['page']}")
    print(doc[:100])
```

**相似度度量**：余弦相似度（默认）/ 欧氏距离
**score_threshold**：过滤 distance > 1.0 的不相关结果

---

### Slide 35｜环节6：Prompt 拼接与生成

**Prompt 模板**：

```python
PROMPT_TEMPLATE = """你是文档问答助手，只根据以下参考资料回答问题。
如果资料中没有答案，请说"资料中未提及"。

参考资料：
{context}

问题：{question}

回答（请用 [1][2] 标注引用来源）：
"""

def generate(question, retrieved_chunks):
    context = "\n\n".join(
        f"[{i+1}] {chunk}" for i, chunk in enumerate(retrieved_chunks)
    )
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    
    response = client.chat.completions.create(
        model="qwen2.5:7b-instruct-q4_K_M",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

> 防幻觉关键：明确"如果资料里没有，就说资料中未提及"

---

### Slide 36｜完整 RAG 流水线串起来

```python
def rag_pipeline(question, top_k=5):
    # 1. 查询向量化
    query_vec = model.encode(question)
    
    # 2. 语义检索
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=top_k
    )
    retrieved_chunks = results['documents'][0]
    
    # 3. 拼 Prompt
    context = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(retrieved_chunks))
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    
    # 4. LLM 生成
    response = client.chat.completions.create(
        model="qwen2.5:7b-instruct-q4_K_M",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content, retrieved_chunks

# 一行调用
answer, sources = rag_pipeline("2024 年中国商业航天发射多少次？")
```

---

### Slide 37｜RAG 流水线效果演示

**问**："2024 年中国商业航天发射次数同比变化？"

```
检索 top-5:
[1] (dist=0.23) 2024 年商业航天发射次数有望达 30 次，同比增加 50%
[2] (dist=0.31) 海南商业航天发射场 1 号工位 6 月底具备发射能力
[3] (dist=0.42) 长征十二号火箭 24 年首飞，3.8 米直径
[4] (dist=0.48) 卫星互联网组网加速，千帆星座首发
[5] (dist=0.55) 商业航天产业链聚集格局初显

LLM 回答：
根据资料，2024 年中国商业航天发射次数预计达 30 次，
同比 2023 年的 20 次增加 50% [1]。主要得益于海南商业
航天发射场投入使用 [2] 和长征十二号等新型火箭首飞 [3]。
```

> 注意引用标注 [1][2][3]——RAG 的可解释性

---

## Part 4：高级检索策略 + Agent 记忆概览（12min）

### Slide 39｜高级检索：痛点与三策略

**痛点**：
1. **用词不匹配**：用户问"法国出口额"，文档写"法兰西出口"
2. **查询-文档语义鸿沟**：问题是疑问句，文档是陈述句，语义空间不同
3. **lost in the middle**：LLM 对 top-k 中间位置内容关注度不够

**三策略对比**：

| 策略 | 思想 | 适合场景 |
|---|---|---|
| **MQE 多查询扩展** | LLM 改写 N 个等价查询，并行检索合并 | 用词多样性场景 |
| **HyDE 假设文档嵌入** | LLM 先生成假设答案，用答案向量检索 | 术语密集专业领域 |
| **Reranker 重排序** | 向量检索粗排 top-10 → Cross-Encoder 精排 top-3 | 对精度要求高 |

**HyDE 为什么有效**：问题是疑问句，文档是陈述句 → 语义空间不同；假设答案也是陈述句 → 更接近真实文档

> Reranker 用 `BAAI/bge-reranker-base`；Bi-Encoder 粗排快，Cross-Encoder 精排准

---

### Slide 40｜RAG 评估指标

**如何量化检索质量？**

| 指标 | 定义 | 用途 |
|---|---|---|
| **Recall@k** | top-k 结果中包含正确答案的比例 | 召回率（找全了吗） |
| **Precision@k** | top-k 结果中相关的比例 | 精确率（找得准吗） |
| **MRR** | 第一个相关结果的平均倒数排名 | 排序质量 |

**示例**：
- 正确答案在 top-5 的第 3 位 → Recall@5=1, Precision@5=0.2, MRR=1/3
- 正确答案不在 top-5 → Recall@5=0, MRR=0

---

### Slide 41｜Agent 记忆系统

**为什么 Agent 需要 Memory？**
- LLM 无状态：重启就忘了"我叫张三"
- 上下文窗口有限：长对话早期信息被挤出

**四类型记忆**：

| 类型 | 存什么 | 生命周期 | 类比 |
|---|---|---|---|
| **工作记忆** | 当前对话上下文 | 会话级，TTL 清理 | "现在在聊什么" |
| **情景记忆** | 具体交互事件 | 长期持久化 | "上周问过 X" |
| **语义记忆** | 抽象知识/用户偏好 | 长期持久化 | "用户偏好 Python" |
| **感知记忆** | 多模态信息 | 动态管理 | "用户上传的图" |

**Memory 与 RAG 的关系**：
- RAG 检索**外部静态知识**（文档）
- Memory 检索**内部动态交互**（对话历史）
- 两者结合：用户提问 → 检索 Memory（找偏好）+ 检索 RAG（找知识）→ 拼 Prompt → 生成 → 存入 Memory

---

## 收尾

### Slide 42｜知识点速查 + 实验五说明 + Q&A

**知识点速查表**：

| 模块 | 核心知识点 |
|---|---|
| 部署 | Ollama 一键起服务 / 量化 Q4_K_M / vLLM PagedAttention + 连续批处理 |
| RAG 三段式 | 检索 Retrieve → 增强 Enhance → 生成 Generate |
| RAG 三代 | Naive(关键词) → Advanced(语义) → Modular(混合) |
| 分块三策略 | 固定字符 / 递归字符（推荐）/ Token |
| 嵌入模型 | all-MiniLM-L6-v2 (384维) / bge-large-zh (中文) |
| 向量库 | ChromaDB 五要素：collection/id/document/embedding/metadata |
| 高级检索 | MQE 多查询扩展 / HyDE 假设文档 / Reranker 重排序 |
| 评估指标 | Recall@k / Precision@k / MRR |
| 记忆四类型 | 工作 / 情景 / 语义 / 感知 |

**实验五说明**：
- 数据：`综述论文.pdf`（ACM TOSEM 2025，"LLM for Mobile: An Initial Roadmap"，29页英文综述）
- 4 任务：文档加载分块 → 向量化存储 → 检索生成 → 高级检索对比
- 注意：英文长文档，需考虑英文分块策略和跨语言查询

**工具速查表**：

| 工具 | 用途 | 核心命令/API |
|---|---|---|
| Ollama | 本地部署 LLM | `ollama serve` / `ollama pull` |
| vLLM | 生产级推理 | `vllm serve` |
| markitdown | 文档转 Markdown | `MarkItDown().convert()` |
| sentence-transformers | 句子嵌入 | `SentenceTransformer().encode()` |
| ChromaDB | 向量数据库 | `collection.add()` / `collection.query()` |
| bge-reranker | 重排序 | Cross-Encoder 编码 |
| Spec-driven | 部署规约 | `@deploy_speckit.md` |

**Q&A**
