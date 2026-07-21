> **注意：** 本仓库包含 Anthropic 对 Claude 技能的实现。有关代理技能标准的信息，请参阅 [agentskills.io](http://agentskills.io)。

# 技能 (Skills)

技能是指令、脚本和资源的文件夹，Claude 可以动态加载这些文件夹来提高在专门任务中的性能。技能教会 Claude 如何以可重复的方式完成特定任务，无论是使用您公司的品牌准则创建文档、使用您组织的特定工作流程分析数据，还是自动化个人任务。

有关更多信息，请查看：
- [什么是技能？](https://support.claude.com/en/articles/12512176-what-are-skills)
- [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [使用代理技能为现实世界赋能](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

# 关于本仓库

本仓库包含演示 Claude 技能系统功能的技能。这些技能涵盖从创意应用（艺术、音乐、设计）到技术任务（Web 应用测试、MCP 服务器生成）再到企业工作流（通信、品牌建设等）的范围。

每项技能都自成一体，位于自己的文件夹中，包含一个 `SKILL.md` 文件，其中包含 Claude 使用的指令和元数据。浏览这些技能以获得灵感为您自己的技能创意，或了解不同的模式和方法。

本仓库中的许多技能都是开源的（Apache 2.0）。我们还在 [`skills/docx`](./skills/docx)、[`skills/pdf`](./skills/pdf)、[`skills/pptx`](./skills/pptx) 和 [`skills/xlsx`](./skills/xlsx) 子文件夹中包含了支持 [Claude 文档功能](https://www.anthropic.com/news/create-files)的文档创建和编辑技能。这些是源代码可用的，而不是开源的，但我们希望将这些与开发者共享，作为更复杂技能的参考，这些技能在生产 AI 应用中是实际使用的。

## 免责声明

**这些技能仅供演示和教育目的提供。** 虽然其中某些功能可能在 Claude 中提供，但您从 Claude 收到的实现和行为可能与这些技能中所示的不同。这些技能旨在说明模式和可能性。在依赖它们完成关键任务之前，请务必在您自己的环境中彻底测试这些技能。

# 技能集

- [./skills](./skills)：创意与设计、开发与技术、企业与通信以及文档技能的示例
- [./spec](./spec)：代理技能规范
- [./template](./template)：技能模板

# 在 Claude Code、Claude.ai 和 API 中尝试

## Claude Code

您可以通过在 Claude Code 中运行以下命令来注册此仓库作为 Claude Code 插件市场：
```
/plugin marketplace add anthropics/skills
```

然后，要安装特定的技能集：
1. 选择 `浏览并安装插件`
2. 选择 `anthropic-agent-skills`
3. 选择 `document-skills` 或 `example-skills`
4. 选择 `立即安装`

或者，通过以下方式直接安装任一插件：
```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

安装该插件后，您可以通过提及该技能来使用它。例如，如果您从市场安装了 `document-skills` 插件，您可以要求 Claude Code 执行以下操作："使用 PDF 技能从 `path/to/some-file.pdf` 提取表单字段"

## Claude.ai

这些示例技能已在 Claude.ai 中的付费计划中提供。

要使用本仓库中的任何技能或上传自定义技能，请按照 [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b) 中的说明进行操作。

## Claude API

您可以通过 Claude API 使用 Anthropic 的预构建技能并上传自定义技能。有关详细信息，请参阅 [技能 API 快速入门](https://docs.claude.com/en/api/skills-guide#creating-a-skill)。

# 创建基本技能

创建技能很简单——只需一个包含 YAML frontmatter 和说明的文件夹以及 `SKILL.md` 文件。您可以使用本仓库中的 **template-skill** 作为起点：

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

Frontmatter 只需要两个字段：
- `name` - 您的技能的唯一标识符（小写，空格用连字符表示）
- `description` - 对您的技能功能和使用时间的完整描述

下面的 Markdown 内容包含 Claude 将遵循的说明、示例和准则。有关更多详细信息，请参阅 [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)。

# 合作伙伴技能

技能是教 Claude 如何更好地使用特定软件的好方法。当我们看到来自合作伙伴的很好的技能示例时，我们可能会在这里突出其中一些：

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)
