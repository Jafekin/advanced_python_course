from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


def plot_results(
    df: pd.DataFrame,
    output_dir: Path = Path("output"),
) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    saved = []
    numeric_cols = df.select_dtypes(include="number").columns[:3]

    for col in numeric_cols:
        fig, ax = plt.subplots(figsize=(8, 4))
        df[col].hist(ax=ax, bins=20)
        ax.set_title(col)
        path = output_dir / f"{col}_hist.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        saved.append(path)

    return saved
