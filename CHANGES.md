# CHANGES — 本地定製改動記錄

本文件記錄 fork 自 ZhuLinsen/daily_stock_analysis 後，針對個人美股分析流程所做的定製改動。

---

## 2026-05-23

### 1. 繁體中文化

**改動檔案：**
- `src/analyzer.py` — `_get_analysis_system_prompt()`
- `strategies/bull_trend.yaml` — `instructions` 欄位

**內容：**
- `_get_analysis_system_prompt` 的中文語言指示段落改為要求 LLM 輸出**繁體中文**，採用台灣／香港慣用詞彙，明確禁止輸出簡體中文。
- `strategies/bull_trend.yaml` 的 `instructions` 全部翻譯為繁體中文。
- `REPORT_LANGUAGE=en` 環境變數保持不變（控制介面語言，不影響 LLM 輸出語言）。

---

### 2. M&A 企業事件偵測

**改動檔案：**
- `src/analyzer.py` — 新增 `_detect_ma_event()` 與 `_inject_ma_warning()` 兩個模組級函式，並在 `GeminiAnalyzer.analyze()` 中調用。

**內容：**
- 在 LLM 分析完成後，檢查 `news_context` 是否包含以下關鍵詞：
  `merger agreement`, `acquisition agreement`, `tender offer`, `going private`, `buyout`, `merger deal`, `takeover bid`, `acquisition`
- 如偵測到任一關鍵詞，自動：
  - 在報告頂部注入醒目警告：`⚠️ CORPORATE EVENT DETECTED：此股票可能涉及併購，技術分析參考價值有限`
  - 將 `decision_type` 覆寫為 `hold`，`operation_advice` 改為 `觀望`
  - 覆寫 `dashboard.core_conclusion` 為企業事件警告
  - 給出空倉者和持倉者的具體提示
- 此偵測作為 `screener.py` M&A 過濾的第二道防線（belt-and-suspenders）。

---

### 3. 分析師數據時效性

**改動檔案：**
- `src/analyzer.py` — `_get_analysis_system_prompt()`

**內容：**
- 在系統 prompt 加入「分析師評級時效規則（強制執行）」章節：
  - 只能引用最近 30 日內的分析師目標價及評級用於結論判斷。
  - 超過 30 日的舊評級只可列為歷史背景，嚴禁用於風險判斷或操作結論。
  - 若找不到 30 日內數據，須明確註明「近期無最新分析師目標」。
  - 若有多家機構評級，優先展示 30 日內的並標註 YYYY-MM-DD 日期。
- 注意：`_format_prompt` 中針對新聞段落已有類似規則，系統 prompt 的新增規則作為更早的全局約束。

---

### 4. Telegram 推送格式相容性

以上改動均在 `GeminiAnalyzer.analyze()` 的結果物件層面操作，不涉及 Telegram bot 的訊息組裝邏輯（`bot/` 目錄），`AnalysisResult` 的欄位結構保持不變，現有推送格式不受影響。

---

### 回滾方式

- `src/analyzer.py`：還原 `_get_analysis_system_prompt` 的語言段落、移除 `_detect_ma_event` / `_inject_ma_warning` 函式、移除 `analyze()` 中的 M&A 偵測呼叫。
- `strategies/bull_trend.yaml`：將 `instructions` 還原為英文版本（見 git history）。
