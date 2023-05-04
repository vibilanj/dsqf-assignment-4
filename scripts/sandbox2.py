import pandas as pd
import sys
sys.path.append("/.../src")

data_path = "./test/data/"
stocks_path = data_path + "stocks_data.csv"

stocks_data = pd.read_csv(stocks_path, parse_dates=["Date"], index_col="Date")
stocks_data.index = stocks_data.index.map(pd.Timestamp)

from src.run_backtest import RunBacktest

optimizer = "hrp"

rbt = RunBacktest(
    stocks_data,
    10000,
    "20220915",
    optimizer
)

rbt.fill_up_portfolio_performance()
rbt.portfolio_performance.to_csv(optimizer + "_portfolio_performance.csv", index=False)
