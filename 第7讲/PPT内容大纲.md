# 第七讲：RAG 进阶与 Agent 记忆

## PPT 内容大纲（约 44 张 Slides）

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 7 讲
**副标题**：RAG 进阶 × Agent 记忆系统
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航

| 模块 | 主题 | 关键技术 | Vibe Coding 工具 |
|---|---|---|---|
| Part 1 | 高级检索策略 | MQE / HyDE / Reranker / 混合检索 | Prompt 调优 + @文件引用 |
| Part 2 | RAG 评估与调优 | Recall@k / MRR / 调参实践 | Inline Edit 快速对比 |
| Part 3 | Agent 记忆系统 | 四类型记忆 / JSON+向量实现 | 上下文工程 |

> 完成标准：能诊断基础 RAG 的不足，用高级策略提升检索质量，并为 Agent 添加记忆

---

### Slide 3｜承上启下：从第6讲到第7讲

```
第6讲：搭建了基础 RAG 流水线（能跑）
         ↓ 但存在两个问题
问题1：检索不准——用词不匹配、语义鸿沟、排序不够精
问题2：没有记忆——每次对话从零开始，不知道"你是谁"
         ↓
第7讲：高级检索策略 + 评估调优 + 记忆系统
```

**本讲目标**：让 RAG "检索更准、评估有据、记住用户"

---

## Part 1：高级检索策略详解（30min）

### Slide 4｜基础 RAG 的三大痛点

| 痛点 | 具体表现 | 示例 |
|---|---|---|
| **用词不匹配** | 用户用口语，文档用术语 | 问"法国出口额"，文档写"法兰西出口" |
| **语义鸿沟** | 问题是疑问句，文档是陈述句 | "发射了多少次？" vs "发射次数达30次" |
| **lost in the middle** | LLM 对 top-k 中间内容关注不足 | top-5 中第3条最相关，但 LLM 忽略了 |

**解决思路**：多查询扩展 + 假设文档 + 重排序 + 混合检索

---

### Slide 5｜策略1：MQE 多查询扩展

**核心思想**：一个问题改写成 N 个等价查询，并行检索后合并去重

```
原始问题："2024年商业航天发射次数"
    ↓ LLM 改写
改写1："中国2024商业火箭发射数量统计"
改写2："2024年民营航天发射情况"
改写3："商业航天2024发射任务次数"
    ↓ 分别检索
3组 top-5 → 合并去重 → 最终 top-5
```

**为什么有效**：不同表述覆盖更多词汇，提高召回率

---

### Slide 6｜MQE 代码实现

```python
def generate_multi_queries(question, n=3):
    """用 LLM 生成 N 个等价查询"""
    prompt = f"""请将以下问题改写成{n}个不同表述的查询，
每个查询用不同的关键词，但语义相同。
每行一个，不要编号。

原始问题：{question}"""
    
    response = client.chat.completions.create(
        model="qwen2.5:7b-instruct-q4_K_M",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    queries = response.choices[0].message.content.strip().split('\n')
    return [question] + queries[:n]  # 原始查询 + N 个改写

def mqe_retrieve(question, top_k=5, n_queries=3):
    """多查询扩展检索"""
    queries = generate_multi_queries(question, n=n_queries)
    all_results = {}
    
    for q in queries:
        vec = model.encode(q)
        results = collection.query(
            query_embeddings=[vec.tolist()], n_results=top_k
        )
        for doc_id, doc in zip(results['ids'][0], results['documents'][0]):
            if doc_id not in all_results:
                all_results[doc_id] = doc
    
    return list(all_results.values())[:top_k]
```

---

### Slide 7｜MQE 效果对比

| 方法 | 查询 | 检索 top-5 命中率 |
|---|---|---|
| 单查询 | "法国出口额" | 2/5（只命中"法国"相关） |
| **MQE** | + "法兰西出口" + "France export" | **4/5**（多表述覆盖） |

**适用场景**：
- 用户表述与文档表述差异大
- 专业术语有多种说法
- 多语言混合查询

**代价**：需要额外调用 LLM 生成改写（增加延迟约 1-2s）

---

### Slide 8｜策略2：HyDE 假设文档嵌入

**核心思想**：先让 LLM 生成一个"假设答案"，用假设答案的向量去检索

