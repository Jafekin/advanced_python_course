# Python 进阶课程总纲

> 更新日期：2026-07-21
> 课程：Python 进阶（计算机学院）
> 教师：
> 平台：CloudStudio + CodeBuddy
> 课时：8讲理论 + 8次实验（每周五上午理论、下午实验）
> 评分：8次实验成绩，无大作业；第8讲实验为NLP完整应用开发

## 双线融合设计

| 讲次 | 核心问题 | Python 主线 | AI 协作主线 |
|------|---------|------------|------------|
| 第1讲 | 如何借助AI快速完成数据处理？ | Pandas 数据读取、清洗、转换、聚合 | Vibe Coding 提示、迭代生成、代码纠错 |
| 第2讲 | 如何把数据转化为可信的视觉表达？ | Matplotlib、Seaborn 高阶可视化 | 图表方案生成、视觉审查、结论修正 | 
| 第3讲 | 如何将AI生成的原型变成可靠工程？ | 模块化、类型注解、异常处理、测试 | Spec 定义、任务分解、约束实现 | 
| 第4讲 | 如何系统掌握与大模型对话的技术？ | NLP 基础、分词、采样参数、API 调用 | Prompt Engineering 全景 | 
| 第5讲 | 如何深入模型内部并定制它？ | Transformer、预训练、BERT 微调、LoRA | AI 辅助微调代码编写 |
| 第6讲 | 如何让模型基于真实文档回答？ | 大模型部署、RAG 流水线从零实现 | Spec-driven 部署规约 |
| 第7讲 | 如何让检索更准、让Agent有记忆？ | 高级检索策略、RAG 评估、记忆系统 | Prompt 调优、上下文工程 |
| 第8讲 | 如何让模型自主思考并执行行动？ | Agent 工具调用、ReAct、多Agent协作 | Agent Skills、MCP、全工具链总结 | 

---

## 第一讲：Python 数据处理与 Vibe Coding

本讲以"意图优先于语法"为核心理念，系统学习 Pandas 数据处理全流程（读取→清洗→转换→统计），同步建立 Vibe Coding 基础工作方式。

**知识线**：Pandas Series 的创建（列表/字典/常量）、索引访问（标签/位置/布尔）、统计方法（sum/mean/std/describe/value_counts）及时间序列操作（shift/rolling）；DataFrame 的创建、列行操作、条件筛选、分组聚合（groupby）、宽转长（melt）、Top N（nlargest）；CSV/Excel 多 sheet/JSON 文件读写与缺失值策略（dropna vs fillna）；数据清洗完整流程（重复值检测、异常值识别 IQR/Z-score、数据类型转换）；描述性统计与相关性分析。

**工具线**：两段式 Prompt（先描述氛围，再逐步加约束）；Rules 规则文件（锁定 AI 输出风格）；上下文四层级与 @文件引用（精准注入数据结构）；Inline Edit（Cmd+K）与 Diff 审查三步清单。每个知识点后紧跟 AI 协作课堂练习。

---

## 第二讲：数据高阶可视化与 AI 辅助表达

本讲聚焦将数据转化为可信的视觉表达，从 Matplotlib 进阶到 Seaborn，重点覆盖科研论文中常用的图表类型与发表级排版技巧。

**知识线**：Matplotlib 图表决策树（分布/对比/关系/趋势/分组）、多子图布局、图表美化系统化（颜色/字体/dpi/图例）；Seaborn 高阶可视化（热力图 heatmap、小提琴图 violinplot、Pairplot 多变量全景、Jointplot 联合分布、FacetGrid 分面图）；科研论文图表（误差棒图 errorbar、置信区间 fill_between、双轴图 twinx、统计标注/显著性星号、发表级排版 Nature/Science 风格参数）；配色方案选择（色盲友好、期刊推荐）。

**工具线**：AI 作为设计顾问——图表方案推荐、视觉审查与改进建议、Publication-ready 代码生成；三轮 Prompt 迭代（粗图→约束→发表级）；Inline Edit 调参。

---

## 第三讲：Spec-driven 协作建模与 Python 工程化

本讲解决"AI生成的代码能跑但不可靠"的问题：将前两讲的一次性分析脚本，用 Python 工程化方法和 Spec-driven AI 协作模式，改造为实际可用的软件系统。

