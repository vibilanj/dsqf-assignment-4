"""
YSC4228: Data Science in Quantitative Finance
Group Assignment 4
Members:
- Alan Matthew Anggara
- Marcellinus Jerricho
- Vibilan Jayanth
- Nahian Chowdhury Nileema

TODO: Change description
Fetches daily stock information of specified stock tickers within
a given time frame and backtests a linear combination of two signals
for a monthly strategy. Calculates various statistics based on the
backtest simulation to provides an analysis of the strategy over the
given time period.
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
        ticker_symbols=user_input.get_tickers(),
        beginning_date=user_input.get_beginning_date(),
        ending_date=user_input.get_ending_date(),
    )

    # Running the backtest simulation
    backtest = RunBacktest(
        stocks_data=stocks_data,
        initial_aum=user_input.get_initial_aum(),
        beginning_date=user_input.get_beginning_date(),
        strategy1=user_input.get_strategy1_type(),
        strategy2=user_input.get_strategy2_type(),
        days1=user_input.get_days1(),
        days2=user_input.get_days2(),
        top_pct=user_input.get_top_pct(),
    )
    backtest.fill_up_portfolio_performance()
    backtest.calc_ic()

    # Getting the backtest performance and IC information
    portfolio_perf = backtest.portfolio_performance
    portfolio_ic = backtest.monthly_ic
    model_stats = backtest.model_statistics_record

    # Calculating backtest statistics
    backtest_statistics = BacktestStats(
        portfolio_performance=portfolio_perf,
        monthly_ic=portfolio_ic,
        model_statistics=model_stats,
    )

    # Printing statistics summary and geenrating plots
    backtest_statistics.print_summary()
    backtest_statistics.plot_daily_aum()
    backtest_statistics.plot_monthly_cumulative_ic()
