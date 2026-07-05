---
type: brainstorm
project: three-in-one-platform
date: 2026-07-04
status: draft
tags: [travel, price-comparison, consumer, telegram-bot, MVP]
---

# 🌐 三合一平台 Brainstorm — 旅行/格價/消費達人

## 現有基礎設施

| 元件 | 狀態 | 用途 |
|------|------|------|
| Hermes Agent (VPS) | ✅ | 核心推理 + 自然語言理解 |
| Telegram Gateway | ✅ | 用戶介面（已連接） |
| Kanban + Proma Worker | ✅ | 背景任務調度 + 異步執行 |
| DeepSeek V4 + Qwen-VL | ✅ | LLM + 圖片理解 |
| Google MCP (Gmail/Drive/Sheets) | ✅ | 數據存取能力 |
| Obsidian Vault (GitHub sync) | ✅ | 知識庫 + 記錄 |
| VPS (always-on) | ✅ | 24/7 運行 |
| 現有旅行筆記 | ✅ | vault/旅行/ 已有基礎資料 |

---

## 三大支柱詳細功能 Brainstorm

### ✈️ 第一支柱：旅行

#### 核心功能
| 功能 | 說明 | 數據源 | 難度 |
|------|------|--------|------|
| **行程規劃師** | 輸入目的地/日數/預算/偏好 → AI 生成每日行程 | LLM + Google Maps API | 🟡 中 |
| **機票格價** | 跨平台機票價格比較 + 價格提醒 | Skyscanner/Google Flights API | 🟡 中 |
| **酒店格價** | 酒店價格比對 + 性價比評分 | Booking/Agoda/Google Hotels | 🟡 中 |
| **旅遊保險比較** | 不同保險計劃對比 + 推薦 | CoverHero/Yulexpress | 🟢 低 |
| **行李清單** | 根據目的地/季節/行程類型自動生成 | LLM + 知識庫 | 🟢 低 |
| **目的地攻略** | 提取 vault 旅行筆記 + 網絡最新資訊 | Obsidian + web search | 🟢 低 |
| **簽證資訊** | 港人免簽/落地簽/電子簽國家查詢 | Wikipedia API | 🟢 低 |
| **匯率轉換** | 即時匯率 + 歷史走勢 | 央行 API | 🟢 低 |
| **天氣預報** | 目的地天氣 + 最佳旅遊月份 | OpenWeather | 🟢 低 |
| **機票價格預測** | 買定等？建議最佳入手時機 | Google Flights 預測 | 🔴 高 |

### 💰 第二支柱：格價

#### 核心功能
| 功能 | 說明 | 數據源 | 難度 |
|------|------|--------|------|
| **產品價格比較** | 掃 price.com.hk / 各大電商價格 | Web scraping | 🟡 中 |
| **歷史價格走勢** | 追蹤產品價格變化，睇低位入貨 | Price history DB | 🟡 中 |
| **超市格價** | 百佳/惠康/U購/一田 每日特價整合 | Web scraping + sheets | 🟡 中 |
| **電器格價** | 豐澤/百老匯/蘇寧/Segway | Web scraping | 🟢 低 |
| **優惠通知** | 心儀產品跌到目標價 → Telegram 通知 | Kanban cron | 🟡 中 |
| **餐飲優惠** | OpenRice 優惠券/信用卡折扣 | Web scraping | 🟢 低 |
| **格價地圖** | 邊區買最平（藥房/日用品） | Data aggregation | 🔴 高 |

### 🛍️ 第三支柱：消費達人

#### 核心功能
| 功能 | 說明 | 數據源 | 難度 |
|------|------|--------|------|
| **信用卡回贈計算** | 輸入消費類別 → 推薦最佳信用卡 | 銀行官網 | 🟡 中 |
| **現金回贈 App 比較** | Tap & Go/WeChat Pay/AlipayHK/BoC Pay 優惠 | Web scraping | 🟢 低 |
| **儲分攻略** | 亞洲萬里通/MTR分/易賞錢/YUU 點用最抵 | 知識庫 | 🟢 低 |
| **慳錢挑戰** | 個人化慳錢計劃（如：$100/日三餐） | LLM | 🟢 低 |
| **消費分析** | 每月支出分類 + 慳錢建議 | 銀行月結單 (Google MCP) | 🟡 中 |
| **團購優惠** | GroupBuyHK/KKDay/Klook 折扣 | Web scraping | 🟢 低 |
| **雙11/Black Friday攻略** | 年度大促策略 + 慳錢清單 | LLM + scrap | 🟢 低 |

---

## MVP 範圍建議

### Phase 1 — 基礎搭建（2-3 週）
```
🟢 Telegram Bot Command 框架
    ├── /travel  — 旅行功能入口
    ├── /price   — 格價功能入口
    ├── /save    — 消費達人入口
    └── /help    — 使用指南

🟢 旅行功能 MVP（最自然切入點，已有 vault 資料）
    ├── /itinerary [目的地] [天數] — AI 行程建議
    ├── /packing [目的地] [季節]   — 行李清單
    ├── /visa [目的地]              — 簽證查詢
    └── /exchange [金額] [貨幣]     — 匯率換算

🟢 格價功能 MVP
    └── /compare [產品名稱] — 查 price.com.hk 價格

🟢 消費達人 MVP
    └── /card [消費類別] — 推薦最佳信用卡
```

