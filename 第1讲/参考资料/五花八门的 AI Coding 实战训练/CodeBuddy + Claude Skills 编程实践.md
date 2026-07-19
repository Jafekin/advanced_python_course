# Skills 概要介绍

---

## 🎯 什么是 Skills？

**Skills** 是近期 Anthropic 发布的一个新特性 — **Claude Skills**，它的目标是让 Claude 不再只是一个「能聊天的模型」，而是一个具备可扩展、可执行技能体系的代理式 **Agentic AI 工具**。

**CodeBuddy** 也是国内首家支持 Skill 的产品。

---

## 💡 一句话概括 Skills 的作用

在规约编程中，开发者可以通过 `rules` 约束大模型输出，通过 `MCP` 调用外部工具，接入知识库输入私域知识。

现在通过 **Skills**，即可更加便捷地为大模型武装类似上述的特定技能，更加高效地解决问题。

---

## 🏗️ Skills 设计逻辑与特点

### 🔧 设计逻辑

**Skills** 是一个文件夹合集，用户可以通过在 Skills 中编写指令、脚本、YML等文件，为AI Coding 工具添加工具、方法、流程等扩展技能。

如图中 `pptx`、`pdf` 等属于 Skills 内置封装好的特性；同时也支持用户制作自定义特性。

<img src='images/image1.png' width=600px>

---

### ✨ 特点

**Skills** 通过模块化、可组合的能力封装，具备以下核心特性：

| 特性 | 描述 |

|------|------|

| ○ **模块化设计** | 每个技能都是独立的文件夹，包含完整的指令、脚本和资源，如文档技能 |

| ○ **动态加载** | AI Agent 可根据任务需求按需加载相应技能 |

| ○ **专业化能力** | 每个技能专注于特定领域，提供深度的专业知识和操作能力 |

| ○ **人性化交互** | 模拟人类专业技能的学习和应用方式 |

| ○ **可扩展性** | 支持自定义技能开发，满足个性化和企业级需求 |

---

## 📂 组成拆解

一个完整的 **Skills** 就是一个标准化的文件夹体系，每个技能由若干文件组成，用来描述功能、脚本和引用资料：

```
my-skill/

├── SKILL.md (必需)

│ ├── YAML 前置元数据 (必需)

│ │ ├── name: (必需)

│ │ └── description: (必需)

│ └── Markdown 指令 (必需)

└── 捆绑资源 (可选)

├── scripts/ - 可执行代码 (Python/Bash等)

├── references/ - 参考文档

└── assets/ - 输出文件 (模板、图标、字体等)
```

**当然我们还可以进行封装引用的：**

- **Tools**（工具）

- **Knowledge**（知识库）

- **Forms**（表单）

---

## 📄 SKILL.md 核心文件

其中 **SKILL.md** 文件是最核心的文件，必须以 **YAML Frontmatter** 元数据开头，其中包含文件名和描述，该描述会在启动时加载到系统提示符中。

如下为 **PDF** 特性的例子：

<img src='images/image (5).png' width=600px>

看起来像普通的 Prompt 文件，但它的结构和加载机制不一样。**Skills** 不是简单的「指令封装」，而是一个具备分层调用逻辑的知识模块体系。

如图为 **PDF** 在 AI 应用的技能，基于该技能进行拆解和封装，包括定义 **Skill.md** 以及相关的脚本和代码解决相关的问题。

<img src='images/image (6).png' width=600px>

---

## 🚀 技能进阶与动态加载

随着技能的提升，我们可以捆绑额外的内容，AI 会在需要时加载这些内容，以 **PDF** 技能 **Skill.md** 为例，这里捆绑了多个资源：

<img src='images/image3.png' width=600px>

在进行处理 **PDF** 技能中，针对不同的任务目标，AI 提供有不同的工作流和解决办法。

比如下图中 **AI** 按照用户提出的 **fillout pdf** 的需求自主选择对应的脚本进行操作。

<img src='images/image4.png' width=600px>

# 🚀 基于Codebuddy的Skills实操体验（一）

---

## 📋 1. 环境准备

### 1.1 🔧 安装 Git（本环境无需安装）

📖 进入 https://git-scm.com/install/ 查询对应的安装方式。

