import sys
from src.stocks_fetcher import StocksFetcher
sys.path.append("/.../src")

tickers = ["MSFT", "WMT", "LMT", "SPY", "GM", "PG"]
sf = StocksFetcher()
data = sf.fetch(
    tickers,
    "20220101",
    "20230101"
)

data.to_csv("./data.csv")

