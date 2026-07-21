"""自定义异常层级"""


class DataError(Exception):
    """数据处理相关错误基类"""
    pass


class LoadError(DataError):
    """数据加载失败"""
    pass


class CleanError(DataError):
    """数据清洗失败"""
    def __init__(self, column: str, reason: str):
        self.column = column
        super().__init__(f"列'{column}'清洗失败: {reason}")
