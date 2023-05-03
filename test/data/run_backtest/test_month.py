import pandas as pd


file_path = "./test/data/run_backtest/data.csv"
data = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
data.index = data.index.map(pd.Timestamp)

# to slice
# data.iloc[start: end] not inclusive of end
# start must be end - 250