```
问题："2024年商业航天发射次数"
    ↓ LLM 生成假设答案
假设答案："2024年中国商业航天完成发射约30次，同比增长50%..."
    ↓ 向量化（假设答案是陈述句，与文档同构）
假设答案向量 → 检索 → 找到真实文档
```

**为什么有效**：
- 问题是疑问句，文档是陈述句 → 语义空间不同
- 假设答案也是陈述句 → 与真实文档更接近

---

### Slide 9｜HyDE 代码实现

```python
def hyde_retrieve(question, top_k=5):
    """HyDE: 假设文档嵌入检索"""
    # 1. 生成假设答案
    prompt = f"""请根据你的知识，写一段可能回答以下问题的文字（约100字）。
不需要完全准确，只需要像一篇文档中可能出现的表述。

问题：{question}"""
    
    response = client.chat.completions.create(
        model="qwen2.5:7b-instruct-q4_K_M",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    hypothetical_doc = response.choices[0].message.content
    
    # 2. 用假设答案的向量检索
    hyde_vec = model.encode(hypothetical_doc)
    results = collection.query(
        query_embeddings=[hyde_vec.tolist()],
        n_results=top_k
    )
    return results['documents'][0]
```

**适用场景**：专业术语密集的领域（医学、法律、航天）

---

### Slide 10｜策略3：Reranker 重排序

**两阶段检索**：粗排（快但不够准）→ 精排（慢但更准）

```
                Bi-Encoder          Cross-Encoder
用途：          粗排 top-50          精排 top-5
速度：          快（独立编码）       慢（交叉编码）
精度：          中                   高
原理：          query和doc分别编码   query和doc一起编码
```

**为什么 Cross-Encoder 更准？**
- Bi-Encoder：query 和 doc 独立编码后比余弦相似度（信息不交互）
- Cross-Encoder：query 和 doc 拼接后一起进 Transformer（完全信息交互）

---

### Slide 11｜Reranker 代码实现

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('BAAI/bge-reranker-base')

def rerank_retrieve(question, top_k=5, rerank_top=20):
    """两阶段检索：粗排 + 精排"""
    # 阶段1：Bi-Encoder 粗排 top-20
    query_vec = model.encode(question)
    results = collection.query(
        query_embeddings=[query_vec.tolist()],
        n_results=rerank_top
    )
    candidates = results['documents'][0]
    
    # 阶段2：Cross-Encoder 精排
    pairs = [[question, doc] for doc in candidates]
    scores = reranker.predict(pairs)
    
    # 按精排分数重新排序
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:top_k]]
```

---

### Slide 12｜Reranker 效果对比

| 方法 | MRR | Recall@5 | 延迟 |
|---|---|---|---|
| 纯 Bi-Encoder (top-5) | 0.52 | 0.68 | 50ms |
| **Bi-Encoder(top-20) + Reranker(top-5)** | **0.74** | **0.85** | 200ms |

**结论**：精度提升 ~40%，延迟增加约 150ms（可接受）

**适用场景**：对精度要求高、延迟容忍度 > 200ms 的场景

---

### Slide 13｜策略4：混合检索（BM25 + 稠密向量）

**思路**：结合关键词匹配（精确）和语义匹配（泛化）

```
查询："2024商业航天发射30次"
    ├── BM25 稀疏检索 → 精确匹配"30次"、"商业航天"
    ├── 稠密向量检索   → 语义匹配"民营火箭发射数量"
    └── RRF 融合       → 综合排序
```

**RRF（Reciprocal Rank Fusion）融合公式**：

$$\text{RRF}(d) = \sum_{r \in R} \frac{1}{k + r(d)}$$

其中 $r(d)$ 是文档 $d$ 在各个排序中的位置，$k=60$（常数）

---

### Slide 14｜混合检索代码实现

```python
from rank_bm25 import BM25Okapi
import jieba

# BM25 索引（离线建立）
tokenized_chunks = [list(jieba.cut(c)) for c in chunks]
bm25 = BM25Okapi(tokenized_chunks)

