from src.stocks_fetcher import StocksFetcher

tickers = ["MSFT", "WMT", "LMT", "SPY", "GM", "PG"]
sf = StocksFetcher()
data = sf.fetch_stocks_data(
    tickers,
    "20220915",
    "20230115"
)

data.to_csv("./data.csv")

