# constitution.md

## 不可违反的规则

1. 所有公开函数必须有完整类型注解和 Google style docstring。
2. 函数不得修改调用者传入的 `DataFrame` 或统计结果映射。
3. 文件路径使用 `pathlib.Path`；只接受 `.md` 后缀的输出文件。
4. 不允许 bare `except`；参数错误使用 `TypeError` 或 `ValueError` 明确说明原因。
5. 不使用 `print` 作为运行日志；需要日志时使用 `logging`。
6. 数值展示统一保留 4 位小数。
7. 每个公开函数至少有正常路径、边界路径和异常路径测试。
8. 变量名使用英文 `snake_case`，解释性注释使用中文。
