#!/bin/bash
# Obsidian Local REST API 測試腳本
# 用 curl 測試 API 係咪正常運行

PORT=27124
API_KEY=$(cat "/d/ObsidianVault/AINotes/.obsidian/plugins/obsidian-local-rest-api/data.json" | grep -o '"apiKey":"[^"]*"' | cut -d'"' -f4)

echo "🔍 測試 Obsidian Local REST API..."
echo "Port: $PORT"
echo ""

# 測試列出所有 Note
echo "📋 列出 vault 入面嘅文件："
curl -sk -H "Authorization: Bearer $API_KEY" \
  "https://localhost:$PORT/vault/" | head -50

echo ""
echo ""

# 測試 API 狀態
echo "💚 API 狀態："
curl -sk -H "Authorization: Bearer $API_KEY" \
  "https://localhost:$PORT/" | head -20
