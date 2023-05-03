"""
This module is responsible for running the backtest simulation.
"""
from typing import Dict, List

import pandas as pd
from collections import OrderedDict

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.hierarchical_portfolio import HRPOpt
from pypfopt import risk_models
from pypfopt import expected_returns

# Constants
DATE_FORMAT = "%Y%m%d"
AUM = "aum"
DATETIME = "datetime"

# Optimizer Constants
MSR = "msr"
MV = "mv"
HRP = "hrp"


class RunBacktest:
    """
    Defines the RunBacktest class which runs the backtest based on
    the stock data obtained by the fetcher and the user defined
    inputs.
    """

    def __init__(
        self,
        stocks_data: pd.DataFrame,
        initial_aum: int,
        beginning_date: int,
        optimizer: str
    ):
        """
        TODO This method initialises the RunBacktest class.

        Args:
          stocks_data (Dict[str, pd.DataFrame]): The dictionary that matches
            the stock ticker to the price information of the stock.
          initial_aum (int): The initial asset under management amount.
          beginning_date (str): The beginning date of the backtest period.
        """
        self.stocks_data: Dict[str, pd.DataFrame] = stocks_data
        self.initial_aum: int = initial_aum
        self.beginning_date: str = beginning_date
        self.optimizer: str = optimizer

        """ TODO
        portfolio_performance (pd.DataFrame): The dataframe to store the
        portfolio performance information such as AUM and dividends.
        portfolio (List[Tuple[str, float]]): The list containing the
        current portfolio. Each element is a tuple of the stock ticker
        and the amount of the stock.
        portfolio_record (List[List[Tuple[str, float]]]): The list containing
        a record of previous portfolios. Each element is a portfolio.
        month_end_indexes (List[int]): The list of indexes of the month
        """
        self.portfolio_performance: pd.DataFrame = \
            self.init_portfolio_performance()
        self.portfolio: OrderedDict[str, float] = OrderedDict()
        self.portfolio_record: List[OrderedDict[str, float]] = []
        self.month_end_indexes: List[int] = self.get_month_end_indexes_from_b()

    def init_portfolio_performance(self) -> None:
        """
        None: Initialises the portfolio performance dataframe with
          the datetime indexes in the specified period and the initial
          AUM.
        """
        datetime_indexes = list(self.stocks_data.values())[0].index.to_list()
        portfolio_performance = pd.DataFrame()
        portfolio_performance[DATETIME] = datetime_indexes
        portfolio_performance[AUM] = [
            self.initial_aum for _ in range(len(datetime_indexes))
        ]
        return portfolio_performance

    def get_month_end_indexes_from_b(self) -> List[int]:
        """
        List[int]: Returns the indexes of the month end dates starting
          from the beginning date.
        """
        datetime_indexes = list(self.stocks_data.values())[0].index.to_list()
        b_timestamp = pd.to_datetime(self.beginning_date, format=DATE_FORMAT)
        month_end_indexes = []

        for idx, datetime in enumerate(datetime_indexes[:-1]):
            if datetime.month != datetime_indexes[idx + 1].month \
                and datetime_indexes[idx].tz_localize(None) > b_timestamp:
                month_end_indexes.append(idx)

        return month_end_indexes

    def calc_aum(self, date_index: int) -> float:
        """
        Calculates the assets under management amount for a given date index.

        Args:
          date_index (int): The index of the date at which AUM must be
            calculated

        Returns:
          float: Returns the AUM amount.
        """
        total_aum = 0
        for stock, amount in self.portfolio.items():
            if (amount != 0.0):
                end_close = self.stocks_data[stock].iloc[date_index]
                total_aum += amount * end_close
        return total_aum
    
    def update_portfolio(self, date_index: int) -> None:
        """TODO

        Args:
            date_index (int): _description_
        """
        df = self.stocks_data[date_index - 249, date_index + 1]
        sample_covariance = risk_models.sample_cov(df)
        if self.optimizer == HRP:
            hrp = HRPOpt(df, sample_covariance)
            hrp.optimize()
            weights = hrp.clean_weights()
        else:
            exp_returns = expected_returns.mean_historical_return(df)
            ef = EfficientFrontier(exp_returns, sample_covariance)
            if self.optimizer == MSR:
                ef.max_sharpe()
            else:
                ef.min_volatility()
            weights = ef.clean_weights()

        self.portfolio = weights
        self.portfolio_record.append(self.portfolio)

    def fill_up_portfolio_performance(self) -> None:
        """TODO
        None: Simulates backtesting based on the user-defined strategies and
          fills up the dataframe of portfolio performance with the calculated
          AUM for each day in the specified time period.
        """
        for date_index in range(self.month_end_indexes[0], len(list(self.stocks_data.values())[0].index)):
            self.portfolio_performance.at[date_index, AUM] = self.calc_aum(date_index)

            # rebalance and store new portfolio
            if date_index in self.month_end_indexes:
                self.update_portfolio(date_index)

        # cut portfolio performance to only start from beginning date
        datetime_indexes = self.portfolio_performance[DATETIME].to_list()
        b_idx = None
        for idx, datetime in enumerate(datetime_indexes):
            if datetime.tz_localize(None) >= pd.to_datetime(
                self.beginning_date, format=DATE_FORMAT
            ):
                b_idx = idx
                break
        self.portfolio_performance = \
            self.portfolio_performance[b_idx:].reset_index(
            drop=True
        )
