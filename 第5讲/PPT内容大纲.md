# 第五讲：NLP 进阶与模型微调

## PPT 内容大纲（约 46 张 Slides）

---

### Slide 1｜封面

**标题**：Python 进阶 · 第 4 讲
**副标题**：NLP 进阶与模型微调——从黑盒调用到白盒定制
**教师**：孙青 / 欧阳元新 · 计算机学院
**平台**：CloudStudio + CodeBuddy

---

### Slide 2｜本讲全景导航

**两条主线同步推进：**

| 知识线                       | 工具线                          |
| --------------------------- | ------------------------------ |
| 语言模型演进（N-gram → Transformer） | Spec-driven：用 Speckit 描述微调任务 |
| 三种预训练架构（BERT/GPT/T5）     | CodeBuddy 生成训练代码             |
| Hugging Face 微调实战          | Inline Edit 调整超参数             |
| LoRA 参数高效微调               | Rules 定义项目规范 + 斜杠指令调试       |

---

### Slide 3｜从第4讲到第5讲：从调用者到理解者

| 第4讲：NLP 基础与 Prompt 工程 | 第5讲：NLP 进阶与模型微调       |
| ----------------------- | ----------------------- |
| 调用大模型 API              | 理解模型内部架构                |
| 设计 Prompt 让模型回答更好       | 用自己的数据让模型表现更好           |
| 把模型当黑盒                  | 打开黑盒，看 Q/K/V 怎么流动        |
| 工具：Prompt、Few-shot、CoT  | 工具：Transformers、PEFT、Trainer |

**核心问题驱动**：「我们已经能调用大模型了，但模型内部是什么？能否让它在我们的数据上表现更好？」

---

### Slide 4｜本讲知识地图

```
语言模型演进
   └─ N-gram → RNN/LSTM → Transformer
                              │
                   ┌──────────┼──────────┐
                   │          │          │
                BERT        GPT        T5
              (Encoder)  (Decoder)  (Enc-Dec)
              双向理解      自回归生成   文本到文本
                   │
          ┌────────┴────────┐
          │                 │
       全参数微调           LoRA 微调
       (更新所有参数)      (只训练少量参数)
          │                 │
       Hugging Face        peft 库
       Transformers
```

---

### Slide 5｜语言模型的核心任务

**语言模型 (Language Model, LM)**：计算一个词序列出现的概率

$$P(S) = P(w_1) \cdot P(w_2|w_1) \cdot P(w_3|w_1,w_2) \cdots P(w_m|w_1,\dots,w_{m-1})$$

**演进脉络**：

| 阶段          | 代表方法              | 核心思想                | 局限            |
| ----------- | ----------------- | ------------------- | ------------- |
| 统计语言模型      | N-gram            | 马尔可夫假设，看前 n-1 个词     | 稀疏性 + 泛化差     |
| 神经网络语言模型    | Word2Vec / NNLM   | 词嵌入，连续向量表示           | 固定窗口          |
| 循环神经网络      | RNN / LSTM        | 引入"记忆"，处理变长序列        | 无法并行 + 长距依赖弱  |
| **Transformer** | **Attention**     | **完全并行，全局注意力**       | **计算量随长度平方增长** |

---

### Slide 6｜N-gram 的两大致命缺陷

**缺陷一：数据稀疏性 (Sparsity)**

如果 "robot learns" 在语料库中从未出现过，N-gram 计算出的概率就是 0：

```python
# Bigram 示例
P(learns|robot) = Count("robot learns") / Count("robot")
                = 0 / 1 = 0   # 完全没见过 → 概率为 0
```

**缺陷二：泛化能力差**

模型不理解 `agent` 和 `robot` 在语义上相似——它把每个词当作孤立的离散符号。

**根本原因**：词被表示为离散的 one-hot 向量，无法捕捉语义相似性。

---

### Slide 7｜词嵌入：从离散符号到连续语义空间

**核心思想**：把每个词映射为高维连续向量（词嵌入 Word Embedding）

```python
# 经典语义类比：King - Man + Woman ≈ Queen
import numpy as np

embeddings = {
    "king":   np.array([0.9, 0.8]),
    "queen":  np.array([0.9, 0.2]),
    "man":    np.array([0.7, 0.9]),
    "woman":  np.array([0.7, 0.3])
}

result = embeddings["king"] - embeddings["man"] + embeddings["woman"]
# result = [0.9, 0.2] → 与 queen 完全一致
```

