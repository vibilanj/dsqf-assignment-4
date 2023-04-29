import sys

from src.backtest_stats import BacktestStats
from src.input_data import InputData
from src.run_backtest import RunBacktest
from src.stocks_fetcher import StocksFetcher

sys.path.append("/.../src")

fetcher = StocksFetcher()
stocks_data = fetcher.fetch_stocks_data(
    ticker_symbols=["MSFT", "TSLA", "AAPL"],
    beginning_date="20220101",
    ending_date="20230101",
)