**知识线**：模块化组织（包结构、`__init__.py`、相对/绝对导入）；类型注解（typing 模块、函数签名标注）；异常处理（try/except 层级、自定义异常、上下文管理器）；测试（pytest 断言/fixture/参数化、测试驱动开发）；代码质量工具（ruff、pre-commit）。

**工具线**：Spec-driven 开发范式——Speckit 工作流（constitution → specify → plan → tasks → implement）；speckit.md 编写实战（硬约束、环境上下文、任务列表）；与两段式 Prompt 的选型原则（单任务用后者，多步骤工程用前者）。贯穿案例：将数据分析原型工程化为「科研实验数据管理与分析工具」。

---

## 第四讲：NLP 基础与 Prompt 工程

本讲从传统 NLP 向大模型过渡，建立文本处理的完整认知框架，核心目标是系统掌握 Prompt Engineering，并完成从 Vibe Coding 工具使用者到 LLM 应用开发者的转变。

**知识线**：语言模型本质（N-gram → RNN → Transformer Decoder-Only 架构演进）；分词三策略对比（按词/按字符/子词），BPE 算法合并过程（get_vocab → get_pair_freqs → merge_vocab 迭代）；Token 对开发者的实际意义（上下文窗口、计费、Prompt 长度管理），tiktoken 实操计算 Token 数；采样参数原理与调参策略（Temperature 控制随机性、Top-k 截断词表、Top-p 核采样，三者关系与组合推荐）；Prompt Engineering 全景（Zero-shot / One-shot / Few-shot 梯度递进、角色扮演 System Prompt、思维链 CoT、结构化 JSON 输出）；OpenAI 兼容 API 工程实践（messages 结构、流式输出、错误处理）；主流模型选型（闭源 vs 开源、参数量/上下文/成本权衡）；缩放法则（Scaling Laws）与模型幻觉（事实性幻觉 vs 推理性幻觉，缓解策略）。

---

## 第五讲：NLP 进阶与模型微调

本讲承接第4讲（已能调用大模型），深入"模型内部"，理解 Transformer 架构与预训练-微调范式，亲手微调一个真实 BERT 模型，完成从"黑盒调用"到"白盒定制"的跨越。

**知识线**：语言模型演进（N-gram 局限 → 词嵌入与语义空间 → RNN/LSTM 瓶颈 → Transformer 革命）；自注意力机制（Q/K/V 三角色、缩放点积公式、多头并行关注、前馈网络 FFN、残差连接与层归一化、位置编码）；三种预训练架构对比（Encoder-Only BERT 双向理解 / Decoder-Only GPT 自回归生成 / Encoder-Decoder T5 文本到文本）；预训练目标 MLM vs CLM 的设计逻辑与适用任务；Hugging Face 生态（transformers / tokenizers / datasets / peft 库）；BERT 情感分类微调实战（完整训练流程）；关键超参数解读与 Loss 曲线诊断；LoRA 参数高效微调（低秩分解 ΔW=AB、peft 库 LoraConfig 实战）。

---

## 第六讲：大模型部署与检索增强生成基础

本讲解决两个工程问题：模型如何变成可调用服务（部署），模型知识过期会幻觉时如何基于真实文档回答（RAG）。

**知识线**：部署全景（权重→推理引擎→OpenAI 兼容 HTTP API）；方案选型（Ollama 个人/原型、vLLM 生产高并发、llama.cpp 纯 CPU）；量化原理（FP16→INT8→INT4 显存-精度三角，GGUF 格式与 K-Quants Q4_K_M 推荐，PTQ vs QAT）；vLLM 深入（PagedAttention 类比 OS 分页、Continuous Batching 动态拼批）；RAG 三段式（Retrieve→Enhance→Generate）与三种方案对比，两阶段工作流（离线建库、在线查询），三代演进（Naive→Advanced→Modular），vs 微调选型；RAG 流水线六环节从零实现（不依赖 LangChain）：markitdown 文档加载、递归字符分块、sentence-transformers 句子嵌入、ChromaDB 向量库、语义检索、防幻觉 Prompt。

---

## 第七讲：检索增强生成进阶

本讲在第六讲基础RAG之上，解决"检索不准"和"Agent无记忆"两个进阶问题，引入高级检索策略、系统化评估方法和Agent记忆系统实现。