**余弦相似度**衡量语义接近程度：

$$\text{similarity}(\vec{a}, \vec{b}) = \cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}||\vec{b}|}$$

语义相近的词 → 向量夹角小 → 余弦值接近 1。

---

### Slide 8｜RNN/LSTM：引入"记忆"但无法并行

**RNN 核心思想**：用隐藏状态 $h_t$ 作为"短期记忆"，结合当前输入 $x_t$ 和上一刻记忆 $h_{t-1}$ 生成新记忆：

$$h_t = f(h_{t-1}, x_t)$$

**LSTM 创新**：引入细胞状态 + 门控机制（遗忘门/输入门/输出门），缓解梯度消失。

**致命瓶颈**：必须按顺序计算，第 t 步等第 t-1 步完成才能开始 → **无法并行**，训练慢。

```
RNN 时序：[x1] → [x2] → [x3] → ... → [xm]   串行
Transformer: [x1, x2, x3, ..., xm] 一次性全部处理   并行
```

---

### Slide 9｜Transformer 的革命（2017）

**论文**：Vaswani et al. "Attention Is All You Need" (2017)

**革命性主张**：完全抛弃循环结构，**只用注意力机制**捕捉序列内的依赖关系。

| 对比项         | RNN/LSTM        | Transformer        |
| ----------- | --------------- | ------------------ |
| 计算方式        | 顺序计算            | 并行计算               |
| 长距离依赖       | 弱（梯度消失）         | 强（一步直达）            |
| 训练速度        | 慢               | 快（GPU 友好）          |
| 复杂度（序列长度）   | O(n)            | O(n²)              |

**代价**：序列长度增加时，注意力复杂度是平方级 O(n²)——这是后续 Longformer、Linformer 等改进的动机。

---

### Slide 10｜Encoder-Decoder 整体结构

**最初的 Transformer 为机器翻译设计**：

```
输入句子 → [Encoder × N] → 上下文向量 → [Decoder × N] → 输出句子
            "理解"                       "生成"
```

| 组件                | 职责                       | 类比         |
| ----------------- | ------------------------ | ---------- |
| **编码器 (Encoder)** | 读取整个输入句子，为每个词生成富含上下文的向量 | "通读全文做笔记"  |
| **解码器 (Decoder)** | 参考已生成的前文 + 编码器的笔记，生成下一个词 | "看着笔记写作文"  |

每个 Encoder/Decoder 层内部都包含：多头注意力 + 前馈网络 + 残差连接 + 层归一化。

---

### Slide 11｜自注意力机制：直觉理解

**场景**：阅读句子 "The agent learns because **it** is intelligent."

读到 "**it**" 时，大脑会自动将注意力放在 "agent" 上——自注意力就是对这种过程的数学建模。

**三个核心角色**（每个词元都有）：

| 角色              | 含义              | 类比         |
| --------------- | --------------- | ---------- |
| **Query (Q)**   | 当前词想找什么信息       | "你的问题"     |
| **Key (K)**     | 这个词能提供什么索引      | "书名标签"     |
| **Value (V)**   | 这个词实际携带的内容      | "书的内容"     |

Q、K、V 都由输入向量乘以可学习的权重矩阵 $W^Q, W^K, W^V$ 得到。

---

### Slide 12｜自注意力机制：四步计算

**Step 1**：计算相关性得分 $QK^T$（每个词对其他所有词的关注度）

**Step 2**：缩放 $\div \sqrt{d_k}$（防止点积过大导致梯度过小）

**Step 3**：Softmax 归一化（分数转为和为 1 的权重）

**Step 4**：加权求和（权重 × V）

**最终公式**：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

**为什么除以 $\sqrt{d_k}$？** 当 $d_k$ 较大时，点积结果方差大，Softmax 后会落到梯度极小的区域，缩放后让分布更平滑。

---

### Slide 13｜自注意力计算示例（3×3 手动推导）