def hybrid_retrieve(question, top_k=5, k=60):
    """混合检索：BM25 + 向量 + RRF 融合"""
    # 稀疏检索（BM25）
    query_tokens = list(jieba.cut(question))
    bm25_scores = bm25.get_scores(query_tokens)
    bm25_rank = bm25_scores.argsort()[::-1][:20]
    
    # 稠密检索（向量）
    query_vec = model.encode(question)
    results = collection.query(
        query_embeddings=[query_vec.tolist()], n_results=20
    )
    dense_ids = [int(id.split('_')[1]) for id in results['ids'][0]]
    
    # RRF 融合
    scores = {}
    for rank, idx in enumerate(bm25_rank):
        scores[idx] = scores.get(idx, 0) + 1 / (k + rank + 1)
    for rank, idx in enumerate(dense_ids):
        scores[idx] = scores.get(idx, 0) + 1 / (k + rank + 1)
    
    top_ids = sorted(scores, key=scores.get, reverse=True)[:top_k]
    return [chunks[i] for i in top_ids]
```

---

### Slide 15｜四种检索策略总结对比

| 策略 | 解决的痛点 | 额外成本 | 适用场景 |
|---|---|---|---|
| **MQE** | 用词不匹配 | +1次 LLM 调用 | 口语/多表述 |
| **HyDE** | 语义鸿沟 | +1次 LLM 调用 | 专业术语密集 |
| **Reranker** | 排序不精 | +Cross-Encoder | 精度优先 |
| **混合检索** | 字面+语义两不误 | +BM25 索引 | 通用场景 |

**组合使用**：MQE + 混合检索 + Reranker = 当前最强方案

> 实验七任务1实现 MQE，任务2实现 Reranker

---

## Part 2：RAG 评估与调优（20min）

### Slide 16｜为什么需要评估？

**问题**：怎么知道你的 RAG 系统"好不好"？

- "感觉回答挺好的" → 不可量化、不可复现
- 改了 chunk_size 后"好像变好了" → 无法确认

**评估 = 用数据说话**：构建测试集 → 计算指标 → 对比方案

---

### Slide 17｜检索质量评估指标

| 指标 | 定义 | 计算 | 用途 |
|---|---|---|---|
| **Recall@k** | top-k 中包含正确答案的比例 | 命中/总问题数 | 找全了吗 |
| **Precision@k** | top-k 中相关的比例 | 相关数/k | 找得准吗 |
| **MRR** | 第一个相关结果的平均倒数排名 | $\frac{1}{N}\sum\frac{1}{rank_i}$ | 排序质量 |

**示例**：5 个测试问题

| 问题 | 正确答案在 top-5 位置 | Recall@5 | MRR |
|---|---|---|---|
| Q1 | 第1位 | 1 | 1/1=1.0 |
| Q2 | 第3位 | 1 | 1/3=0.33 |
| Q3 | 未命中 | 0 | 0 |
| Q4 | 第2位 | 1 | 1/2=0.5 |
| Q5 | 第1位 | 1 | 1/1=1.0 |
| **平均** | — | **0.8** | **0.57** |

---

### Slide 18｜评估代码实现

```python
def evaluate_retrieval(test_set, retrieve_fn, top_k=5):
    """评估检索质量
    test_set: [{"question": ..., "answer_chunk_id": ...}, ...]
    """
    recalls, mrrs = [], []
    
    for item in test_set:
        results = retrieve_fn(item["question"], top_k=top_k)
        result_ids = [r['id'] for r in results]
        
        # Recall@k
        hit = 1 if item["answer_chunk_id"] in result_ids else 0
        recalls.append(hit)
        
        # MRR
        if item["answer_chunk_id"] in result_ids:
            rank = result_ids.index(item["answer_chunk_id"]) + 1
            mrrs.append(1.0 / rank)
        else:
            mrrs.append(0.0)
    
    return {
        "Recall@k": sum(recalls) / len(recalls),
        "MRR": sum(mrrs) / len(mrrs)
    }
