'''
Author        Jiahui Chen 1946847867@qq.com
Date          2026-07-21 16:09:14
LastEditTime  2026-07-21 17:06:05
Description   

'''
from pathlib import Path
from typing import Optional
import pandas as pd
import logging

from .exceptions import LoadError

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {".csv", ".xlsx", ".xls", ".json"}


def load_data(
    file_path: Path,
    sheet_name: Optional[str] = None,
    encoding: str = "utf-8-sig",
) -> pd.DataFrame:

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"文件不存在: {file_path}"
        )

    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_FORMATS:
        raise ValueError(
            f"不支持的格式: {suffix}, "
            f"仅支持 {SUPPORTED_FORMATS}"
        )

    try:
        if suffix == ".csv":

            try:
                return pd.read_csv(
                    file_path,
                    encoding=encoding
                )

            except UnicodeDecodeError:
                logger.warning(
                    f"{encoding} 解码失败，降级为 gbk"
                )

                return pd.read_csv(
                    file_path,
                    encoding="gbk"
                )

        elif suffix in (".xlsx", ".xls"):

            return pd.read_excel(
                file_path,
                sheet_name=(
                    sheet_name
                    if sheet_name is not None
                    else 0
                )
            )

        elif suffix == ".json":

            return pd.read_json(file_path)

    except (FileNotFoundError, ValueError):
        raise

    except Exception as e:
        raise LoadError(
            f"加载 {file_path.name} 失败: {e}"
        ) from e