```python
import numpy as np

# 3 个词，每个词 4 维嵌入
X = np.random.randn(3, 4)
Q = K = V = X  # 简化：Q=K=V=X

# Step 1: 相关性得分
scores = Q @ K.T        # shape (3, 3)

# Step 2: 缩放
d_k = K.shape[-1]
scaled_scores = scores / np.sqrt(d_k)

# Step 3: Softmax
def softmax(x):
    x = x - x.max(axis=-1, keepdims=True)  # 数值稳定
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=-1, keepdims=True)

weights = softmax(scaled_scores)   # 每行和为 1

# Step 4: 加权求和
output = weights @ V                # shape (3, 4)
```

**注意力权重矩阵可视化**（每行和为 1）：

|       | 词1    | 词2    | 词3    |
| ----- | ----- | ----- | ----- |
| 词1    | 0.6   | 0.3   | 0.1   |
| 词2    | 0.2   | 0.5   | 0.3   |
| 词3    | 0.1   | 0.4   | 0.5   |

---

### Slide 14｜多头注意力：多角度并行关注

**单头的局限**：只学会一种关联（如只关注主语）。

**多头思想**：把 Q/K/V 在维度上切分成 h 份，每份独立做一次注意力，最后拼接：

```
原始 d_model = 768, num_heads = 12
每个头维度 = 768 / 12 = 64
12 个头各自从不同角度关注 → 拼接回 768 维 → 线性变换
```

| 类比         | 单头注意力             | 多头注意力                 |
| ---------- | ----------------- | --------------------- |
| 阅读         | 只关注"指代关系"         | 同时关注指代、时态、从属、修饰等     |
| 专家         | 一个专家              | h 个专家从不同视角看           |

**PyTorch 简化实现**：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.d_k = d_model // num_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, Q, K, V):
        # 切分多头 → 各自做缩放点积注意力 → 拼接 → 线性变换
        ...
```

---

### Slide 15｜前馈神经网络（FFN）

**作用**：从注意力聚合后的信息中提取更高阶特征，**逐位置**独立处理。

**结构**：两个线性变换 + ReLU 激活，"先扩大再缩小"：

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$

```python
class PositionWiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)   # 扩大：768 → 3072
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(d_ff, d_model)   # 缩小：3072 → 768

    def forward(self, x):
        return self.linear2(self.dropout(self.relu(self.linear1(x))))
```

**关键**：所有位置共享同一组权重，但独立处理——这就是"逐位置"的含义。

---

### Slide 16｜残差连接与层归一化（Add & Norm）

**每个子层都被 Add & Norm 包裹**：

$$\text{Output} = \text{LayerNorm}(x + \text{Sublayer}(x))$$

| 操作              | 解决的问题           | 原理                          |
| --------------- | --------------- | --------------------------- |
| **残差连接 (Add)**  | 深层网络梯度消失        | 梯度可绕过子层直接传播，x + Sublayer(x) |
| **层归一化 (Norm)** | 内部协变量偏移         | 对单个样本所有特征归一化到均值 0、方差 1      |

```python
# Encoder 层中的 Add & Norm
attn_output = self.self_attn(x, x, x, mask)
x = self.norm1(x + self.dropout(attn_output))   # Add & Norm

ff_output = self.feed_forward(x)
x = self.norm2(x + self.dropout(ff_output))     # Add & Norm
```

---

### Slide 17｜位置编码：让注意力知道顺序

**问题**：自注意力本身**不包含位置信息**——"agent learns" 和 "learns agent" 对它是等价的。

**解决**：为每个位置加一个固定的位置向量（正弦/余弦函数生成）：

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right), \quad PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)   # 偶数维 sin
        pe[:, 1::2] = torch.cos(position * div_term)   # 奇数维 cos
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return self.dropout(x + self.pe[:, :x.size(1)])  # 加到词嵌入上
```

**特点**：不学习，直接用公式计算；不同位置的编码唯一；相对位置可由线性组合表达。

---

### Slide 18｜Transformer 信息流动全景

```
输入嵌入 + 位置编码
       │
   ┌───┴───┐
   │ Multi-Head Attention │  ← 多角度关注全局
   └───┬───┘
       │ Add & Norm
   ┌───┴───┐
   │ Feed-Forward Network │  ← 逐位置特征提取
   └───┬───┘
       │ Add & Norm
       
   下一层 Encoder（× N）
```

