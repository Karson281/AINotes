---
type: plugin-doc
status: completed
updated: 2026-07-12
tags:
  - obsidian
  - dashboard
  - dataview
  - creditcard
---
#  Plugin — 信用咭消費Dashboard 

> **狀態**：✅ 已成功部署  
> **日期**：2026-07-12  
> **耗時**：約 2 小時  
> **維護者**：Proma Agent

---
## 完成項目

### 三、信用咭 Dashboard 全面修復與強化

|Fix|狀態|
|:--|:-:|
|Dataview `dv already declared` IIFE wrap|✅|
|`dv.paragraph` → `dv.el("p")` API fix|✅|
|「Enable Inline Javascript Queries」setting|✅|
|AEON JCB 刪除（定額減免誤導）|✅|
|Enjoy Platinum bank fix (Standard Chartered→Hang Seng)|✅|
|Enjoy Platinum `local_retail: 8%` → `0`|✅|
|HSBC Red `local_dining/retail: 8%` → `0`|✅|
|日期自動匹配 merchant_specific condition|✅|
|商戶總覽 Dataview table|✅|
|**conditional flag 分級排序**|✅|

### 四、conditional flag 分級系統（今日核心創新）

- 🏆 **常用推薦 Top 2**：只顯示無條件通用卡（不受 merchant_specific 干擾）
- ⚠️ **條件觸發區**：日期/商戶限制嘅高回贈卡獨立顯示，僅供參考
- 📋 **全部無條件卡**：其餘通用卡
- 消費下限檢查：未達 `spend_min` 直接 skip
- 8% Enjoy Platinum 唔會再壓過 4% HSBC Red 常用卡

