"""MarketWatch scraper API: DataGuru Python SDK example.

Runs DataGuru's MarketWatch APIs and prints the JSON they return:
  - MarketWatch Equity & ETF Quote: $0.0022 per successful request ($2.20 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/sdk_example.py            # every API below
    python examples/sdk_example.py marketwatch-equity-etf
"""
import json
import sys
from pathlib import Path

from dataguru import DataGuru, DataGuruError

def marketwatch_equity_etf(dg):
    """MarketWatch Equity & ETF Quote: Scrape equity and ETF quote data from MarketWatch including real-time price, change, bid/ask, ranges, volume, and exchange."""
    return dg.call(
        "marketwatch-equity-etf",
        target="AAPL",
    )


EXAMPLES = {
    "marketwatch-equity-etf": marketwatch_equity_etf,
}
DEFAULT = ['marketwatch-equity-etf']


def main(names):
    out = Path("output")
    out.mkdir(exist_ok=True)
    with DataGuru() as dg:  # reads DATAGURU_API_KEY
        for name in names:
            data = EXAMPLES[name](dg)
            (out / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{name}: saved output/{name}.json")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or DEFAULT
    unknown = [n for n in names if n not in EXAMPLES]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(EXAMPLES)}")
    try:
        main(names)
    except DataGuruError as error:
        sys.exit(f"DataGuru error: {error}")
