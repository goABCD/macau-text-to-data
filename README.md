# 澳門相關標題：文本 → 數據

把澳門相關中文標題（新聞／徵文主題）做成小型文本分析：問題 → 數據 → 統計與可視化 → 對管理／決策的提示。不做複雜 NLP。

## 問題

公開場合反覆出現的澳門議題有哪些高頻詞與主題？這些信息對文旅運營、教育資源或城市管理有什麼可討論的提示？局限是什麼？

## 數據源

- `data/raw/macau_titles.csv`：示意語料（澳門相關新聞標題與公開徵文主題風格的中文標題）。
- **可替換**：澳門政府開放數據、本地新聞標題列表、公開徵文主題匯總等；保持 CSV 三列即可：`id,title,source,year`。

> 當前文件為演示語料，便於一鍵跑通流程；面試前請換成你可核驗的真實來源並在本 README 標明出處與抓取日期。

## 步驟

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/analyze.py
streamlit run app/streamlit_app.py   # 可選：簡易看板
```

1. **清洗**：讀 CSV、去空標題  
2. **分詞**：`jieba` + 精簡停用詞  
3. **詞頻**：統計高頻詞並出橫條圖  
4. **簡易主題**：關鍵詞規則歸入「文旅與客流／交通與城市／教育與青年／數據與決策／人口與公共服務」  
5. **輸出**：`data/processed/` 與 `figures/word_freq.png`

## 結論（示意語料下的寫法；換真數據後請重跑並改寫）

- 標題中「數據／旅客／教育／交通」等詞反覆出現，說明公開敘事同時關心**客流體驗**與**信息如何支持決策**。  
- 規則歸類能快速得到主題結構，適合管理者做「議題掃描」，但不能替代嚴格抽樣與因果推斷。  

## 局限

- 示意語料樣本小，不能代表全澳輿論。  
- 關鍵詞規則主題粗粒度，同義詞／反諷未處理。  
- 無時間序列建模；結論僅供討論「數據思維」，非政策建議。

## 技術棧

Python · pandas · jieba · matplotlib ·（可選）Streamlit

## 倉庫結構

```
data/raw/          原始標題
data/processed/    詞頻與主題匯總
src/analyze.py     主分析腳本
app/streamlit_app.py  可選看板
figures/           圖表
```
