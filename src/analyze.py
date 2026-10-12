"""澳門相關中文標題：清洗 → 分詞 → 詞頻 → 簡易主題歸類 → 圖表。"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import jieba
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "macau_titles.csv"
OUT_CSV = ROOT / "data" / "processed" / "word_freq.csv"
OUT_TOPIC = ROOT / "data" / "processed" / "topic_summary.csv"
FIG_DIR = ROOT / "figures"

# 常見停用詞（精簡版，面試可講清取捨）
STOPWORDS = {
    "的", "了", "與", "和", "在", "是", "對", "及", "如何", "如何", "一個",
    "從", "到", "能", "什麼", "中", "下", "上", "為", "以", "並", "等",
    "：", ":", "—", "-", "？", "?", "／", "/", "｜", "|",
}

# 簡易關鍵詞規則 → 管理視角主題（非複雜 NLP）
TOPIC_RULES = [
    ("文旅與客流", ["旅客", "文旅", "博物館", "客流", "零售", "夜經濟"]),
    ("交通與城市", ["交通", "輕軌", "出行", "智慧城市", "無障礙"]),
    ("教育與青年", ["中學", "教育", "青年", "就業", "實習", "寫作", "征文", "微文", "孔子"]),
    ("數據與決策", ["數據", "開放數據", "圖表", "詞頻", "決策", "管理", "運營", "資源配置"]),
    ("人口與公共服務", ["人口", "公共服務", "天氣"]),
]


def load_titles(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["title"] = df["title"].astype(str).str.strip()
    df = df[df["title"].str.len() > 0].copy()
    return df


def tokenize(text: str) -> list[str]:
    tokens = []
    for w in jieba.lcut(text):
        w = w.strip()
        if len(w) < 2 or w in STOPWORDS:
            continue
        tokens.append(w)
    return tokens


def word_freq(df: pd.DataFrame, top_n: int = 25) -> pd.DataFrame:
    counter: Counter[str] = Counter()
    for title in df["title"]:
        counter.update(tokenize(title))
    rows = [{"word": w, "count": c} for w, c in counter.most_common(top_n)]
    return pd.DataFrame(rows)


def assign_topic(title: str) -> str:
    for name, keys in TOPIC_RULES:
        if any(k in title for k in keys):
            return name
    return "其他"


def plot_freq(freq: pd.DataFrame, out: Path) -> None:
    plt.rcParams["font.sans-serif"] = [
        "Noto Sans CJK JP",
        "Noto Sans CJK SC",
        "WenQuanYi Zen Hei",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(8, 5))
    plot_df = freq.sort_values("count")
    ax.barh(plot_df["word"], plot_df["count"], color="#3B82F6")
    ax.set_xlabel("出現次數")
    ax.set_title("澳門相關標題高頻詞（示意語料）")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    df = load_titles(RAW)
    df["topic"] = df["title"].map(assign_topic)

    freq = word_freq(df)
    freq.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    topic = (
        df.groupby("topic", as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("count", ascending=False)
    )
    topic.to_csv(OUT_TOPIC, index=False, encoding="utf-8-sig")

    plot_freq(freq.head(15), FIG_DIR / "word_freq.png")

    print(f"標題數: {len(df)}")
    print("主題分布:")
    print(topic.to_string(index=False))
    print(f"已寫入 {OUT_CSV} / {OUT_TOPIC} / figures/word_freq.png")


if __name__ == "__main__":
    main()