### Phase 2 — 智能通知（4-6 週）
```
🔔 價格追蹤 + Telegram alert
    ├── /track [產品] [目標價] — 設定價格提醒
    ├── /untrack [ID]           — 取消提醒
    ├── /mytracks               — 查看提醒列表
    └── 自動檢查 cron job（每日 08:00 / 18:00 HKT）

📊 每日精選
    ├── 超市特價 (07:00 HKT)
    ├── 信用卡優惠更新 (09:00 HKT)
    └── 旅行 deal（週末限定）
```

### Phase 3 — 進階功能（7-10 週）
```
🤖 智能對話模式
    ├── 自然語言：「聽日去東京三日，$5000 budget 有冇行程？」
    ├── 圖片分析：傳送月結單 screenshot → 分析消費
    └── 跨功能：「我想慳錢去日本旅行，有咩建議？」

📈 數據視覺化
    ├── 價格走勢圖（Text-based / Chart）
    ├── 消費分析儀表板
    └── 旅行預算追蹤
```

### Phase 4 — 網站/Web App（長期）
```
🌐 Web Dashboard（可選，非 MVP）
    ├── 價格歷史圖表（Chart.js / ECharts）
    ├── 旅行行程可視化（地圖 + timeline）
    ├── 消費分類圖表
    └── Obsidian vault 雙向同步
```

---

## UI/UX 策略：Telegram Bot First

### 點解 Telegram Bot 優先？
1. **零基建成本** — Hermes Gateway 已通 ✅
2. **用戶習慣** — 你已經日日用 Telegram 互動 ✅
3. **即時通知** — Push notification 天然支持 ✅
4. **跨平台** — Desktop + Mobile 一齊用 ✅
5. **LLM 原生介面** — 自然語言輸入更適合 AI 功能 ✅

### Command 設計原則
```
/command [參數] — 簡單查詢（低認知成本）
對話模式       — 複雜需求（AI 引導式）
定期推送       — 被動接收（不需用戶記得 check）
```

### Example 對話流程
```
你: /itinerary 東京 3日 5000 budget
Bot: ✈️ 東京三日行程建議（預算 $5,000 HKD）
     Day 1: 淺草+晴空塔 ($800)
     Day 2: 澀谷+新宿 ($1,200)  
     Day 3: 鎌倉一日遊 ($1,500)
     ［建議］酒店用 Agoda 而家做緊 -30%
     ［提醒］東京下週降雨率 40%，帶遮
     想調整？直接話我知～

你: 第二日想改去 Disney
Bot: 🏰 東京迪士尼一日（預算約 $1,500）
     Budget 會超 $300，建議：
     - Day 1 改免費景點慳 $200
     - 或 total budget 加 $300
     點睇？
```

---

## 技術考量

### 數據獲取策略
| 數據類型 | 方案 | 成本 | 備註 |
|---------|------|------|------|
| price.com.hk | Web scraping (Proma 定時爬取) | 免費 | 注意 rate limit |
| Google Flights | Google Flights API (需申請) | 免費 tier | 有限制 |
| Skyscanner | 官方 API | 免費 tier | 需申請 partner |
| 超市特價 | Web scraping 百佳/惠康 | 免費 | 可存 sheets |
| 信用卡優惠 | Web scraping 銀行官網 | 免費 | 定期更新 |
| 匯率 | ExchangeRate-API | 免費 | 1500 req/mo |
| 天氣 | OpenWeather Free API | 免費 | 60 req/min |

### 儲存策略
```
短期查詢 → LLM context（無需持久化）
價格追蹤 → SQLite + cron job（持久化 alert）
用戶偏好 → Obsidian vault / MEMORY.md
價格歷史 → SQLite / Google Sheets（可視化）
```

### Proma Worker 分工
| Task | 負責 | 排程 |
|------|------|------|
| 價格爬取 | Proma Worker | 每日 2 次 |
| 優惠更新 | Proma Worker | 每日 1 次 |
| 價格 alert 檢查 | Proma Worker | 每 30 分鐘 |
| 數據清洗 | Proma Worker | On-demand |
| LLM 推理/回應 | Hermes (VPS) | Real-time |

---

## 風險與注意事項

| 風險 | 緩解 |
|------|------|
| Web scraping 被 ban | 用 rotating UA + respectful delay；重要 data source 用 API |
| API 限額爆 | 設 caching layer；優先免費/低 quota source |
| 價格誤差 | 用戶免責聲明；提供直接連結讓用戶 double-check |
| Telegram 訊息太長 | 用分段 message + inline buttons |
| 數據過期 | 設 expiry timestamp；定期 refresh |
| 功能太多變 bloat | **MVP 嚴格守住**，唔好 scope creep |

---

## 下一步建議

### 立即行動（呢個 task 完成後）
1. 揀定 Phase 1 邊個功能最先做（建議 /itinerary — 最簡單、最直接有用）
2. 開新 Kanban task 俾 Proma Worker 做 price.com.hk scraping research
3. 測試 Google Flights API access
4. 設計 Telegram command handler 嘅 plugin 架構

### 設計決策（需要你拍板）
- [ ] 功能優先級：旅行 > 格價 > 消費達人？（建議順序）
- [ ] Price data source：自己 scrape price.com.hk 定用第三方 API？
- [ ] 信用卡數據：人手整理定自動 scrape？
- [ ] 消費分析：用戶上傳月結單（Google Sheets MCP）定係自己入數？
- [ ] Website 係咪真係需要定 Telegram Bot 就夠？

### 命名建議
考慮俾個平台一個易記名：
- **「慳啲啦」** — 貼地廣東話，cover 晒慳錢/格價/慳旅行
- **「TripPriceSave」** — 英文直接描述三大功能
- **「旅價達人」** — 中英混合，簡潔

---

*Brainstorm by Hermes Agent — 2026-07-04*
