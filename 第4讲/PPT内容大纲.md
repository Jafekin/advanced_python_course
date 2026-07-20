# 第四讲：NLP 基础与 Prompt 工程

## PPT 内容大纲（约 52 张 Slides）

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 4 讲
**副标题**：NLP 基础与 Prompt 工程
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

### Slide 3｜导入：你一直在和大模型对话

**回顾前三讲经验：**

- 第1讲：两段式 Prompt 驱动 AI 生成 Pandas 数据处理代码
- 第2讲：让 AI 推荐可视化方案、三轮迭代优化图表
- 第3讲：用 Spec-driven 约束 AI 实现工程化模块

**问题**：你知道 AI 是如何理解这些 Prompt 的吗？

**三个真实疑问引入本讲：**

1. 为什么同样的 Prompt，AI 有时给出不同答案？（采样参数）
2. AI 是怎么理解文字的？"你好"对它来说是什么？（Tokenization）
3. 怎么让 AI 稳定地按我想要的格式输出？（Prompt Engineering）

---

### Slide 4｜本讲的价值定位

**从"使用者"到"工程师"的转变：**

```text
第1-2讲：使用 AI 工具完成数据分析和建模任务
第4讲：  理解 AI 背后的原理，系统化地设计 Prompt
```

**本讲的核心收获：**

- 会用 tiktoken 控制上下文预算，不再被 Token 限制卡住
- 能设计有效的 System Prompt，让 API 稳定输出结构化结果
- 理解幻觉成因，建立正确的 AI 使用心态

---

### Slide 5｜语言模型是什么

**语言模型（Language Model）的根本任务：计算一个句子出现的概率**

$$P(S) = P(w_1) \cdot P(w_2|w_1) \cdot P(w_3|w_1,w_2) \cdots P(w_m|w_1,...,w_{m-1})$$

**类比**：语言模型就是在玩"文字接龙"——给定前文，预测下一个最可能的词。

**演进路线**：

| 阶段     | 模型              | 特点             | 缺陷          |
| ------ | --------------- | -------------- | ----------- |
| 统计时代   | N-gram          | 简单计数，看前 N-1 个词 | 无法处理未见过的词组合 |
| 神经网络   | RNN/LSTM        | 有"记忆"，可处理变长序列  | 顺序计算慢，长距离遗忘 |
| **当代** | **Transformer** | 注意力机制，完全并行     | 计算量大，需海量数据  |

今天使用的 ChatGPT、DeepSeek、Qwen 全部基于 Transformer 的 Decoder-Only 架构。

---

### Slide 6｜Transformer 架构核心思想（概览）

**自注意力机制（Self-Attention）**：处理每个词时，能"看到"整个句子的其他词

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

**类比**：读到"它"这个字时，大脑会自动回溯找到"它"指代的那个名词

**Decoder-Only 架构**（GPT 系列采用）：

- 只保留解码器，专注"预测下一个词"
- 因果掩码：只能看到当前位置之前的词，不能偷看后面
- 自回归生成：一个词一个词地往后写

> 本讲只做概念性介绍，Transformer 细节将在第五讲深入展开。

---

### Slide 7｜为什么需要分词（Tokenization）

**问题**：计算机只认识数字，如何让模型"看懂"文字？

**分词 = 将文本转换为模型可处理的数字序列**

三种分词策略对比：

| 方案          | 示例                     | 优点        | 缺点          |
| ----------- | ---------------------- | --------- | ----------- |
| 按词分         | ["Hello", "world"]     | 直观        | 词表爆炸、无法处理新词 |
| 按字符分        | ["H","e","l","l","o"]  | 词表小       | 单字符无语义、序列太长 |
| **子词分（主流）** | ["Hello", "wor", "ld"] | 平衡词表大小和语义 | 需要算法设计      |

现代大模型（GPT、DeepSeek、Qwen）统一采用**子词分词**。

---

### Slide 8｜BPE 算法：子词分词的核心

**BPE（Byte-Pair Encoding）= 贪心合并最高频相邻对**

训练过程（迷你语料：`{"hug":1, "pug":1, "pun":1, "bun":1}`）：

| 步骤  | 词表                | 最高频对     | 合并结果                     |
| --- | ----------------- | -------- | ------------------------ |
| 初始  | {h,u,g,p,n,b} (6) | —        | —                        |
| 1   | +ug (7)           | u+g→ug   | h ug, p ug, p u n, b u n |
| 2   | +un (8)           | u+n→un   | h ug, p ug, p un, b un   |
| 3   | +hug (9)          | h+ug→hug | hug, p ug, p un, b un    |
| 4   | +pug (10)         | p+ug→pug | hug, pug, p un, b un     |