```

---

### Slide 19｜构建评估数据集

**手动构建**（最可靠）：

```python
test_set = [
    {
        "question": "2024年商业航天发射了多少次？",
        "answer_chunk_id": "chunk_7",   # 人工标注的正确 chunk
        "expected_answer": "30次，同比增加50%"
    },
    {
        "question": "海南商业航天发射场什么时候投入使用？",
        "answer_chunk_id": "chunk_12",
        "expected_answer": "2024年6月底"
    },
    # ... 至少 20 个问题
]
```

**构建技巧**：
- 每个 chunk 至少生成 1 个问题
- 包含简单/中等/困难三个层次
- 困难问题：需要跨 chunk 信息、同义词替换、口语表述

---

### Slide 20｜调参实践：chunk_size 对检索质量的影响

```python
# 对比不同 chunk_size
for size in [200, 500, 800, 1200]:
    # 重新分块 + 入库
    chunks = chunk_recursive(text, chunk_size=size)
    rebuild_collection(chunks)
    
    # 评估
    metrics = evaluate_retrieval(test_set, basic_retrieve, top_k=5)
    print(f"chunk_size={size}: Recall@5={metrics['Recall@k']:.2f}, MRR={metrics['MRR']:.2f}")
```

**典型结果**：

| chunk_size | Recall@5 | MRR | 分析 |
|---|---|---|---|
| 200 | 0.65 | 0.45 | 太碎，上下文不足 |
| **500** | **0.82** | **0.61** | 最佳平衡点 |
| 800 | 0.78 | 0.55 | 语义稍稀释 |
| 1200 | 0.70 | 0.48 | 噪音明显增加 |

---

### Slide 21｜调参实践：top_k 与嵌入模型选择

**top_k 选择**：

| top_k | Recall | Prompt 长度 | 建议 |
|---|---|---|---|
| 3 | 较低 | 短 | 上下文窗口小时 |
| **5** | 中等 | **适中** | 通用推荐 |
| 10 | 高 | 长 | 召回优先，需大窗口 |

**嵌入模型对比**（同一测试集）：

| 模型 | Recall@5 | MRR | 大小 |
|---|---|---|---|
| all-MiniLM-L6-v2 | 0.72 | 0.51 | 80MB |
| bge-large-zh | **0.85** | **0.64** | 1.3GB |
| bge-m3 | 0.88 | 0.67 | 2.3GB |

> 中文场景 bge-large-zh 性价比最高

---

### Slide 22｜生产化考量

| 维度 | 问题 | 解决方案 |
|---|---|---|
| **增量更新** | 新文档如何入库 | 按文档 ID 去重，只添加新 chunk |
| **旧文档更新** | 文档修改后怎么办 | 删除旧 chunk → 重新入库 |
| **缓存** | 相似查询重复计算 | 查询向量缓存 + 结果缓存 |
| **检索失败** | 没有相关文档 | score_threshold 过滤 + 兜底回答 |
| **生成拒绝** | LLM 拒绝回答 | 调整 Prompt + 备选模型 |

```python
# 增量更新示例
def add_document(file_path):
    doc_id = hashlib.md5(file_path.encode()).hexdigest()
    # 检查是否已入库
    existing = collection.get(where={"doc_id": doc_id})
    if existing['ids']:
        collection.delete(where={"doc_id": doc_id})  # 删旧
    # 入新
    chunks = process_document(file_path)
    collection.add(..., metadatas=[{"doc_id": doc_id} for _ in chunks])
```

---

## Part 3：Agent 记忆系统（25min）

### Slide 23｜为什么 Agent 需要 Memory？

**LLM 的两个根本限制**：
1. **无状态**：每次请求独立，重启就忘了"我叫张三"
2. **上下文有限**：窗口再大也有上限，长对话早期信息被挤出

**没有 Memory 的 Agent**：
```
用户：我叫张三，我喜欢 Python
Agent：你好张三！
... 10 轮对话后 ...
用户：我叫什么？
Agent：抱歉，我不知道你是谁。  ← 忘了
```

**有 Memory 的 Agent**：
```
用户：我叫什么？
Agent：你叫张三，你喜欢 Python。  ← 从记忆中检索
```

---

### Slide 24｜四类型记忆体系

| 类型 | 存什么 | 生命周期 | 类比 | 实现方式 |
|---|---|---|---|---|
| **工作记忆** | 当前对话上下文 | 会话级 | "现在聊什么" | 滑动窗口 |
| **情景记忆** | 具体交互事件 | 长期 | "上周问过X" | JSON + 时间戳 |
| **语义记忆** | 用户偏好/抽象知识 | 长期 | "喜欢Python" | 向量化存储 |
| **感知记忆** | 多模态信息 | 动态 | "上传的图" | 文件引用 |

---

### Slide 25｜工作记忆：滑动窗口

**最简单的记忆**：保留最近 N 轮对话

```python
class WorkingMemory:
    def __init__(self, max_turns=10):
        self.messages = []
        self.max_turns = max_turns
    
    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        # 滑动窗口：只保留最近 N 轮
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-self.max_turns * 2:]
    
    def get_context(self):
        return self.messages