**Vibe Coding 衔接**：让 CodeBuddy 解读 `MultiHeadAttention` 源码，逐行解释 Q/K/V 切分、缩放点积、掩码、拼接的过程，比自己读源码快 3 倍。

---

### Slide 19｜三种预训练架构总览

| 架构                | 代表模型     | 注意力方向 | 训练目标        | 擅长任务           |
| ----------------- | -------- | ----- | ----------- | -------------- |
| **Encoder-Only**  | BERT     | 双向    | MLM（遮盖预测）   | 理解类：分类、NER、问答  |
| **Decoder-Only**  | GPT      | 单向（因果） | CLM（预测下一个）  | 生成类：对话、写作、代码   |
| **Encoder-Decoder** | T5 / BART | 编码双向 + 解码因果 | Seq2Seq     | 翻译、摘要、文本到文本    |

```
BERT:    [我] [爱] [北] [京]      全部双向看到
GPT:     [我] → [爱] → [北] → [京]  只能看前文
T5:      Encoder 理解输入 → Decoder 生成输出
```

---

### Slide 20｜BERT：双向理解之王

**BERT (Bidirectional Encoder Representations from Transformers)**

**核心创新**：Masked Language Model (MLM)

```
原始句子：我爱北京天安门
遮盖后：  我 [MASK] 北京 [MASK] 门
任务：    预测 [MASK] = "爱" 和 "天安"
```

**为什么 MLM 比CLM 更适合理解类任务？**

| 训练目标 | 看到的上下文     | 适合任务     |
| ------ | ---------- | -------- |
| MLM    | 前后文都看到     | 分类、NER、问答 |
| CLM    | 只看前文       | 生成、对话    |

**BERT 微调下游任务**：在 [CLS] 位置的输出向量后接一个线性分类层即可。

---

### Slide 21｜GPT：自回归生成之王

**GPT (Generative Pre-trained Transformer)**

**核心思想**：语言的本质就是**预测下一个词**——抛弃编码器，只用解码器。

**Causal Language Model (CLM)**：

```
输入：[Datawhale Agent is]
预测：[a]           ← 只看 "Datawhale Agent is"
输入：[Datawhale Agent is a]
预测：[powerful]    ← 只看 "Datawhale Agent is a"
```

**掩码自注意力 (Masked Self-Attention)**：训练时一次输入完整序列，但用三角掩码阻止位置 t 看到位置 >t 的内容：

```
掩码矩阵（下三角）：
[1 0 0 0]
[1 1 0 0]
[1 1 1 0]
[1 1 1 1]
```

GPT 系列从 GPT-1 到 GPT-4，参数量从 1.17 亿增长到万亿级，但架构核心不变。

---

### Slide 22｜T5：统一的文本到文本框架

**T5 (Text-to-Text Transfer Transformer)**：把所有 NLP 任务统一为"输入文本 → 输出文本"。

| 任务     | 输入                          | 输出              |
| ------ | --------------------------- | --------------- |
| 翻译     | `translate English to French: The house is wonderful.` | `La maison est magnifique.` |
| 摘要     | `summarize: [文章内容]`          | `[摘要]`          |
| 分类     | `classify: [文本]`             | `positive`      |
| 问答     | `question: ... context: ...` | `[答案]`          |

**优势**：一个模型、一套训练方式处理所有任务。
**劣势**：参数量大、推理慢于专用架构。

---

### Slide 23｜如何选择预训练模型？

**任务-架构对应表**：

| 你的任务                | 推荐架构          | 推荐模型（中文）                       |
| ------------------- | ------------- | ------------------------------ |
| 文本分类（情感、意图）         | Encoder-Only  | bert-base-chinese / macbert    |
| 命名实体识别 (NER)        | Encoder-Only  | bert-base-chinese              |
| 问答（抽取式）             | Encoder-Only  | bert-base-chinese              |
| 文本生成（对话、续写）         | Decoder-Only  | Qwen / ChatGLM / GPT           |
| 翻译、摘要               | Encoder-Decoder | T5 / mT5 / BART                |
| 通用嵌入（语义检索）          | Encoder-Only  | bge / text2vec / sentence-bert |

**工程经验**：理解类任务首选 BERT 系列；生成类任务首选 GPT 系列；不要用 BERT 做生成，不要用 GPT 做分类。

