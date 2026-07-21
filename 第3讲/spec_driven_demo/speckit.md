# speckit.md — Reporter 模块当前任务

请先阅读并遵守：

- @constitution.md
- @context.md
- @tasks.md

## 本轮交付

实现 `sci_analyzer/reporter.py` 中的 `generate_report`。

## 执行顺序（不要跳步）

1. 先给出不超过 8 行的实现计划：参数校验、内容组装、文件写入、测试对应关系。
2. 确认接口不变后，再实现函数。
3. 运行 `python -m pytest spec_driven_demo/tests/test_reporter.py -q`。
4. 若失败，报告失败的测试名、根因和最小修改方案；不要靠删除测试或放宽断言通过。

## 交付前自检

- 类型注解和 Google style docstring 是否完整？
- 是否只读取 `df`，没有原地修改？
- 是否拒绝非 `.md` 输出路径？
- 是否创建了缺失的父目录？
- 是否没有使用 `print` 和 bare `except`？