对未见过的词 "bug"：查找 → b + ug → `['b', 'ug']`

---

### Slide 9｜BPE 算法 Python 实现

```python
def train_bpe(corpus, num_merges):
    """BPE 训练：迭代合并最高频相邻 token 对"""
    # 初始化：每个词拆成字符列表
    vocab = {word: list(word) for word in corpus}
    merges = []

    for step in range(num_merges):   # 外层用 step，避免与内层 i 冲突
        # 统计所有相邻 token 对的频率
        pairs = {}
        for word, freq in corpus.items():
            tokens = vocab[word]
            for j in range(len(tokens) - 1):
                pair = (tokens[j], tokens[j+1])
                pairs[pair] = pairs.get(pair, 0) + freq

        if not pairs:
            break
        # 找到频率最高的 pair 并合并
        best_pair = max(pairs, key=pairs.get)
        new_token = best_pair[0] + best_pair[1]
        merges.append(best_pair)

        # 在所有词中执行合并
        for word in vocab:
            tokens = vocab[word]
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens)-1 and (tokens[i], tokens[i+1]) == best_pair:
                    new_tokens.append(new_token)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            vocab[word] = new_tokens

        print(f"步骤 {step+1}: 合并 {best_pair} → '{new_token}'")

    return merges, vocab
```

---

### Slide 10｜tiktoken 实操：Token 计算

```python
import tiktoken

# 加载 GPT-4 使用的分词器
enc = tiktoken.encoding_for_model("gpt-4")

# 中英文 Token 计算对比
text_en = "Hello, how are you?"
text_zh = "你好，最近怎么样？"

tokens_en = enc.encode(text_en)
tokens_zh = enc.encode(text_zh)

print(f"英文: {len(tokens_en)} tokens → {tokens_en}")
print(f"中文: {len(tokens_zh)} tokens → {tokens_zh}")

# 解码验证
for t in tokens_zh:
    print(f"  Token {t} → '{enc.decode([t])}'")
```

**关键发现**：中文通常 1 个汉字 = 1-2 个 Token；英文 1 个词 ≈ 1-3 个 Token

---

### Slide 11｜Token 对开发者的实际意义

**三个直接影响：**

| 维度            | 影响             | 实际场景                              |
| ------------- | -------------- | --------------------------------- |
| **上下文窗口**     | 模型能"看到"的最大范围   | GPT-5.5: 1M tokens ≈ 75万字中文      |
| **计费**        | API 按 Token 计费 | DeepSeek-V4-Flash: ¥1/百万 input tokens |
| **Prompt 长度** | 决定你能给模型多少信息    | 长文档需要截断或分块处理                      |

**实用技巧**：

- 用 tiktoken 预估成本：`tokens × 单价`
- 中文 Prompt 比等长英文更"贵"（Token 数更多）
- 上下文预算分配：System Prompt 占 10-20%，用户输入占 30-40%，预留生成空间

---

### Slide 12｜采样参数：Temperature

**Temperature = 控制输出的"随机性"**

原理：在 Softmax 中引入温度系数 T

$$p_i^{(T)} = \frac{e^{z_i/T}}{\sum_{j=1}^k e^{z_j/T}}$$

| Temperature   | 效果        | 适用场景           |
| ------------- | --------- | -------------- |
| 0 ~ 0.3（低温）   | 确定性高，重复率高 | 代码生成、事实问答、数据提取 |
| 0.3 ~ 0.7（中温） | 平衡自然      | 日常对话、邮件撰写      |
| 0.7 ~ 2.0（高温） | 创意发散      | 诗歌创作、头脑风暴      |

**Temperature=0**：始终选概率最高的 Token，输出完全确定

---

### Slide 13｜采样参数：Top-k 与 Top-p

**Top-k**：只从概率最高的 k 个词中采样

- k=1：等同于贪心解码，完全确定
- k=50：从前50个候选词中随机选

**Top-p（核采样）**：累积概率达到 p 就停止

- p=0.9：保留累积概率达到90%的最小词集合
- 动态调整候选数量（概率集中时候选少，分散时候选多）

**组合使用优先级**：Temperature → Top-k → Top-p

