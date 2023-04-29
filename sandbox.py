# import sys

# from src.backtest_stats import BacktestStats
# from src.input_data import InputData
# from src.run_backtest import RunBacktest
# from src.stocks_fetcher import StocksFetcher

# sys.path.append("/.../src")

# fetcher = StocksFetcher()
# stocks_data = fetcher.fetch_stocks_data(
#     ticker_symbols=["MSFT", "TSLA", "AAPL"],
#     beginning_date="20220101",
#     ending_date="20230101",
# )


import yfinance as yf
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

tickers = ["MSFT", "TSLA", "AAPL"]
df = yf.download(tickers, start="2021-01-01", end="2022-02-01")["Adj Close"]

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# Optimize for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
ef.portfolio_performance(verbose=True)