---

### Slide 24｜预训练：在海量数据上学习"语言能力"

**预训练 (Pre-training)**：在大量无标注文本上自监督学习。

| 模型       | 预训练数据                            | 数据规模              |
| -------- | -------------------------------- | ----------------- |
| BERT     | BookCorpus + English Wikipedia   | 3.3B tokens        |
| GPT-3    | CommonCrawl + WebText2 + Books   | 570GB 文本           |
| bert-base-chinese | 中文维基百科 + 新闻 + 百科                 | 约 100MB 中文文本       |

**类比**：预训练 = "大学通识教育"，让模型掌握通用语言能力；微调 = "岗前专业培训"，针对具体任务调整。

**为什么不需要从头训练？**

| 方式       | 算力            | 数据              | 时间              |
| -------- | ------------- | --------------- | --------------- |
| 从零训练 BERT | 64 个 TPU × 4 天 | 3.3B tokens 标注  | 约 100 万美元        |
| 微调 BERT  | 1 个 GPU × 1 小时 | 几千条标注数据         | 几乎免费             |

迁移学习的价值：站在巨人肩膀上，用极少资源完成定制任务。

---

### Slide 25｜MLM vs CLM：两种预训练目标对比

**MLM（BERT 用）**：随机遮盖 15% 的 token，预测被遮盖的词

```
输入：我 [MASK] 北京 [MASK] 安 [MASK]
目标：预测 [MASK] = "爱", "天", "门"
```

**CLM（GPT 用）**：逐词预测下一个词

```
输入：我 爱 北
目标：预测下一个词 = "京"
```

| 训练目标 | 上下文        | 适合下游任务   | 代表模型   |
| ------ | ---------- | -------- | ------ |
| MLM    | 双向（前后都看）   | 理解类      | BERT   |
| CLM    | 单向（只看前文）   | 生成类      | GPT    |

**思考题预告**：为什么 BERT 选 MLM 而不是 CLM？（详见实验报告思考题 a）

---

### Slide 26｜微调范式：预训练 + 微调两阶段

**两阶段流程**：

```
阶段一：预训练（一次性，昂贵）
   海量无标注语料 → 自监督学习 → 预训练模型（通用语言能力）

阶段二：微调（每个任务一次，便宜）
   少量带标注数据 → 监督学习 → 任务专用模型（特定任务能力）
```

**BERT 微调文本分类的完整流程**：

```
1. 加载预训练 BERT
2. 在 [CLS] 输出后接线性分类头（输出 2 维 logits）
3. 用带标签数据训练（交叉熵损失 + AdamW 优化器）
4. 评估：Accuracy / F1
```

**与 sklearn 的对比**：

| 对比项         | sklearn `model.fit()`     | BERT 微调                     |
| ----------- | ------------------------ | --------------------------- |
| 训练方式        | 闭式解 / 梯度下降               | 反向传播 + 优化器                  |
| 数据预处理       | 数值化即可                    | Tokenization（input_ids 等）   |
| 调用接口        | `model.fit(X, y)`        | `outputs = model(**inputs)` |
| 学习率         | 默认即可                     | 必须很小（2e-5）                  |

---

### Slide 27｜Hugging Face 生态导览

**一站式 NLP 工具链**：

| 库                  | 作用                       |
| ------------------ | ------------------------ |
| `transformers`     | 加载/使用预训练模型、Tokenizer      |
| `datasets`         | 加载/处理数据集                 |
| `tokenizers`       | 高性能 Tokenizer（Rust 实现）   |
| `peft`             | 参数高效微调（LoRA 等）           |
| `accelerate`       | 多 GPU / 混合精度训练加速         |
| `Model Hub`        | 数万个预训练模型的中央仓库            |

**核心 API 速览**：

```python
from transformers import (
    AutoTokenizer,                        # 通用 Tokenizer 加载
    AutoModel,                            # 通用模型加载（输出隐藏状态）
    AutoModelForSequenceClassification,   # 文本分类模型（带分类头）
    BertTokenizer,                        # BERT 专用 Tokenizer
    BertForSequenceClassification,        # BERT 分类模型
    pipeline                              # 一行代码完成任务
)
```

`Auto*` 系列根据模型名自动选择对应类，推荐使用。

