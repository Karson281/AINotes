#!/bin/bash
cd "$(dirname "$0")" || exit 1

echo "=== 掃描股票分析檔案 ==="
echo ""

# Collect all YYYYMMDD-*.md files, excluding non-ticker names
# Non-ticker names: Chinese characters, "Summary", or files not matching YYYYMMDD- pattern
declare -A groups

for f in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-*.md; do
    [ -f "$f" ] || continue
    ticker="${f:9}"
    ticker="${ticker%.md}"
    date="${f:0:8}"

    # Skip non-ticker: check if ticker contains only ASCII (no Chinese)
    # Also skip "Summary"
    if [ "$ticker" = "Summary" ]; then
        echo "  [SKIP] $f (not a stock ticker)"
        continue
    fi
    # Check for non-ASCII characters (Chinese)
    if echo "$ticker" | grep -qP '[^\x00-\x7F]'; then
        echo "  [SKIP] $f (not a stock ticker)"
        continue
    fi

    # Group by ticker: store "date|file"
    if [ -z "${groups[$ticker]}" ]; then
        groups[$ticker]="$date|$f"
    else
        groups[$ticker]="${groups[$ticker]} $date|$f"
    fi
done

echo ""
echo "=== 結果 ==="
echo ""

keep_count=0
del_count=0
keep_list=""
del_list=""

for ticker in "${!groups[@]}"; do
    items="${groups[$ticker]}"
    # Sort by date (descending) - each item is "date|file"
    # We'll just compare dates directly
    latest_date=""
    latest_file=""
    oldest=""

    IFS=' ' read -ra entries <<< "$items"
    for entry in "${entries[@]}"; do
        d="${entry%%|*}"
        f="${entry#*|}"
        if [ -z "$latest_date" ] || [ "$d" -gt "$latest_date" ]; then
            latest_date="$d"
            latest_file="$f"
        fi
    done

    # Now delete everything except the latest
    for entry in "${entries[@]}"; do
        d="${entry%%|*}"
        f="${entry#*|}"
        if [ "$f" = "$latest_file" ]; then
            echo "  [KEEP] $f"
            keep_list="$keep_list $f"
            keep_count=$((keep_count + 1))
        else
            echo "  [DEL] $f"
            del_list="$del_list $f"
            del_count=$((del_count + 1))
        fi
    done
done

echo ""
echo "=== 總計 ==="
echo "  保留: $keep_count 個檔案"
echo "  刪除: $del_count 個檔案"

echo ""
echo "=== 執行刪除 ==="
echo ""

for f in $del_list; do
    if rm -f "$f"; then
        echo "  ✅ 已刪除: $f"
    else
        echo "  ❌ 刪除失敗: $f"
    fi
done

echo ""
echo "=== 清理完成 ==="

# Clean up self
rm -f "$0"
