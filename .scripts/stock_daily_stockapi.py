#!/usr/bin/env python3
"""stock-api companion — parallel data collection for month-long comparison"""
import csv, json, os, subprocess, sys
from datetime import datetime
from pathlib import Path

STOCKAPI_DIR = "/root/stock-api"
STOCKAPI_CLI = os.path.join(STOCKAPI_DIR, "dist/cli.js")
DATA_FILE = "/root/vault/stock-api-comparison.csv"
TODAY = datetime.now().strftime("%Y%m%d")

# Mapping: (Yahoo ticker, stock-api code, name)
STOCKS = [
    # 港股
    ("0005.HK", "HK00005", "匯豐控股"),
    ("0006.HK", "HK00006", "電能實業"),
    ("0267.HK", "HK00267", "中信股份"),
    ("0270.HK", "HK00270", "粵海投資"),
    ("0363.HK", "HK00363", "上海實業"),
    ("0669.HK", "HK00669", "創科實業"),
    ("0823.HK", "HK00823", "領展房產基金"),
    ("0883.HK", "HK00883", "中國海洋石油"),
    ("0941.HK", "HK00941", "中國移動"),
    ("2388.HK", "HK02388", "中銀香港"),
    ("2800.HK", "HK02800", "盈富基金"),
    ("3466.HK", "HK03466", "香港高息股ETF"),
    ("3988.HK", "HK03988", "中國銀行"),
    ("6823.HK", "HK06823", "香港電訊"),
    # 美股
    ("JPM",   "USJPM",   "摩根大通"),
    ("ABBV",  "USABBV",  "艾伯維"),
    ("CVX",   "USCVX",   "雪佛龍"),
    ("O",     "USO",     "Realty Income"),
    ("VZ",    "USVZ",    "Verizon"),
]


def fetch_stockapi_batch(codes):
    """Call npx stock-api get-stocks with multiple codes"""
    try:
        result = subprocess.run(
            ["node", STOCKAPI_CLI, "get-stocks"] + codes,
            capture_output=True, text=True, timeout=20,
            cwd=STOCKAPI_DIR
        )
        if result.returncode != 0:
            print(f"  ⚠️ stock-api error: {result.stderr.strip()}")
            return {}
        data = json.loads(result.stdout)
        return {item["code"]: item for item in data}
    except Exception as e:
        print(f"  ❌ stock-api failed: {e}")
        return {}


def main():
    print("=== stock-api Companion v1 ===")
    print(f"Date: {datetime.now():%Y-%m-%d %H:%M}")

    # Fetch all stocks in one batch call
    codes = [s[1] for s in STOCKS]
    print(f"\nFetching {len(codes)} stocks via stock-api...")
    results = fetch_stockapi_batch(codes)
    print(f"  Got {len(results)}/{len(codes)} results")

    # Check if data file exists; if not, write header
    data_path = Path(DATA_FILE)
    write_header = not data_path.exists()

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                "date", "ticker_yahoo", "ticker_stockapi", "name",
                "price_stockapi", "change_pct_stockapi", "source"
            ])

        count = 0
        for yahoo_ticker, api_code, name in STOCKS:
            item = results.get(api_code)
            if item:
                writer.writerow([
                    TODAY, yahoo_ticker, api_code, name,
                    item.get("now", ""),
                    round(item.get("percent", 0) * 100, 2),
                    item.get("source", ""),
                ])
                count += 1

    print(f"\n✅ Saved {count} records to {DATA_FILE}")

    # Print quick summary
    print("\n📊 Today's stock-api prices:")
    for yahoo_ticker, api_code, name in STOCKS:
        item = results.get(api_code)
        if item:
            pct = round(item.get("percent", 0) * 100, 2)
            sign = "+" if pct >= 0 else ""
            print(f"  {api_code:>10}  {item['name']:　<12}  ¥{item['now']:<8}  {sign}{pct}%")
        else:
            print(f"  {api_code:>10}  {name:　<12}  ❌ no data")

    # Summary stats
    print(f"\n📈 Total records in CSV: {sum(1 for _ in open(DATA_FILE)) - 1}")


if __name__ == "__main__":
    main()
