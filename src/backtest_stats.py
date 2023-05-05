"""
This module is responsible for the backtest statistics.
"""
from collections import OrderedDict
from math import sqrt
from typing import List, Tuple

from matplotlib import animation
import matplotlib.pyplot as plt
import pandas as pd

# Constants
DATETIME = "datetime"
AUM = "aum"
IC = "ic"
TRADING_DAYS_PER_YEAR = 250


class BacktestStats:
    """
    Defines the BacktestStats class which calculates statistics based
    on the backtest portfolio performance and monthly portfolio weights.
    """

    def __init__(
        self,
        portfolio_performance: pd.DataFrame,
        weights_record: Tuple[List[str], List[OrderedDict[str, float]]]
    ):
        """
        This method initialises the BacktestStats class.

        Args:
            portfolio_performance (pd.Dataframe): The dataframe containing
                the portfolio performance information calculated during the
                backtest simulation.
            weights_record (Tuple[List[str], List[OrderedDict[str, float]]]):
                The tuple containing the portfolio weight information
                calculated during the backtest simulation.
        """
        self.portfolio_performance: pd.DataFrame = portfolio_performance
        self.weights_record: \
            Tuple[List[str], List[OrderedDict[str, float]]] = weights_record

        """
        beginning_trading_date (pd.Timestamp): The timestamp of the
            beginning trading day.
        ending_trading_date (pd.Timestamp): The timestamp of the
            ending trading day.
        """
        self.beginning_trading_date: pd.Timestamp = \
          self.portfolio_performance[DATETIME][0]
        self.ending_trading_date: pd.Timestamp = \
          list(self.portfolio_performance[DATETIME])[-1]

    def get_number_of_days(self) -> int:
        """
        int: Returns the number of calendar days from the beginning date
            to the ending date.
        """
        return (self.ending_trading_date -\
                self.beginning_trading_date).round("1d").days

    def get_initial_aum(self) -> float:
        """
        float: Returns the initial assets under management amount.
        """
        return self.portfolio_performance[AUM][0]

    def get_final_aum(self) -> float:
        """
        float: Returns the final assets under management amount.
        """
        return list(self.portfolio_performance[AUM])[-1]

    def get_profit_loss(self) -> float:
        """
        float: Returns the profit or loss during the backtest.
        """
        return self.get_final_aum() - self.get_initial_aum()

    def get_total_stock_return(self) -> float:
        """
        float: Returns the total stock return of the backtest strategy.
        """
        return (self.get_final_aum() - self.get_initial_aum()) / \
            self.get_initial_aum()

    def get_annualized_rate_of_return(self) -> float:
        """
        float: Returns the annualized rate of return of the
            backtest strategy calculated based on the formula
            from the following source:
            https://www.investopedia.com/terms/a/annualized-rate.asp
        """
        return (
            (self.get_initial_aum() + self.get_profit_loss()) / \
                self.get_initial_aum()
        ) ** (365 / self.get_number_of_days()) - 1

    def get_daily_returns(self) -> List[float]:
        """
        List[float]: Returns a list of daily returns of the portfolio.
        """
        daily_returns = []
        daily_aum_list = list(self.portfolio_performance[AUM])
        for idx, daily_aum in enumerate(daily_aum_list[1:]):
            yesterday_aum = daily_aum_list[idx - 1]
            daily_return = (daily_aum - yesterday_aum) / yesterday_aum
            daily_returns.append(daily_return)
        return daily_returns

    def get_average_daily_return(self) -> float:
        """
        float: Returns the average daily return of the portfolio.
        """
        daily_returns = self.get_daily_returns()
        return sum(daily_returns) / len(daily_returns)

    def get_daily_standard_deviation(self) -> float:
        """
        float: Returns the standard deviation of the daily returns
            of the portfolio.
        """
        daily_returns = self.get_daily_returns()
        average_daily_return = self.get_average_daily_return()
        daily_deviations = [
            daily_return - average_daily_return for daily_return \
                in daily_returns
        ]
        squared_daily_deviations = [
            daily_deviation**2 for daily_deviation in daily_deviations
        ]
        average_squared_daily_deviations = sum(squared_daily_deviations) / len(
            squared_daily_deviations
        )
        return sqrt(average_squared_daily_deviations)

    def get_annualized_volatility(self) -> float:
        """ 
        float: Returns the annualized standard deviation or the
            annualized volatility of the daily returns of the 
            portfolio (assuming 250 trading days in a year) calculated
            based on the information from the following source: 
            https://am.jpmorgan.com/hk/en/asset-management/adv/tools-resources/investment-glossary/ 
        """
        return self.get_daily_standard_deviation() * sqrt(TRADING_DAYS_PER_YEAR)

    def get_daily_sharpe_ratio(self) -> float:
        """
        float: Returns the sharpe ratio of the portfolio (assuming
            a daily risk-free rate of 0.01%) calculated based on the
            formula from the following source:
            https://www.realvantage.co/insights/what-is-sharpe-ratio/
        """
        return (
            self.get_average_daily_return() - 0.0001
        ) / self.get_daily_standard_deviation()

    def get_annualized_sharpe_ratio(self) -> float:
        """
        float: Returns the annualized sharpe ratio of the portfolio
            (assuming 250 trading days in a year) calculated based on
            the information from the following source: 
            https://am.jpmorgan.com/hk/en/asset-management/adv/tools-resources/investment-glossary/ 
        """
        return self.get_daily_sharpe_ratio() * sqrt(TRADING_DAYS_PER_YEAR)

    def print_summary(self) -> None:
        """
        None: Prints the formatted summary of the calculated portfolio
            statistics.
        """
        out_str = f"""
    Backtest Stats

    Annual Return: {self.get_annualized_rate_of_return() * 100:.3f}%
    Annual Volatility: {self.get_annualized_volatility() * 100:.3f}%
    Annual Sharpe Ratio: {self.get_annualized_sharpe_ratio():.5f}
    Total Stock Return: {self.get_total_stock_return() * 100:.3f}%
    Profit and Loss: {self.get_profit_loss():.5f}
    """
        print(out_str)

    def plot_portfolio_weights(
            self,
            path: str = "portfolio_weights",
            plot: str = "line"
        ) -> None:
        """
        Plots the portfolio weights at each rebalance date throughout
        the backtesting period.

        Args:
            path (str): Specifies the path where the plot is saved.
                Defaults to "portfolio_weights".
            plot (str): Specifies the type of plot to product. Allowed
                plot types are "line", "stacked_bar", "stacked_area" and
                "pies". Defaults to "line".

        Returns:
            None: Generates a plot of the portfolio weights and saves it to
                a file.
        """
        weights = pd.DataFrame(self.weights_record[1],
                               index=self.weights_record[0])

        if plot == "line":
            weights.index = pd.to_datetime(weights.index)
            fig = weights.plot.line(
                title="Portfolio Weights over Time",
                grid=True,
                legend=False,
                xlabel="Date",
                ylabel="Weight",
                marker="o"
            ).get_figure()
            fig.legend(loc="center right")
            fig.subplots_adjust(right=0.83)
            fig.savefig(path)
            fig.clf()
        elif plot == "stacked_bar":
            fig = weights.plot.bar(
                stacked=True,
                title="Portfolio Weights over Time",
                grid=True,
                legend=False,
                xlabel="Date",
                ylabel="Weight"
            ).get_figure()
            fig.legend(loc="center right")
            fig.autofmt_xdate()
            fig.subplots_adjust(right=0.83)
            fig.savefig(path)
            fig.clf()
        elif plot == "stacked_area":
            fig = weights.plot.area(
                stacked=True,
                title="Portfolio Weights over Time",
                grid=True,
                legend=False,
                xlabel="Date",
                ylabel="Weight"
            ).get_figure()
            fig.legend(loc="center right")
            fig.autofmt_xdate()
            fig.subplots_adjust(right=0.83)
            fig.savefig(path)
            fig.clf()
        elif plot == "pies":
            fig, ax = plt.subplots()
            def update(frame):
                ax.clear()
                ax.set_title(f"Portfolio Weights ({weights.index[frame]})")
                ax.axis("equal")
                ax.pie(weights.iloc[frame],
                       labels=weights.columns,
                       autopct="%1.1f%%")
            ani = animation.FuncAnimation(fig,
                                          update,
                                          frames=len(weights),
                                          interval=500,
                                          repeat=True)
            ani.save(f"{path}.gif", writer="imagemagick", fps=2)
            plt.close()