---

### Slide 28｜pipeline：一行代码体验预训练模型

```python
from transformers import pipeline

# 情感分析（默认英文模型）
classifier = pipeline("sentiment-analysis")
classifier("I love this hotel!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# 中文情感分析（指定中文模型）
classifier = pipeline("sentiment-analysis", model="bert-base-chinese")
classifier("这家酒店服务很好，房间干净。")
# [{'label': 'LABEL_1', 'score': 0.99}]  # 1=正面

# 命名实体识别
ner = pipeline("ner")
ner("张三在北京大学读书")
# [{'entity': 'PER', 'word': '张三'}, {'entity': 'ORG', 'word': '北京大学'}]

# 问答
qa = pipeline("question-answering")
qa(question="BERT 是什么？", context="BERT 是一个预训练语言模型...")
```

**适用场景**：快速原型验证、不要求定制时的开箱即用。

---

### Slide 29｜Tokenizer 深入：从文本到模型输入

**Tokenizer 的作用**：把文本转换为模型能处理的数字 ID 序列。

```python
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
encoding = tokenizer(
    "酒店位置很好，服务态度也不错。",
    padding="max_length",      # 填充到最大长度
    truncation=True,           # 超长截断
    max_length=32,             # 最大长度
    return_tensors="pt"        # 返回 PyTorch 张量
)

print(encoding.keys())
# dict_keys(['input_ids', 'token_type_ids', 'attention_mask'])
```

| 输出字段                | 含义                  | 形状             |
| ------------------- | ------------------- | -------------- |
| `input_ids`         | 词元对应的 ID 序列         | (1, 32)        |
| `attention_mask`    | 1=真实 token，0=padding | (1, 32)        |
| `token_type_ids`    | 句对任务中区分上下句          | (1, 32)        |

```
原文：    酒店位置很好
input_ids: [101, 6983, 2421, ..., 0, 0]   # 101=[CLS], 102=[SEP], 0=padding
attention_mask: [1, 1, 1, ..., 0, 0]      # 1=关注，0=忽略
```

---

### Slide 39｜Vibe Coding 融合②：Inline Edit 调参

**场景**：训练 Loss 不降，需要调超参数。

**旧方式**：手动改代码 → 运行 → 再改 → 再运行...

**Inline Edit 方式**：

1. 选中 `lr=2e-5` → `Cmd+K`
2. 输入："把学习率改成 5e-5，并加 warmup（前 10% 步数线性升温）"
3. 查看 Diff → Accept

```python
# 修改前
optimizer = AdamW(model.parameters(), lr=2e-5)

# 修改后（CodeBuddy 生成）
from transformers import get_linear_schedule_with_warmup
optimizer = AdamW(model.parameters(), lr=5e-5)
total_steps = len(train_loader) * 3
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=total_steps // 10,
    num_training_steps=total_steps
)
```

**斜杠指令调试**：
- `/fix` —— 训练报错时一键定位问题
- `/explain` —— 选中 `BertForSequenceClassification` 源码，逐行解释

---

### Slide 40｜全参数微调的代价

**BERT-base 的参数规模**：

| 组件              | 参数量         |
| --------------- | ----------- |
| Embedding 层     | 23M         |
| 12 层 Transformer | 85M         |
| 分类头             | 1.5K        |
| **总计**          | **约 1.1 亿** |

**全参数微调的问题**：

| 痛点          | 说明                          |
| ----------- | --------------------------- |
| 显存占用大       | 模型参数 + 梯度 + 优化器状态 ≈ 4 倍参数量  |
| 存储成本高       | 每个任务一份完整模型副本                |
| 部署困难        | 多任务需要多个大模型                  |
| 容易过拟合       | 参数多、数据少时易记忆训练集              |

**核心矛盾**：模型大才能学好，但大模型微调代价高——LoRA 等参数高效微调方法应运而生。

---

### Slide 41｜PEFT 思想：冻结主干，只调少量参数

**PEFT (Parameter-Efficient Fine-Tuning)**：冻结大部分预训练参数，只训练少量新增参数。

