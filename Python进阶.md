## 第一讲：Python进阶基础与 Vibe Coding

本讲以"意图优先于语法"为核心理念，系统学习 Pandas 两大数据结构、可视化与 Vibe Coding 完整工具链，两条主线同步推进。

**知识线**：Pandas Series 的创建（列表/字典/常量）、索引访问（标签/位置/布尔）、统计方法（sum/mean/std/describe/value_counts）及时间序列操作（shift/rolling）；DataFrame 的创建、列行操作、条件筛选、分组聚合（groupby）、宽转长（melt）、Top N（nlargest）；CSV/Excel 多 sheet/JSON 文件读写与缺失值策略（dropna vs fillna）；Matplotlib 图表决策树（柱状图、折线图、直方图、箱线图、多子图布局、3D 散点图）；NetworkX 社交网络构建与最短路径分析。

**工具线**：两段式 Prompt（先描述氛围，再逐步加约束）；Rules 规则文件（锁定 AI 输出风格）；上下文四层级与 @文件引用（精准注入数据结构）；Inline Edit（Cmd+K）与 Diff 审查三步清单；MCP 能力扩展（模型上下文协议，连接外部数据源）；Agent Skills（可复用 SOP 封装）；自定义斜杠指令。

---

## 第二讲：机器学习基础与 Spec-driven协作建模

本讲以"工程化建模"为目标，理解机器学习的核心工作流（数据 → 特征工程 → 训练 → 评估 → 部署），并通过四个经典算法完整实践监督学习与无监督学习。

**理论基础**：AI/ML/DL 层级关系，机器学习三要素（数据/算法/算力），特征工程（提取、转换、选择、降维），监督学习 vs 无监督学习的本质区别；另简介 KNN 与逻辑回归作为背景知识。

**四个算法任务**（理论先行，再用 sklearn 实践）：

- 线性回归（监督/回归）：MSE 损失函数、梯度下降法、正规方程解、过拟合/欠拟合；评估指标 RMSE / R²
- SVM 分类（监督/分类）：最大间隔超平面、核函数（线性/多项式/RBF）、Hard/Soft Margin；混淆矩阵、精确率/召回率/F1-score，以及"准确率陷阱"
- K-means 聚类（无监督）：随机初始化 → 分配 → 更新的迭代过程，肘部法则确定最优 K，K-means++ 改进初始化
- PCA 降维（无监督）：协方差矩阵与特征值分解，主成分方向，解释方差比，标准化的必要性

**工具线升级——Spec-driven 开发范式（Speckit）**：针对多步骤建模项目，引入 GitHub 开源工具 Speckit，核心工作流为 `constitution（底线约束）→ specify（需求）→ plan（方案）→ tasks（拆解）→ implement（落地）`。课程实验采用轻量用法：手写 `speckit.md`（包含 constitution 硬约束、context 数据背景、任务列表），每次对话附带 `@speckit.md` 引用，AI 自动遵守全程约束，无需每轮重复说明。两段式 Prompt 与 Speckit 的选型原则：单任务快速验证用前者，多步骤跨对话项目用后者。

---

## 第三讲：NLP 基础与 Prompt 工程

本讲从传统 NLP 向大模型过渡，建立文本处理的完整认知框架，核心目标是系统掌握 Prompt Engineering，并完成从 Vibe Coding 工具使用者到 LLM 应用开发者的转变。

**知识线**：语言模型本质（N-gram → RNN → Transformer Decoder-Only 架构演进）；分词三策略对比（按词/按字符/子词），BPE 算法合并过程（get_vocab → get_pair_freqs → merge_vocab 迭代）；Token 对开发者的实际意义（上下文窗口、计费、Prompt 长度管理），tiktoken 实操计算 Token 数；采样参数原理与调参策略（Temperature 控制随机性、Top-k 截断词表、Top-p 核采样，三者关系与组合推荐）；Prompt Engineering 全景（Zero-shot / One-shot / Few-shot 梯度递进、角色扮演 System Prompt、思维链 CoT、结构化 JSON 输出）；OpenAI 兼容 API 工程实践（messages 结构、流式输出、错误处理）；主流模型选型（闭源 vs 开源、参数量/上下文/成本权衡，2026 年模型全景表）；缩放法则（Scaling Laws：参数量、数据量、算力的幂律关系）与模型幻觉（事实性幻觉 vs 推理性幻觉，缓解策略：Few-shot 定锚、CoT 自验证、RAG 知识注入）。