```python
response = client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=messages,
    temperature=0.7,   # 中等随机
    top_p=0.9,         # 核采样
    max_tokens=500     # 最大生成长度
)
```

---

### Slide 14｜采样参数对比实验（现场演示）

**同一 Prompt，不同参数效果对比：**

Prompt：`"写一句关于春天的诗"`

| 参数组合             | 输出示例      | 特点          |
| ---------------- | --------- | ----------- |
| T=0              | "春风又绿江南岸" | 每次都一样，最"安全" |
| T=0.7, top_p=0.9 | "柳絮飘飞入画廊" | 自然多样        |
| T=1.5            | "紫云翻涌鲤跃荷" | 有创意但可能不通顺   |


---

### Slide 15｜Prompt Engineering：为什么重要

**Prompt = 与大模型沟通的"编程语言"**

| 传统编程             | Prompt Engineering |
| ---------------- | ------------------ |
| 写 Python/Java 代码 | 写自然语言指令            |
| 编译器执行            | 大模型执行              |
| 语法错误会报错          | 表达不清会得到错误输出        |
| 确定性结果            | 概率性结果（需要约束）        |

**Prompt Engineering 的目标**：用最少的 Token、最清晰的表达，让模型稳定输出你想要的结果。

**与前两讲的关系**：

- 第1讲的"两段式 Prompt"（先氛围后约束）是 PE 的一种简单形式
- 本讲将它升级为完整的方法论体系

---

### Slide 16｜Zero-shot / One-shot / Few-shot

**根据提供示例数量分类：**

**Zero-shot（零样本）**——直接下指令：

```
判断以下文本的情感倾向（正面/负面/中性）：
文本：北航计算机学院的 Python 进阶课程内容很扎实！
情感：
```

**One-shot（单样本）**——给一个示例：

```
文本：这家餐厅的服务太慢了。
情感：负面

文本：北航计算机学院的 Python 进阶课程内容很扎实！
情感：
```

**Few-shot（少样本）**——给多个示例：

```
文本：这家餐厅的服务太慢了。 → 负面
文本：今天天气不错，心情很好。 → 正面
文本：快递已送达。 → 中性

文本：北航计算机学院的 Python 进阶课程内容很扎实！ → 
```

示例越多，模型对任务边界理解越准确。

---

### Slide 17｜角色扮演（Role Prompting）

**通过赋予模型角色，控制回答风格、知识范围和语气**

```python
messages = [
    {"role": "system", "content": 
     "你是一位资深 Python 数据分析专家，拥有10年经验。"
     "回答时使用中文，给出代码示例，并解释背后的设计考量。"},
    {"role": "user", "content": "如何高效处理百万行 CSV？"}
]
```

**System Prompt 设计三要素**：

| 要素   | 示例                | 作用     |
| ---- | ----------------- | ------ |
| 身份定义 | "你是资深 Python 专家"  | 激活相关知识 |
| 行为约束 | "回答用中文，附代码"       | 控制输出格式 |
| 边界限制 | "只回答 Python 相关问题" | 防止跑题   |


---

### Slide 18｜思维链（Chain-of-Thought, CoT）

**核心思想：引导模型"一步一步地思考"**

**不用 CoT（直接回答，容易出错）**：

```
问：一个篮球队80场赢了60%，接下来15场赢了12场，两赛季总胜率？
答：63%（错误）
```

**使用 CoT（加一句引导语）**：

```
问：... 请一步一步地思考。
答：
第一步：第一赛季胜场 = 80 × 60% = 48场
第二步：总比赛数 = 80 + 15 = 95场
第三步：总胜利 = 48 + 12 = 60场
第四步：总胜率 = 60/95 ≈ 63.16%
```

**CoT 适用场景决策**：

| 任务类型    | 推荐策略                 |
| ------- | -------------------- |
| 简单分类/提取 | Zero-shot 或 Few-shot |
| 需要推理/计算 | CoT（"请逐步思考"）         |
| 格式严格    | 结构化输出                |
| 复杂多步骤   | CoT + Few-shot       |

---

### Slide 19｜结构化输出

**让模型按指定格式返回结果，便于程序解析**

```
请从以下产品评论中提取信息，严格按 JSON 格式输出：

评论：这款"星尘"笔记本电脑屏幕效果惊人，但键盘手感不太好。

输出格式：
{
  "product_name": "产品名称",
  "sentiment": "正面/负面/混合",
  "pros": ["优点列表"],
  "cons": ["缺点列表"]
}
```