| 方法              | 核心思想                  | 参数量        |
| --------------- | --------------------- | ---------- |
| **LoRA**        | 权重更新 ΔW = AB（低秩分解）    | 0.1%-1%    |
| Prefix Tuning   | 在每层注意力前加可学习的前缀 token  | 1%-5%      |
| P-Tuning v2     | 类似 Prefix，但更深         | 1%-5%      |
| Adapter         | 在每层插入小型瓶颈网络           | 1%-5%      |
| Prompt Tuning   | 只优化输入端的连续 prompt       | <1%        |

**类比**：全参数微调 = 重写整本课本；PEFT = 在课本上加书签和批注，原书不动。

**为什么有效？** 预训练模型已经学到通用语言能力，下游任务只需要"轻微调整"，不需要大幅改变参数。

---

### Slide 42｜LoRA 核心原理：低秩分解

**核心假设**：微调时的权重更新 ΔW 是低秩的，可以分解为两个小矩阵的乘积：

$$W_{\text{new}} = W_{\text{pretrained}} + \Delta W = W_{\text{pretrained}} + AB$$

其中：
- $W$：原始权重矩阵，shape `(d, d)`，**冻结不动**
- $A$：shape `(d, r)`，可训练
- $B$：shape `(r, d)`，可训练
- $r$：低秩维度，通常 4-64，远小于 $d$

```
原始：d × d = 768 × 768 = 589,824 参数
LoRA：d × r + r × d = 768 × 8 + 8 × 768 = 12,288 参数（r=8）
参数量降到原来的 2%！
```

**与 PCA 的相似之处**：

| 对比项         | PCA                      | LoRA                      |
| ----------- | ------------------------ | ------------------------- |
| 目标          | 用低维空间近似高维数据              | 用低秩矩阵近似权重更新               |
| 假设          | 数据本征维度低                  | 微调变化本征维度低                 |
| 输出          | 主成分矩阵                    | A、B 两个小矩阵                 |

---

### Slide 43｜LoRA 代码实战

```python
from peft import LoraConfig, get_peft_model, TaskType

# 加载预训练模型（同任务2）
model = BertForSequenceClassification.from_pretrained(
    "bert-base-chinese", num_labels=2)

# 配置 LoRA
lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,        # 序列分类任务
    r=8,                                # 低秩维度
    lora_alpha=32,                      # 缩放系数（实际缩放 = alpha/r）
    lora_dropout=0.1,                   # LoRA 层的 dropout
    target_modules=["query", "value"]   # 对注意力的 Q 和 V 矩阵加 LoRA
)

# 用 LoRA 包装模型
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 294,912 || all params: 102,272,257 || trainable%: 0.29%
```

**关键观察**：可训练参数从 1.1 亿降到 29 万（0.29%），但效果接近全参数微调！

后续训练循环与任务2完全一样——PEFT 的优雅之处。

---

### Slide 44｜全参数 vs LoRA 对比

| 对比项                | 全参数微调        | LoRA 微调             |
| ------------------ | ------------ | ------------------- |
| 可训练参数量             | 1.1 亿 (100%) | 29 万 (0.29%)        |
| 训练显存（batch=8）      | 约 4GB        | 约 1.5GB             |
| 训练时间（3 epochs）     | 约 30 分钟      | 约 25 分钟             |
| 模型存储（每个任务）         | 400MB        | 1MB（只存 LoRA 权重）     |
| 最终 F1（hotel.csv）   | 约 0.92       | 约 0.90              |
| 多任务部署              | 每任务一份完整模型    | 共享主干 + 多个 LoRA 头    |

**结论**：
- 数据量大、追求极致精度 → 全参数微调
- 数据少、多任务、资源受限 → LoRA
- 工程实践中 LoRA 已成为默认选择

---

### Slide 45｜本讲知识地图（完整版）

```
N-gram → 神经网络语言模型 → RNN/LSTM → Transformer
                                          │
                              ┌───────────┼───────────┐
                              │           │           │
                            BERT         GPT         T5
                          (理解)        (生成)      (转换)
                              │
                   ┌──────────┴──────────┐
                   │                     │
                全参数微调              LoRA 微调
                (1.1亿参数)          (29万参数, 0.29%)
                   │                     │
              Transformers             peft 库
              Trainer / 手写循环        get_peft_model
```

**重点掌握**：
- [完成] 自注意力 Q/K/V 计算流程
- [完成] BERT 的 MLM 预训练目标
- [完成] Hugging Face 微调完整流程
- [完成] LoRA 低秩分解原理

