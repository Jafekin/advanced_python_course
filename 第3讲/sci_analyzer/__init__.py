"""科研实验数据管理与分析工具"""

from .loader import load_data
from .cleaner import clean_data, remove_duplicates, detect_outliers
from .stats_engine import run_statistics
from .exceptions import DataError, LoadError, CleanError

__version__ = "0.1.0"
__all__ = [
    "load_data", "clean_data", "remove_duplicates",
    "detect_outliers", "run_statistics",
    "DataError", "LoadError", "CleanError",
]