```

**局限**：超出窗口的信息永久丢失

---

### Slide 26｜情景记忆：记住具体事件

```python
import json
from datetime import datetime

class EpisodicMemory:
    def __init__(self, path="episodic_memory.json"):
        self.path = path
        self.memories = self._load()
    
    def _load(self):
        try:
            with open(self.path) as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_episode(self, event, importance=0.5):
        """保存一个事件"""
        self.memories.append({
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "importance": importance
        })
        with open(self.path, 'w') as f:
            json.dump(self.memories, f, ensure_ascii=False, indent=2)
    
    def recall_recent(self, n=5):
        """回忆最近 N 个事件"""
        return self.memories[-n:]
```

---

### Slide 27｜语义记忆：记住用户偏好

```python
class SemanticMemory:
    def __init__(self, model, collection):
        self.model = model
        self.collection = collection  # ChromaDB collection
    
    def store(self, fact, metadata=None):
        """存储一个知识/偏好"""
        vec = self.model.encode(fact)
        self.collection.add(
            ids=[f"mem_{hash(fact)}"],
            documents=[fact],
            embeddings=[vec.tolist()],
            metadatas=[metadata or {}]
        )
    
    def recall(self, query, top_k=3):
        """根据当前对话召回相关记忆"""
        vec = self.model.encode(query)
        results = self.collection.query(
            query_embeddings=[vec.tolist()],
            n_results=top_k
        )
        return results['documents'][0]