**了解即可**：
- Transformer 完整源码实现
- T5 的文本到文本框架
- 其他 PEFT 方法（Prefix、Adapter）

---

### Slide 46｜实验五说明 + 思考题

**实验任务总览**：

| 任务                | 内容                          | 分值     |
| ----------------- | --------------------------- | ------ |
| 任务1               | NumPy 手动实现自注意力              | 35     |
| 任务2               | BERT 酒店评论情感分类微调             | 65     |
| 任务3（选做）           | LoRA 微调对比全参数微调               | +30    |

**思考题（三选一）**：

a. 为什么 BERT 使用 MLM 而不是 CLM 进行预训练？MLM 和 CLM 分别适合哪类下游任务？

b. 微调 BERT 时学习率通常设为 2e-5，远小于从零训练的值。为什么？设置过大会发生什么？

c. LoRA 的核心思想是将 ΔW 分解为低秩矩阵 AB。为什么这个假设在微调场景下合理？它和 PCA 降维有什么相似之处？

**参考资料**：
1. Hello-Agents 第三章：大语言模型基础（3.1 Transformer 架构）
2. Devlin et al. (2019). "BERT: Pre-training of Deep Bidirectional Transformers"
3. Vaswani et al. (2017). "Attention Is All You Need"
4. Hu et al. (2022). "LoRA: Low-Rank Adaptation of Large Language Models"
5. Hugging Face 文档：https://huggingface.co/docs/transformers

---

## 附录：Vibe Coding 工具线融入点速查

| 知识点             | Vibe Coding 工具           | 融入方式                       |
| --------------- | ------------------------ | -------------------------- |
| Transformer 架构  | CodeBuddy `/explain`     | 让 AI 逐行解释 MultiHeadAttention 源码 |
| Tokenizer 使用    | Inline Edit (`Cmd+K`)    | 选中代码 → 调整 max_length、padding 策略 |
| 微调训练循环          | Speckit                  | 用 Spec 描述任务 → 生成训练脚本框架     |
| 超参数调优           | CodeBuddy 对话             | "Loss 不降怎么办？过拟合怎么处理？"     |
| LoRA 配置         | Rules (`.codebuddy/rules/`) | 定义项目规范：默认 LoRA rank=8     |
| 实验调试            | 斜杠指令 `/fix`              | 训练报错时一键定位                  |
| 代码审查            | 斜杠指令 `/cr`               | 审查微调代码的潜在问题                |

## 附录：Transformers 常用 API 速查

| 操作             | 代码                                                     |
| -------------- | ------------------------------------------------------ |
| 加载 Tokenizer   | `BertTokenizer.from_pretrained("bert-base-chinese")`   |
| 加载分类模型         | `BertForSequenceClassification.from_pretrained(name, num_labels=2)` |
| 文本编码           | `tokenizer(text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")` |
| 一行推理           | `pipeline("sentiment-analysis", model="bert-base-chinese")` |
| 前向传播（含 loss）   | `outputs = model(input_ids=..., attention_mask=..., labels=...)` |
| 获取 logits      | `outputs.logits`                                       |
| 获取 loss        | `outputs.loss`                                         |
| 优化器            | `AdamW(model.parameters(), lr=2e-5)`                   |
| 学习率调度          | `get_linear_schedule_with_warmup(optimizer, warmup, total)` |
| LoRA 配置        | `LoraConfig(task_type=TaskType.SEQ_CLS, r=8, target_modules=["query","value"])` |
| LoRA 包装        | `model = get_peft_model(model, lora_config)`           |
| 查看可训练参数        | `model.print_trainable_parameters()`                   |

## 附录：关键公式速查

| 概念          | 公式                                                          |
| ----------- | ----------------------------------------------------------- |
| 自注意力        | $\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$ |
| FFN         | $\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$             |
| 残差 + 层归一化   | $\text{Output} = \text{LayerNorm}(x + \text{Sublayer}(x))$ |
| 位置编码（偶数维）   | $PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$ |
| LoRA 权重更新   | $W_{\text{new}} = W + AB$，A:(d,r), B:(r,d)                  |
| 余弦相似度       | $\cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}||\vec{b}|}$ |
