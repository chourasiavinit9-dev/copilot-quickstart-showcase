#!/usr/bin/env python3
"""
=============================================================================
REAL-TIME FINANCIAL DATA INGESTION PIPELINE FOR TIGER CLOUD
=============================================================================
Streams live market ticks (BTC/USD, ETH/USD, SOL/USD) and ingests them
directly into the TimescaleDB 'crypto_ticks' hypertable on Tiger Cloud.
Supports automated batch insertion, error handling, and CAGG tracking.
=============================================================================
"""

import sys
import time
import json
import urllib.request
import subprocess
from datetime import datetime, timezone

# ANSI Colors for terminal telemetry
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD"]


def fetch_live_tick(symbol):
    """Fetch live spot market price from Coinbase public API."""
    url = f"https://api.coinbase.com/v2/prices/{symbol}/spot"
    req = urllib.request.Request(url, headers={"User-Agent": "TigerData-Pipeline/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            price = float(data["data"]["amount"])
            # Calculate mock bid/ask spread around live spot price
            spread = price * 0.0002
            bid = round(price - spread, 2)
            ask = round(price + spread, 2)
            day_volume = round(price * 0.15, 4)
            return {
                "symbol": symbol.replace("-", "/"),
                "price": price,
                "bid": bid,
                "ask": ask,
                "day_volume": day_volume,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        print(f"{RED}[ERROR] Failed fetching {symbol}: {e}{RESET}")
        return None


def insert_ticks_batch(ticks):
    """Construct SQL multi-row insert and execute via Tiger CLI."""
    if not ticks:
        return False

    value_rows = []
    for t in ticks:
        row = f"('{t['timestamp']}', '{t['symbol']}', {t['price']}, {t['day_volume']}, {t['bid']}, {t['ask']})"
        value_rows.append(row)

    values_sql = ",\n   ".join(value_rows)
    sql = f"""INSERT INTO crypto_ticks (time, symbol, price, day_volume, bid, ask)
VALUES
   {values_sql};"""

    cmd = ["tiger", "db", "query", "-c", sql]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return True
    else:
        print(f"{RED}[DB ERROR] Failed inserting batch: {result.stderr or result.stdout}{RESET}")
        return False


def run_pipeline(target_ticks=30, batch_size=3, delay=1.0):
    """
    Main ingestion loop streaming live market data into Tiger Cloud.
    """
    print(f"\n{CYAN}{BOLD}=================================================================={RESET}")
    print(f"{CYAN}{BOLD}  TIGER CLOUD REAL-TIME FINANCIAL STREAMING PIPELINE{RESET}")
    print(f"{CYAN}{BOLD}  Ingesting live crypto market ticks into TimescaleDB Hypertable{RESET}")
    print(f"{CYAN}{BOLD}=================================================================={RESET}\n")

    total_ingested = 0
    batch = []

    while total_ingested < target_ticks:
        for symbol in SYMBOLS:
            tick = fetch_live_tick(symbol)
            if tick:
                batch.append(tick)
                print(f"{GREEN}[STREAM]{RESET} {tick['timestamp'][11:19]} UTC | {BOLD}{tick['symbol']:<7}{RESET} | Price: {YELLOW}${tick['price']:>10.2f}{RESET} | Bid: ${tick['bid']:>10.2f} | Ask: ${tick['ask']:>10.2f}")

            if len(batch) >= batch_size:
                sys.stdout.write(f"{CYAN}[INGEST] Batch of {len(batch)} ticks writing to Tiger Cloud... {RESET}")
                sys.stdout.flush()
                start_t = time.time()
                success = insert_ticks_batch(batch)
                latency_ms = (time.time() - start_t) * 1000

                if success:
                    total_ingested += len(batch)
                    print(f"{GREEN}✓ INGESTED in {latency_ms:.1f}ms{RESET} (Total: {total_ingested}/{target_ticks})")
                batch.clear()

            time.sleep(delay)

    print(f"\n{GREEN}{BOLD}🎉 Pipeline run complete! Successfully ingested {total_ingested} real-time ticks into Tiger Cloud!{RESET}\n")


if __name__ == "__main__":
    count = 15
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        count = int(sys.argv[1])
    run_pipeline(target_ticks=count, batch_size=3, delay=0.8)