**关键技巧**：

- 明确给出 JSON/XML/表格等目标格式
- 提供一个完整示例
- 加约束："严格按照上述格式，不要添加额外内容"

**工具线衔接**：结构化输出 = 让 AI 的结果可以被代码直接 `json.loads()` 解析

---

### Slide 20｜Prompt Engineering 策略选择决策树

```text
你的任务是什么？
├── 简单分类/判断 → Zero-shot（直接问）
├── 需要特定输出风格 → Few-shot（给示例）
├── 需要推理/计算 → CoT（"请逐步思考"）
├── 需要稳定格式 → 结构化输出（给 JSON 模板）
├── 复杂多步骤任务 → CoT + Few-shot + System Prompt
└── 不确定 → 先试 Zero-shot，效果不好再升级
```

**迭代原则**：从最简单的策略开始，根据效果逐步加码

**与 Vibe Coding 的映射**：

- Zero-shot ≈ 第一轮氛围 Prompt
- Few-shot ≈ @文件引用提供示例
- CoT ≈ Speckit 中的 plan 步骤
- System Prompt ≈ Rules 文件

---

### Slide 21｜工具线衔接：从 Vibe Coding 到通用 PE

| 第1讲 Vibe Coding 技巧 | 本讲 PE 方法论               | 本质     |
| ------------------ | ----------------------- | ------ |
| 两段式 Prompt         | Zero-shot → Few-shot 升级 | 迭代细化   |
| Rules 文件           | System Prompt           | 全局风格控制 |
| @文件引用              | Few-shot 示例 / 上下文注入     | 精准信息供给 |
| Diff 审查            | 幻觉检测与验证                 | 输出质量把关 |
| Inline Edit        | 参数调优（Temperature等）      | 快速迭代   |

**核心认知**：Vibe Coding 就是 Prompt Engineering 在编程场景的具体应用。

---

### Slide 22｜大模型 API 调用：消息结构

**OpenAI 兼容 API 的 messages 格式**：

```python
messages = [
    {"role": "system", "content": "你是一个 NLP 助手..."},   # 系统指令
    {"role": "user", "content": "请分析这段文本的情感"},       # 用户输入
    {"role": "assistant", "content": "这段文本的情感是..."},  # AI 回复
    {"role": "user", "content": "为什么这么判断？"}           # 多轮对话
]
```

**三种角色**：

| role      | 作用                | 对应 Vibe Coding  |
| --------- | ----------------- | --------------- |
| system    | 全局指令，定义 AI 的身份和行为 | Rules 文件        |
| user      | 用户的每一轮输入          | Chat 框中的 Prompt |
| assistant | AI 的历史回复（多轮对话上下文） | 会话层上下文          |

---

### Slide 23｜API 调用实践：环境配置

```python
# 安装依赖
# pip install openai tiktoken

from openai import OpenAI

# 创建客户端（课程统一使用 硅基流动 API）
client = OpenAI(
    api_key="sk-xxxxxxxx",  
    base_url="https://api.siliconflow.cn/v1"
)

# 第一次调用
response = client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=[
        {"role": "system", "content": "你是一个简洁的助手，回答不超过50字"},
        {"role": "user", "content": "什么是自然语言处理？"}
    ],
    temperature=0.3
)

print(response.choices[0].message.content)
# → "自然语言处理（NLP）是让计算机理解、生成和处理人类语言的AI技术分支。"
```

---

### Slide 24｜API 实战：情感分类任务

```python
def classify_sentiment(text):
    """使用 Few-shot + 结构化输出完成情感分类"""
    system_prompt = """你是情感分析专家。对输入文本判断情感，严格按 JSON 格式输出。
		输出格式：{"sentiment": "正面/负面/中性", "confidence": 0.0到1.0的浮点数}
		不要添加任何其他内容。"""
    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f'文本："{text}"\n输出：'}
        ],
        temperature=0
    )
    return response.choices[0].message.content

# 测试
print(classify_sentiment("这门课让我学到了很多新知识"))
# → {"sentiment": "正面", "confidence": 0.92}
```

---

### Slide 25｜API 实战：信息抽取任务