附上 **Ubuntu** 环境安装命令如下，在 **CloudStudio** 中的终端直接运行即可：

```bash
apt-get install git
```

---

### 1.2 📦 安装 Node.js（本环境无需安装）

```bash
# 如未安装，可通过下面指令安装

# 如已经安装请忽略，未安装可进行安装

https://nodejs.org/en/download/
```

---

### 1.3 🛠️ 安装 CodeBuddy Code/Plugin（本环境默认自带CodeBuddy Code与Plugin）

🔗 具体安装方式通过：

- **国外版**: [codebuddy.ai](https://codebuddy.ai)

- **国内版**: [copilot.tencent.com](https://copilot.tencent.com)

---

## ⚙️ 2. 配置第一个Skill实例

> 💡 **提示**：本环境已 git clone，将Skills安装在了 `-/.codebuddy/skills` 目录下

```bash
# 在项目中配置并进入skills目录，随后克隆Skills仓库到本环境中

git clone https://github.com/anthropics/skills.git



# 如你在使用 CodeBuddy Code或IDE，也可以用同样的方式配置 skill。
```

---

## 🔍 3. 检测Skill是否生成

在 **CodeBuddy插件对话框** 中输入以下命令进行检测是否生效：

```bash
list codebuddy/skills
```

<img src='images/listskill.png' width=600px>

---

## 🚀 4. 执行 Prompt

进行技能应用，在 **CodeBuddy对话框** 中直接使用输入以下 Prompt：

```
使用 webapp-testing skill 帮我进行针对 https://codebuddy.ai 官网做下 web 应用测试
```

> ✨ **体验感受**：不得不说体感非常丝滑了！不仅自动安装了 **Playwright**，还自动执行了 **webapp-testing** 的测试。

<img src='images/webapp test.png' width=600px>

---

## 📊 5. 得到结果

<img src='images/webapptestresult.png' width=600px>

# 🛠️ 自定义Skill

---

## 📚 第一步、了解 Skill 结构

每个 Skill 包含以下结构：

```
my-skill/

├── SKILL.md (必需)

│ ├── YAML 前置元数据 (必需)

│ │ ├── name: (必需)

│ │ └── description: (必需)

│ └── Markdown 指令 (必需)

└── 捆绑资源 (可选)

├── scripts/ - 可执行代码 (Python/Bash等)

├── references/ - 参考文档

└── assets/ - 输出文件 (模板、图标、字体等)
```

---

### 🔍 查看模板Skill命令

```bash
cat /workspace/-/.codebuddy/skills/template-skill/SKILL.md
```

<img src='images/selfskill.png' width=600px>

---

## 🚀 第二步、创建您的第一个Skill

> 💡 **以下教程为过程举例，各位同学可以按照同样的方法去封装其他的skill**

在 skills 目录下创建新的 skill，如：`newskillcr`

```bash
cd /workspace/-/.codebuddy/skills

mkdir newskillcr

cd newskillcr
```

<img src='images/mkdir.png' width=600px>

---

## 📝 第三步、创建 SKILL.md 文件

使用 CodeBuddy 创建一个代码审查 Skill 实例，在项目中查找并阅读该文件内容：

**[📋 查看代码审查Skill](/workspace/-/.codebuddy/skills/newskillcr/SKILL.md)**

<img src='images/skillcrmd.png' width=600px>

---

## ✅ 第四步、检查自定义 Skills 是否生效

由于 `Skill.md` 中的 `skill name` 为 `code-review-skill`，使用以下命令进行检测是否生效：

```bash
list newskillcr
```

<img src='images/listcr.png' width=600px>

---

## 🎯 第五步、使用Skill

用户可通过输入如下示例指令调用 Skill：

```bash
采用 code-review-skills 帮我针对 examples 目录代码进行代码评审
```

<img src='images/crr1.png' width=600px>

<img src='images/crr2.png' width=600px>

# 🎯 Skills 九大使用技巧

---

## 1️⃣ 模块化任务分解

**边界清晰，职责单一，一个 Skill 专注一件事**

### 📋 核心原则：

> 将复杂任务拆分成多个独立的 Skill，每个 Skill 只负责一个明确的功能

> 避免创建"万能 Skill"，保持单一职责原则，方便维护和组合使用，灵活应对不同场景

### 📝 示例：

| ❌ **不好** | ✅ **好的** |

|-----------|-----------|

| 创建一个 "web-development" Skill 处理所有前端任务 | 分别创建 "react-component-builder"、"api-integration"、"ui-styling" 等专项 Skill |

---

## 2️⃣ 提供清晰的触发条件

**让 AI 知道何时使用**

### 📋 核心原则：

> 在 description 中清晰描述技能的适用场景、结合精确关键词和语义理解，通过触发条件激活相关 Skill，避免误触发

> 使用"当用户提到 X 时"、"适用于 Y 场景"等明确表述

### 📝 示例：

```markdown
## 触发条件

- 用户提到"小红书"、"发布笔记"

- 需要生成符合小红书风格的内容

- 涉及小红书 API 调用或数据处理
```

---

## 3️⃣ 热数据前置

**高频信息优先加载**

### 📋 核心原则：

> 识别 80% 场景下会用到的"热数据"，放在核心指令层

> 20% 的边缘场景数据作为"冷数据"，外部存储

### 📝 示例：

| 🔥 **热数据(核心指令层)** | ❄️ **冷数据(外部引用)** |

|------------------------|------------------------|

| **最常用的 3 个 API**<br><br>```python<br># 1. 发布笔记(使用率 85%)<br>create_note(title, content, images)<br><br># 2. 上传图片(使用率 80%)<br>upload_image(file_path)<br><br># 3. 获取笔记状态(使用率 60%)<br>get_note_status(note_id)<br>``` | - 完整 API 列表(50+ 接口) → 存储在 `api_reference.md`<br>- 历史版本兼容性 → 存储在 `CHANGELOG.md`<br>- 高级配置参数 → 使用时通过 `read_file` 工具获取 |

---

## 4️⃣ 参考官方 Skill 模版案例

**示例代码分级，借助 AI 快速生成**

### 📋 核心原则：

> 参考官方模版，在 Skill 中提供完整的代码示例和配置模板，核心层只提供 1-2 个最简示例（< 10 行代码）<br>完整教程、高级用法作为外部资源引用

### 📝 示例：

#### 🎯 **快速开始(核心层)**

```python
# 30 秒上手

from xhs import Client

client = Client(api_key="your_key")

client.create_note("标题", "内容", ["image.jpg"])
```

#### 📚 **完整教程(外部资源)**

- 高级配置 → `examples/advanced_usage.py`

- 批量操作 → `examples/batch_processing.py`

- 最佳实践 → `docs/best_practices.md`

> 💡 **提示**：AI 会根据用户需求自动读取相应文件

---

## 5️⃣ 三层信息架构

**渐进式披露内容**

### 📋 核心原则：

> 将 Skill 内容分为三层：元数据(Meta)、核心指令(Instruction)、参考资源(Reference)<br>只在需要时逐层加载，避免一次性塞入所有信息

### 📝 示例：

#### 📋 **元数据层** (≤200 tokens, 始终加载)

```yaml
触发词: 小红书、RED、发布笔记

适用场景: 内容发布、数据分析

依赖: Python 3.8+, requests
```

---

#### 🎯 **核心指令层** (触发时加载)

```markdown
### 基础发布流程

1. 认证 → 2. 上传图片 → 3. 创建笔记



### 关键 API

- `create_note(title, content, images)`

- `upload_image(file_path)`
```

---

#### 📚 **参考资源层** (按需加载)

- 完整 API 文档 → 使用 `web_fetch` 工具获取

- 错误码对照表 → 遇到错误时查询

- 高级配置示例 → 用户明确需要时提供

---

## 6️⃣ 组合优先

**设计可被调用的 Skill**

### 📋 核心原则：

> Skill 应该像"乐高积木"，可以被自由组合和复用<br>通过参数传递配置，而不是写死在代码中<br>提供稳定的接口(合约)，确保向后兼容

### 📝 示例：

#### 🏢 **Brand Content Generator** (正确示范)

```markdown
## 触发条件

- 用户提到"生成品牌内容"、"营销文案"

- 其他 Skill 调用本 Skill 的内容生成能力



## 接口定义(合约)
```

**📥 输入参数**

```typescript
interface BrandConfig {

// 必填参数

companyName: string; // 公司名称

topic: string; // 内容主题

// 可选参数(有默认值)

brandColor?: string; // 品牌色,默认 #000000

slogan?: string; // 品牌口号,默认为空

targetAudience?: string; // 目标用户,默认"大众"

contentStyle?: string; // 内容风格,默认"专业"

platform?: string; // 发布平台,默认"小红书"

}
```

**📤 输出格式**

```typescript
interface GeneratedContent {

title: string; // 标题

content: string; // 正文

hashtags: string[]; // 话题标签

style: object; // 样式配置

metadata: object; // 元数据

}
```

#### 🚀 **使用示例**

```python
result = generate_brand_content({

"companyName": "腾讯科技",

"topic": "AI 编程助手发布",

"brandColor": "#006EFF",

"slogan": "用户为本,科技向善",

"targetAudience": "开发者",

"contentStyle": "科技感"

})
```

---

## 7️⃣ 识别何时应该创建 Skill

**四大黄金信号**

### 📋 核心原则：

> **使用频率 × 任务复杂度 × 团队规模 = Skill 价值**

| 🎯 **黄金信号** | 📝 **描述** |

|----------------|-------------|

| • 同一任务频繁执行 | 重复性工作自动化 |

| • Prompt 较长（超过 2000 字） | 复杂指令封装 |

| • 团队协作、知识共享 | 标准化流程 |

| • 任务包含脚本执行或模板生成 | 代码工具化 |

> ⚠️ **注意**：一次性小任务，不建议使用

### 📝 示例：

#### 📊 **数据报表生成场景**

**🔢 频率**：每天 1 次，每周 5 次

**🔄 重复内容**：

1. 从数据库提取昨日数据

2. 计算 10+ 个指标(DAU、留存率、转化率...)

3. 生成 Excel 报表

4. 发送邮件给管理层

5. 上传到共享文件夹

**⌨️ 每次手动输入**：

```
"帮我生成昨日数据报表,需要包括:

- DAU、MAU、留存率

- 新增用户、活跃用户

- 转化漏斗各环节数据

- 同比、环比分析

- 生成 Excel 格式

- 发送给 boss@company.com..."
```

*(每次输入 200+ 字，耗时 2 分钟)*

---

## 8️⃣ 动态上下文管理

**用完即释放**

### 📋 核心原则：

> Skill 执行完任务后，主动提示 AI 释放详细文档<br>使用"会话状态标记"避免重复加载

### 📝 示例：

#### 🔄 **上下文管理策略**

| 📋 **任务开始** | 📋 **任务完成** |

|----------------|----------------|

| 1. 加载核心指令层<br>2. 根据用户需求按需加载参考资源 | 3. 提示 AI: "详细文档已使用完毕，可释放上下文"<br>4. 保留元数据层，以便后续快速重新激活 |

#### 🚀 **多轮对话优化**

- 使用 `.skill_cache.json` 记录已加载的资源

- 避免同一会话中重复加载相同文档

---

## 9️⃣ Skill 的测试与版本管理

**像对待代码一样对待 Prompt**

### 📋 核心原则：

> **Prompt = Code**，必须可测试、可回滚<br>Skill 是软件工程资产，不是一次性文档<br>必须有测试用例验证行为<br>必须有版本控制支持回滚

### 📝 示例：

#### 📋 **1. 明确的契约**

- **输入**: `source_path`, `output_format`, `include_examples`

- **输出**: 成功/失败的标准 JSON 格式

- **错误码**: `PARSE_ERROR`, `UNSUPPORTED_FRAMEWORK`

#### 🧪 **2. 完整的测试** (87% 覆盖率)

| 📝 **测试类型** | 🎯 **测试内容** |

|----------------|----------------|

| 单元测试 | 路由解析、请求体解析、错误处理 |

| 集成测试 | 多文件项目、认证识别 |

| E2E 测试 | 真实 50+ 端点项目 |

#### 📚 **3. 版本控制**

- 遵循语义化版本管理

- `v1.0.0`: 稳定版

- `v0.9.0-beta`: 实验版，基础功能

- 清晰的升级路径和迁移指南

---# 开放作业

完全开放练习，用户可基于前几章的教学自由发挥，打造自己的skil吧