```

> 语义记忆本质就是"对用户信息做 RAG"

---

### Slide 28｜记忆写入：从对话中提取关键信息

```python
def extract_memories(conversation):
    """对话结束后，让 LLM 提取值得记住的信息"""
    prompt = """分析以下对话，提取值得长期记住的用户信息。
只提取确定的事实，每行一条，格式："类别: 内容"

类别包括：姓名、偏好、技能、目标、约束

对话：
""" + "\n".join(f"{m['role']}: {m['content']}" for m in conversation)
    
    response = client.chat.completions.create(
        model="qwen2.5:7b-instruct-q4_K_M",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    facts = response.choices[0].message.content.strip().split('\n')
    return [f.strip() for f in facts if f.strip()]
```

---

### Slide 29｜记忆检索：新对话开始时召回

```python
def build_memory_context(user_message, semantic_mem, episodic_mem):
    """构建记忆上下文，注入到 System Prompt"""
    # 语义记忆：根据当前话题召回相关偏好
    relevant_facts = semantic_mem.recall(user_message, top_k=3)
    
    # 情景记忆：最近几次交互
    recent_episodes = episodic_mem.recall_recent(n=3)
    
    memory_context = "## 用户记忆\n"
    if relevant_facts:
        memory_context += "已知信息：\n"
        memory_context += "\n".join(f"- {f}" for f in relevant_facts)
    if recent_episodes:
        memory_context += "\n\n近期交互：\n"
        memory_context += "\n".join(f"- {e['event']}" for e in recent_episodes)
    
    return memory_context
```

---

### Slide 30｜完整记忆系统串联

```python
class MemoryAgent:
    def __init__(self):
        self.working = WorkingMemory(max_turns=10)
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory(model, mem_collection)
    
    def chat(self, user_message):
        # 1. 召回记忆
        memory_ctx = build_memory_context(
            user_message, self.semantic, self.episodic)
        
        # 2. 构建消息
        system = f"你是用户的个人助手。\n{memory_ctx}"
        self.working.add("user", user_message)
        messages = [{"role": "system", "content": system}] + \
                   self.working.get_context()
        
        # 3. 生成回复
        response = client.chat.completions.create(
            model="qwen2.5:7b-instruct-q4_K_M",
            messages=messages
        )
        reply = response.choices[0].message.content
        self.working.add("assistant", reply)
        
        # 4. 保存记忆
        self.episodic.save_episode(f"用户问:{user_message[:50]}")
        return reply
```

---

### Slide 31｜Memory 与 RAG 的关系

```
┌─────────────────────────────────────────┐
│              用户提问                     │
│                 ↓                        │
│    ┌──────────┐    ┌──────────┐          │
│    │ Memory   │    │  RAG     │          │
│    │ 检索偏好  │    │ 检索知识  │          │
│    └────┬─────┘    └────┬─────┘          │
│         ↓               ↓                │
│    ┌────────────────────────────┐        │
│    │   合并上下文 → LLM 生成    │        │
│    └────────────────────────────┘        │
│                 ↓                        │
│           回复 + 存入 Memory             │
└─────────────────────────────────────────┘
```

| 维度 | Memory | RAG |
|---|---|---|
| 检索对象 | 用户交互历史（动态） | 外部文档知识（静态） |
| 更新频率 | 每次对话后更新 | 文档变更时更新 |
| 目的 | 个性化、连贯性 | 准确性、可溯源 |

> 两者结合 = 既懂你又懂事

---

### Slide 32｜时间衰减：让记忆有"遗忘"

```python
import math
from datetime import datetime

def decay_score(memory, current_time, half_life_days=7):
    """指数衰减：越久远的记忆权重越低"""
    age_days = (current_time - memory['timestamp']).days
    decay = math.exp(-0.693 * age_days / half_life_days)
    return memory['importance'] * decay
```

**为什么需要遗忘**：
- 避免过时信息干扰（"上周喜欢红色" vs "今天改喜欢蓝色"）
- 控制检索结果数量
- 模拟人类记忆衰退

---

### Slide 33｜Memory + RAG 融合实战

```python
def memory_rag_chat(question, memory_agent, rag_collection):
    """融合记忆和 RAG 的问答"""
    # 1. 记忆检索（用户偏好）
    user_prefs = memory_agent.semantic.recall(question, top_k=2)
    
    # 2. RAG 检索（文档知识）
    query_vec = model.encode(question)
    rag_results = rag_collection.query(
        query_embeddings=[query_vec.tolist()], n_results=5
    )
    rag_context = "\n".join(rag_results['documents'][0])
    
    # 3. 合并成 Prompt
    system = f"""你是用户的个人助手。
用户信息：{'; '.join(user_prefs) if user_prefs else '暂无'}

参考资料：
{rag_context}

规则：优先使用参考资料回答，结合用户偏好调整表述风格。"""
    
    response = client.chat.completions.create(
        model="qwen2.5:7b-instruct-q4_K_M",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
```

---

### Slide 34｜衔接第8讲：从 Memory 到 Agent

**本讲实现的记忆系统**：
- 能记住用户是谁（语义记忆）
- 能回忆最近聊了什么（情景记忆）
- 能结合外部知识回答（RAG）

**第8讲 Agent 还需要**：
- **工具调用**：不只能对话，还能搜索/计算/执行代码
- **推理规划**：自主决定调用哪些工具、按什么顺序
- **反思循环**：检查结果是否正确，不正确则重试

```
Memory Agent（本讲） + Tool Use + 推理规划 = 完整 Agent（第8讲）
```

---

## Part 4：小结与实验说明（5min）

### Slide 35｜本讲知识地图

```
RAG 进阶与 Agent 记忆
├── Part 1：高级检索策略
│   ├── MQE 多查询扩展（解决用词不匹配）
│   ├── HyDE 假设文档嵌入（解决语义鸿沟）
│   ├── Reranker 重排序（提升排序精度）
│   └── 混合检索 BM25+向量+RRF（通用最强）
├── Part 2：评估与调优
│   ├── 指标：Recall@k / Precision@k / MRR
│   ├── 调参：chunk_size / top_k / 嵌入模型
│   └── 生产化：增量更新 / 缓存 / 错误处理
└── Part 3：Agent 记忆
    ├── 四类型：工作 / 情景 / 语义 / 感知
    ├── 实现：JSON + 向量化 + 时间衰减
    └── 融合：Memory 偏好 + RAG 知识
```

---

### Slide 36｜知识点速查表

| 模块 | 核心知识点 |
|---|---|
| MQE | LLM 改写 N 个查询，并行检索合并 |
| HyDE | 生成假设答案，用答案向量检索 |
| Reranker | Bi-Encoder 粗排 + Cross-Encoder 精排 |
| 混合检索 | BM25 + 稠密向量 + RRF 融合 |
| Recall@k | top-k 中命中正确答案的比例 |
| MRR | 第一个相关结果的平均倒数排名 |
| 工作记忆 | 滑动窗口，保留最近 N 轮 |
| 情景记忆 | JSON 存储 + 时间戳 + 衰减 |
| 语义记忆 | 向量化存储 + 语义检索 |

---

### Slide 37｜工具速查表

| 工具/库 | 用途 | 核心 API |
|---|---|---|
| rank_bm25 | BM25 稀疏检索 | `BM25Okapi(corpus).get_scores(query)` |
| CrossEncoder | Reranker 精排 | `CrossEncoder('bge-reranker-base').predict(pairs)` |
| jieba | 中文分词（BM25 需要） | `list(jieba.cut(text))` |
| ChromaDB | 向量存储 + 记忆存储 | `collection.query()` / `collection.add()` |
| json | 情景记忆持久化 | `json.dump()` / `json.load()` |

---

### Slide 38｜实验七任务总览

| 任务 | 内容 | 核心技巧 | 分值 |
|---|---|---|---|
| 任务1（25分） | MQE 多查询扩展 | LLM 改写 + 并行检索 + 效果对比 | 25 |
| 任务2（25分） | Reranker 重排序 | CrossEncoder + 两阶段检索 + 效果对比 | 25 |
| 任务3（25分） | 构建评估数据集 + 计算指标 | 至少 10 个 QA 对 + Recall@5 + MRR | 25 |
| 任务4（25分） | 简单记忆系统 | JSON + 向量检索 + 对话演示 | 25 |

**基于第6讲实验的 RAG 系统迭代升级**

---

### Slide 39｜实验七数据与环境

**数据**：复用第6讲实验的 `综述论文.pdf` 和已建好的 ChromaDB

**环境**：
```bash
pip install rank-bm25 jieba sentence-transformers chromadb openai
```

**提交要求**：
- 可运行的 Jupyter Notebook
- 任务1-2 需展示对比表格（基础检索 vs 高级检索的 Recall/MRR）
- 任务3 需展示评估数据集（至少 10 个问答对）
- 任务4 需展示至少 3 轮对话，证明记忆生效

---

### Slide 40｜下讲预告

**第 8 讲：Agent 系统开发**

- 本讲实现了 Memory Agent → 下讲加上工具调用和推理规划
- Part 1：Agent 架构（ReAct / Function Calling）
- Part 2：工具定义与注册
- Part 3：推理-行动循环
- Part 4：综合实战（RAG + Memory + Tools = 完整 Agent）

---

### Slide 41｜课后作业

1. 完成实验七全部 4 个任务，提交实验报告
2. **思考题（二选一）**：
   - a. MQE 和 HyDE 分别适合什么场景？如果你的知识库是中英文混合的，该用哪种策略？
   - b. Agent 的记忆系统和人类记忆有什么相似之处？"遗忘"为什么对 Agent 也是必要的？
3. **拓展阅读**：
   - Gao et al. (2024). Retrieval-Augmented Generation for Large Language Models: A Survey
   - Wang et al. (2023). Query2Doc: Query Expansion with Large Language Models
   - Park et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior

---

## 附录：高级检索策略速查

| 策略 | 一句话原理 | 代码关键 |
|---|---|---|
| MQE | 改写 N 个查询并行搜 | `generate_multi_queries()` → 多次 `query()` → 合并 |
| HyDE | 假设答案做向量 | LLM 生成假设 → `encode(假设)` → `query()` |
| Reranker | 粗排+精排 | `query(n=20)` → `CrossEncoder.predict()` → 取 top-5 |
| 混合检索 | BM25+向量+RRF | `bm25.get_scores()` + `query()` → RRF 公式 |

## 附录：评估指标速查

| 指标 | 公式 | 含义 |
|---|---|---|
| Recall@k | hit_count / total_queries | 召回率 |
| Precision@k | relevant_in_topk / k | 精确率 |
| MRR | mean(1/rank_of_first_hit) | 排序质量 |
| NDCG@k | DCG/IDCG | 加权排序质量（进阶） |
