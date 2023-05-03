import pandas as pd

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.hierarchical_portfolio import HRPOpt
from pypfopt import risk_models
from pypfopt import expected_returns


file_path = "./test/data/run_backtest/data.csv"
data = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
data.index = data.index.map(pd.Timestamp)

# configurations
date_index = 528

# Calculations
# Calculate expected returns and sample covariance
df = data[date_index - 249: date_index + 1]
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# Optimize for maximal Sharpe ratio
ef_msr = EfficientFrontier(mu, S)
weights_msr = ef_msr.max_sharpe()
clean_weights_msr = ef_msr.clean_weights()

# Optimize for minimum variance/min volatility 
ef_mv = EfficientFrontier(mu, S)
weights_mv = ef_mv.min_volatility()
clean_weights_mv = ef_mv.clean_weights()

# Optimize for heirarchical risk parity
hrp = HRPOpt(df, S)
hrp.optimize()
clean_weights_hrp = hrp.clean_weights()

# print weights
print("Weights")
print("msr:", clean_weights_msr)
print("mv:", clean_weights_mv)
print("hrp:", clean_weights_hrp)