```python
def extract_info(review):
    """从产品评论中提取结构化信息"""
    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=[
            {"role": "system", "content": """你是信息抽取专家。
				从产品评论中提取以下字段，严格按JSON格式输出：
				{
				  "product": "产品名称",
				  "pros": ["优点列表"],
				  "cons": ["缺点列表"],
				  "rating": 推测评分(1-5)
				}
				不要添加任何其他内容。"""},
            {"role": "user", "content": review}
        ],
        temperature=0
    )
    return response.choices[0].message.content

result = extract_info(
    "这款华为 MatePad 平板续航超强，能用一整天，"
    "但是扬声器音质一般，看视频体验打折扣。"
)
print(result)
```

---

### Slide 26｜API 实战：文本摘要任务

```python
def summarize(text, max_words=50):
    """使用 CoT 策略生成摘要"""
    response = client.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=[
            {"role": "system", "content": f"""你是摘要专家。
				请按以下步骤生成摘要：
				1. 识别文本的核心主题
				2. 提取 3 个关键信息点
				3. 用不超过{max_words}字组织成流畅的摘要
				只输出最终摘要，不需要展示中间步骤。"""},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
```

**三类 NLP 任务的 PE 策略对比**：

| 任务   | Temperature | 策略                          | 关键技巧   |
| ---- | ----------- | --------------------------- | ------ |
| 情感分类 | 0           | Few-shot + JSON             | 给示例锁格式 |
| 信息抽取 | 0           | System Prompt + JSON Schema | 明确字段定义 |
| 文本摘要 | 0.3         | CoT + 长度约束                  | 步骤引导   |

---

### Slide 27｜模型选择：四大考量维度

**选择大模型不是"越大越强"，而是多维度权衡：**

| 维度        | 关键问题        | 权衡点                  |
| --------- | ----------- | -------------------- |
| **性能**    | 任务能力够不够？    | 推理/代码/中文等专项能力        |
| **成本**    | Token 单价多少？ | 输入/输出分别计费            |
| **速度**    | 响应延迟可接受吗？   | 首 Token 延迟、生成速度      |
| **上下文长度** | 需要处理多长的文档？  | 4K / 32K / 128K / 2M |

**选型决策树**：

```text
需要最强推理/代码能力？ → 是 → GPT-5.5 / Claude Opus 4.8 / DeepSeek-V4-Pro
→ 否 ↓
数据敏感或需本地部署？ → 是 → Qwen3 / LLaMA 4 / DeepSeek-V4-Flash 开源版
→ 否 ↓
预算有限？ → 是 → DeepSeek-V4-Flash / Qwen3-8B（性价比高）
→ 否 → 闭源 API（开箱即用）
```

---

### Slide 28｜闭源模型概览

| 模型               | 厂商        | 特点                        | 上下文  | 适用场景            |
| ---------------- | --------- | ------------------------- | ---- | --------------- |
| GPT-5.5          | OpenAI    | 最新旗舰，推理强，1M 上下文           | 1M   | 复杂推理、代码、多模态     |
| Claude Opus 4.8  | Anthropic | 长文档处理强，安全性高               | 200K | 企业应用、文档分析       |
| Gemini 2.5 Pro   | Google    | 原生多模态，超长上下文               | 2M   | 海量信息、视频理解       |
| 通义千问 Qwen3.5     | 阿里        | 混合推理，中文优秀，成本低             | 256K | 中文对话、内容生成、推理    |
| 智谱 GLM-5.2       | 智谱        | 744B MoE，Agent 能力强，MIT 开源 | 200K | 中文应用、代码、逻辑推理    |
| DeepSeek-V4-Flash | 深度求索     | 284B MoE，轻量快速，性价比高         | 1M   | 日常任务、高并发、成本敏感   |
| DeepSeek-V4-Pro  | 深度求索      | 1.6T MoE 旗舰，推理能力顶尖        | 1M   | 顶级推理、Agent 开发  |

**特点**：开箱即用、性能前沿、按量计费、数据需上传

---

### Slide 29｜开源模型概览

| 模型                  | 参数规模         | 特点                               | 适用场景          |
| --------------------- | ------------ | -------------------------------- | ------------- |
| LLaMA 4               | 17B-405B     | Meta 出品，原生多模态，生态成熟               | 研究、定制化        |
| Qwen3（通义千问）      | 0.6B-235B    | 阿里出品，混合推理，中文强，多尺寸               | 中文应用、边缘到云端部署  |
| DeepSeek-V4-Flash     | 284B (MoE)   | MIT 开源，轻量快速，1M 上下文，性价比极高        | 日常任务、高并发、成本敏感 |
| DeepSeek-V4-Pro       | 1600B (MoE)  | MIT 开源，旗舰推理，1M 上下文               | 复杂推理、数学、Agent |
| GLM-5.2（智谱）        | 744B (MoE)   | MIT 开源，Agent 能力强，200K 上下文        | 中文应用、代码、逻辑推理  |
| Mistral / Mixtral     | 7B-141B(MoE) | 欧洲出品，小尺寸高性能                      | 资源受限环境、多语言    |

