"""簡易看板：讀取已處理結果，方便面試演示。先運行 python src/analyze.py。"""

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
FREQ = ROOT / "data" / "processed" / "word_freq.csv"
TOPIC = ROOT / "data" / "processed" / "topic_summary.csv"
FIG = ROOT / "figures" / "word_freq.png"
RAW = ROOT / "data" / "raw" / "macau_titles.csv"

st.set_page_config(page_title="澳門文本→數據", layout="wide")
st.title("澳門相關標題：文本 → 數據")
st.caption("問題：公開標題裡反覆出現什麼議題？對文旅／教育／城市管理有何提示？")

if not FREQ.exists():
    st.warning("請先在項目根目錄運行：`python src/analyze.py`")
    st.stop()

freq = pd.read_csv(FREQ)
topic = pd.read_csv(TOPIC)
raw = pd.read_csv(RAW)

c1, c2 = st.columns(2)
with c1:
    st.subheader("主題分布")
    st.bar_chart(topic.set_index("topic")["count"])
with c2:
    st.subheader("高頻詞圖")
    if FIG.exists():
        st.image(str(FIG))
    else:
        st.dataframe(freq)

st.subheader("原始標題（可替換為真實開放來源）")
st.dataframe(raw, use_container_width=True)