**知识线**：高级检索三策略（MQE 多查询扩展——LLM改写等价查询并行检索、HyDE 假设文档嵌入——用假设答案向量检索、Reranker Cross-Encoder 重排序）；混合检索（稀疏BM25 + 稠密向量，RRF 融合）；RAG 评估指标（Recall@k / Precision@k / MRR）与端到端评估；调参实践（chunk_size/overlap/top_k/嵌入模型选型）；生产化考量（增量更新、缓存、错误处理）；Agent 记忆系统四类型（工作记忆/情景记忆/语义记忆/感知记忆）与五操作（编码/存储/检索/整合/遗忘）；Memory 与 RAG 的关系（内部交互 vs 外部知识）；简化记忆系统实现（JSON + sentence-transformers）。

---

## 第八讲：Agent 系统开发

本讲整合前七讲所学，在 RAG 基础上引入 Agent 能力，以 Vibe Coding 工作流开发一个完整 AI 应用，作为课程最终交付物。

**知识线**：从 RAG 到 Agent 的演进（RAG 只能"检索+回答"，Agent 能"思考+行动"）；Agent 核心能力——工具调用（Tool Use：Function Calling 协议、工具定义与描述、模型决策调用）、多轮对话状态管理（消息历史维护、上下文窗口控制、记忆摘要）、任务拆解与执行链（ReAct 推理-行动循环、Plan-and-Execute、多步任务编排）；多 Agent 协作（角色分工、消息传递）；通信协议（MCP/A2A/ANP）；Skill 写法实战；八讲 Vibe Coding 工具链完整回顾与总结。

**最终实验**：综合 NLP 应用开发——整合数据处理、可视化、工程化结构、Prompt 设计、RAG 检索、Agent 工具调用，构建一个有 Gradio 交互界面的智能问答系统。


## 项目结构

- `第1讲` 到 `第8讲`：按课程讲次组织的教学资料
- 章节目录下包含课件、案例、练习和参考资料
- 根目录下保留仓库说明和课程总览文档

## 内容说明

- 课件文件
- 示例代码
- 练习与参考答案
- 课程补充资料

## 使用方式

直接在本地打开对应目录查看和编辑文件，按主题分类管理即可。

## 在单台课程服务器上从 GitHub 拉取指定讲次

每讲使用独立服务器时，将 `scripts/pull_lesson_from_github.sh` 上传到对应服务器并在**服务器上**运行。脚本会要求输入数字 `1`–`8`；首次运行时从 GitHub 对本仓库做稀疏 clone，之后只会保留并更新所选讲次。默认下载目录为服务器的 `/workspace`。

```bash
# 在本机将脚本上传到某台课程服务器（以第 3 讲服务器为例）
scp scripts/pull_lesson_from_github.sh ubuntu@YOUR_SERVER:/opt/course-tools/

# 登录该服务器后，交互选择讲次
ssh ubuntu@YOUR_SERVER
bash /opt/course-tools/pull_lesson_from_github.sh
```

也可在服务器上指定讲次和仓库保存位置：

```bash
# 第一次下载或后续更新第 3 讲
bash /opt/course-tools/pull_lesson_from_github.sh --lesson 3

# 查看全部可选讲次
bash /opt/course-tools/pull_lesson_from_github.sh --list
```

脚本会把 Git 缓存放在 `$HOME/.cache/advanced_python_course`，不会读取、更不会修改 CloudStudio 等环境中 `/workspace` 已有仓库的 `origin`。讲次文件默认同步到 `/workspace/第X讲`；`assets`、`scripts`、`.gitattributes`、`.gitignore`、`LICENSE`、`README.md` 等仓库根目录内容均不会同步到 `/workspace`。脚本默认从 `https://github.com/Jafekin/advanced_python_course.git` 的 `main` 分支拉取，并使用 `git pull --ff-only origin main` 更新。因此服务器需要能够访问 GitHub，且安装 Git 2.25 或更高版本。更新时脚本使用系统自带的 `tar` 创建完整暂存副本后再替换所选的 `/workspace/第X讲`，因此不依赖 `rsync`；它只清理所选讲次目录内已不再存在的文件，不会触碰 `/workspace` 中的其他内容。