**开源 vs 闭源对比**：

| 维度  | 闭源         | 开源           |
| --- | ---------- | ------------ |
| 部署  | API 调用即可   | 需本地 GPU/下载权重 |
| 成本  | 按 Token 计费 | 仅硬件成本        |
| 定制  | 只能调 Prompt | 可微调权重        |
| 数据  | 需上传到厂商     | 完全本地，数据安全    |
| 性能  | 通常更强       | 中等模型略弱       |

> 开源模型的本地部署与微调将在第5-6讲深入展开。

---

### Slide 30｜缩放法则（Scaling Laws）

**核心发现：模型性能与参数量、数据量、计算量呈幂律关系**

$$L(N) \propto N^{-\alpha}, \quad L(D) \propto D^{-\beta}, \quad L(C) \propto C^{-\gamma}$$

**三个关键洞察**：

1. **持续投入有回报**：按比例增加参数/数据/算力，性能可预测提升
2. **Chinchilla 定律**（DeepMind 2022）：给定算力预算下，参数量和数据量存在最优配比——70B 模型 + 4倍数据，性能超越 175B 的 GPT-3
3. **能力涌现**：模型规模达阈值后突然出现新能力（CoT 推理、指令遵循、代码生成）

**对开发者的启示**：

- 选模型时不能只看参数量，还要看训练数据量
- "涌现能力"意味着复杂任务需要足够大的模型
- 2023 年后模型同质化加剧，差距主要在数据和对齐

---

### Slide 31｜模型幻觉（Hallucination）

**幻觉 = 模型自信地生成与事实矛盾或不存在的内容**

**三种典型幻觉**：

| 类型    | 示例                | 特点          |
| ----- | ----------------- | ----------- |
| 事实性幻觉 | 虚构论文引用、不存在的历史事件   | 最常见，最危险     |
| 忠实性幻觉 | 总结时偏离原文、添加未提及内容   | RAG 系统的高发问题 |
| 逻辑幻觉  | 推理链条中间步骤出错但结论看似合理 | CoT 也无法完全避免 |

**产生原因**：

- 训练数据含错误/矛盾信息
- 自回归生成本质是"预测下一个最可能的词"，无事实核查
- 知识时效性：训练截止后的事件模型不知道

---

### Slide 32｜幻觉缓解策略

**四层防护**：

| 层级           | 策略           | 示例                    |
| ------------ | ------------ | --------------------- |
| **Prompt 层** | 明确边界         | "如果不确定，请说'我不知道'，不要编造" |
| **推理层**      | CoT 自我验证     | 让模型分步推理后再检查每一步        |
| **系统层**      | RAG 检索增强     | 先查文档再回答               |
| **工程层**      | 多模型投票 + 人工审核 | 关键场景必须人工把关            |

**Prompt 层缓解示例**：

```
请仅基于以下文档回答问题，不要使用文档外的知识。
如果文档中没有相关信息，请明确说"文档中未提及"。

【文档】...
【问题】...
```

第1讲的"Diff 审查"习惯，本质上就是人工幻觉检测。

---

### Slide 33｜本讲知识地图

```text
NLP 基础与 Prompt 工程
├── 语言模型演进
│   ├── N-gram → RNN/LSTM → Transformer（预告第5讲深入）
│   └── Decoder-Only 架构（GPT 系列）
├── 分词（Tokenization）
│   ├── 子词分词思想
│   ├── BPE 算法（贪心合并）
│   └── tiktoken 工具（Token 计算）
├── 采样参数
│   ├── Temperature（随机性）
│   ├── Top-k / Top-p（候选截断）
│   └── 组合策略
├── Prompt Engineering
│   ├── Zero/One/Few-shot
│   ├── 角色扮演（System Prompt）
│   ├── 思维链（CoT）
│   ├── 结构化输出
│   └── 策略决策树
├── API 调用
│   ├── messages 结构
│   └── 三类 NLP 任务实战
├── 模型选择
│   └── 闭源 vs 开源
└── 局限性
    ├── 缩放法则
    └── 模型幻觉 + 缓解策略
```