---

## 第四讲：NLP 进阶与模型微调

本讲承接第3讲（已能调用大模型），深入"模型内部"，理解 Transformer 架构与预训练-微调范式，亲手微调一个真实 BERT 模型，完成从"黑盒调用"到"白盒定制"的跨越。

**知识线**：语言模型演进（N-gram 局限 → 词嵌入与语义空间 → RNN/LSTM 瓶颈 → Transformer 革命）；自注意力机制（Q/K/V 三角色、缩放点积公式、多头并行关注、前馈网络 FFN、残差连接与层归一化、位置编码）；三种预训练架构对比（Encoder-Only BERT 双向理解 / Decoder-Only GPT 自回归生成 / Encoder-Decoder T5 文本到文本）；预训练目标 MLM vs CLM 的设计逻辑与适用任务；Hugging Face 生态（transformers / tokenizers / datasets / peft 库，AutoTokenizer / AutoModel / pipeline 核心 API）；BERT 情感分类微调实战（hotel.csv 数据集，load_data → CommentDataset → train_model → 评估完整流程，input_ids / attention_mask / token_type_ids 编码原理）；关键超参数解读（lr=2e-5 / batch_size / epochs / warmup / weight_decay）与 Loss 曲线诊断（欠拟合 / 过拟合 / 梯度爆炸）；LoRA 参数高效微调（全参数微调代价 → PEFT 思想 → 低秩分解 ΔW=AB → 与 PCA 降维的类比 → peft 库 LoraConfig 实战）。

---

## 第五讲：大模型部署与检索生成增强（RAG）

本讲解决两个工程问题：模型如何变成可调用服务（部署），模型知识过期会幻觉如何基于真实文档回答（RAG）。

**知识线**：部署全景（权重→推理引擎→OpenAI 兼容 HTTP API）；方案选型（Ollama 个人/原型、vLLM 生产高并发、llama.cpp 纯 CPU、TGI/LM Studio）；量化原理（FP16→INT8→INT4 显存-精度三角，7B 模型 14GB→4GB，GGUF 格式与 K-Quants Q4_K_M 推荐，PTQ vs QAT）；vLLM 深入（PagedAttention 类比 OS 分页管理 KV Cache 显存利用率 30%→95%，Continuous Batching 动态拼批吞吐 2-10 倍，实测 Batch=16 时 2.4 倍于 Ollama）；RAG 三段式（Retrieve→Enhance→Generate）与三种方案对比（传统检索/纯 LLM/RAG），两阶段工作流（离线建库一次、在线查询每次），三代演进（Naive 关键词→Advanced 语义→Modular 混合），vs 微调选型；RAG 流水线六环节从零实现（不依赖 LangChain）：markitdown 文档加载、递归字符分块三策略与 chunk_size 调参、sentence-transformers 句子嵌入与模型选型（all-MiniLM-L6-v2 / bge-large-zh / bge-m3）、ChromaDB 五要素、语义检索、防幻觉 Prompt 与引用标注；高级检索三策略（MQE 多查询扩展、HyDE 假设文档嵌入、Reranker Cross-Encoder 重排序）与评估指标（Recall@k / Precision@k / MRR）；Agent 记忆系统概览（四类型：工作/情景/语义/感知；五操作：编码/存储/检索/整合/遗忘；Memory 检索内部交互 vs RAG 检索外部知识，衔接第6讲）。

---

## 第六讲：Agent 系统开发

本讲整合前五讲所学，在第五讲 RAG 基础上引入 Agent 能力，以 Vibe Coding 工作流开发一个完整 AI 应用，作为课程最终交付物。

**知识线**：从 RAG 到 Agent 的演进（RAG 只能"检索+回答"，Agent 能"思考+行动"）；Agent 核心能力——工具调用（Tool Use：Function Calling 协议、工具定义与描述、模型决策调用）、多轮对话状态管理（消息历史维护、上下文窗口控制、记忆摘要）、任务拆解与执行链（ReAct 推理-行动循环、Plan-and-Execute、多步任务编排）；多 Agent 协作简介（角色分工、消息传递）；典型应用形态：智能知识库问答 Agent（RAG + 工具调用），或能自主调用外部 API 完成复合任务的 Agent（如查天气、查数据库、发邮件）。
