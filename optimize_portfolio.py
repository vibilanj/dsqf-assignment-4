"""
YSC4228: Data Science in Quantitative Finance
Group Assignment 4
Members:
- Alan Matthew Anggara
- Marcellinus Jerricho
- Vibilan Jayanth
- Nahian Chowdhury Nileema

Fetches daily stock information of specified stock tickers within
a given time frame and optimizes a monthly portfolio using the
PyPortfolioOpt library. Calculates various statistics based on the
portfolio backtesting simulation to provide an overview of the 
performance of the portfolio over the given time period.
"""
import sys

from src.backtest_stats import BacktestStats
from src.input_data import InputData
from src.run_backtest import RunBacktest
from src.stocks_fetcher import StocksFetcher

sys.path.append("/.../src")

if __name__ == "__main__":
    # Getting user input
    user_input = InputData()

    # Initialising and fetching stocks data
    fetcher = StocksFetcher()
    stocks_data = fetcher.fetch_stocks_data(
        tickers=user_input.get_tickers(),
        beginning_date=user_input.get_beginning_date(),
        ending_date=user_input.get_ending_date()
    )

    # Running the backtest simulation
    backtest = RunBacktest(
        stocks_data=stocks_data,
        initial_aum=user_input.get_initial_aum(),
        beginning_date=user_input.get_beginning_date(),
        optimizer=user_input.get_optimizer()
    )
    backtest.fill_up_portfolio_performance()

    # Getting the backtest performance and portfolio weights
    portfolio_perf = backtest.portfolio_performance
    weights_rec = backtest.weights_record

    # Calculating backtest statistics
    backtest_statistics = BacktestStats(
        portfolio_performance=portfolio_perf,
        weights_record = weights_rec
    )

    # Printing statistics summary and geenrating plots
    backtest_statistics.print_summary()
    if user_input.get_plot_weights():
        backtest_statistics.plot_portfolio_weights()