---

### Slide 34｜实验任务总览

| 任务       | 内容                       | 核心技巧                    | 分值  |
| -------- | ------------------------ | ----------------------- | --- |
| 任务1（40分） | BPE 分词算法实现 + tiktoken 对比 | Python 实现 BPE 训练过程      | 40  |
| 任务2（60分） | Prompt Engineering 对比实验  | Zero/Few-shot/CoT 三策略对比 | 60  |
| 任务3（**选做**，+35分） | 大模型 API 应用开发      | 情感分类 + 信息抽取 + 摘要        | +35 |

> 必做满分 100 分，完成任务3可额外获得 35 分加分。

**实验数据**：课程统一提供 DeepSeek API Key，三组真实文本数据放在 `实验三/` 目录

**完成标准**：

- 任务1、2为必做，提交可运行代码 + 运行结果截图
- 任务2需提交三种策略的输出对比表
- 任务3为选做，完成任务1、2即视为完成必做部分；完成任务3者需提交 JSON 结构化输出

---
### Slide 38｜本讲小结

**知识收获**：

- 语言模型演进：N-gram → RNN/LSTM → Transformer（Decoder-Only）
- 分词原理：子词分词、BPE 算法、tiktoken 工具
- 采样参数：Temperature / Top-k / Top-p 的原理与组合
- Prompt Engineering：Zero/Few-shot、角色扮演、CoT、结构化输出
- API 调用：messages 结构 + 三类 NLP 任务实战
- 模型选择：闭源 vs 开源的四维权衡
- 局限性：缩放法则 + 幻觉成因与缓解

---

### Slide 40｜课后作业

1. 完成实验三任务1、任务2（必做），有余力者完成任务3（选做），提交实验报告

2. **思考题（三选一）**：
   
   - a. Temperature=0 和 Temperature=1.5 分别适合什么场景？做代码生成助手该如何设置采样参数？
   
   - b. CoT 为什么能提升推理准确率？它有什么局限性？什么场景下反而会降低性能？
   
   - c. 大模型的"幻觉"如何检测？RAG 和 CoT 自我验证哪种更适合"事实性问答"？

3. **拓展阅读**：
   
   - OpenAI Prompt Engineering Guide
   
   - Wei et al. (2022). Chain-of-Thought Prompting
   
   - Kaplan et al. (2020). Scaling Laws for Neural Language Models

---

## 附录：Prompt Engineering 速查表

| 策略        | 适用场景       | 关键写法         |
| --------- | ---------- | ------------ |
| Zero-shot | 简单任务、模型能力强 | 直接下指令        |
| One-shot  | 需要格式示范     | 给一个示例        |
| Few-shot  | 任务边界复杂     | 给 3-5 个示例    |
| 角色扮演      | 需要专业风格     | "你是一位资深..."  |
| CoT       | 推理/计算任务    | "请一步一步地思考"   |
| 结构化输出     | 需程序解析      | 给 JSON 模板    |
| 约束边界      | 防幻觉        | "仅基于以下文档..." |

## 附录：采样参数速查表

| 参数          | 范围    | 作用     | 推荐值                    |
| ----------- | ----- | ------ | ---------------------- |
| Temperature | 0-2   | 控制随机性  | 代码:0 / 对话:0.7 / 创意:1.0 |
| Top-k       | 1-100 | 候选词数量  | 40 (通用)                |
| Top-p       | 0-1   | 累积概率阈值 | 0.9 (通用)               |
| max_tokens  | -     | 最大生成长度 | 根据任务设                  |
| stream      | bool  | 流式输出   | True (用户体验好)           |

## 附录：OpenAI 兼容 API 速查

| 操作          | 代码                                                        |
| ----------- | --------------------------------------------------------- |
| 创建客户端       | `client = OpenAI(api_key=..., base_url=...)`              |
| 对话补全        | `client.chat.completions.create(model=..., messages=...)` |
| 取回复内容       | `response.choices[0].message.content`                     |
| 取 Token 用量  | `response.usage.total_tokens`                             |
| 流式输出        | `stream=True`, 迭代 `response`                              |
| tiktoken 编码 | `enc = tiktoken.encoding_for_model("gpt-4")`              |
| 计算 Token 数  | `len(enc.encode(text))`                                   |
