"""
This module is responsible for running the backtest simulation.
"""
from collections import OrderedDict
from typing import Dict, List, Tuple

import pandas as pd
from pypfopt import expected_returns, risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.hierarchical_portfolio import HRPOpt

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
        beginning_date: str,
        optimizer: str
    ):
        """
        This method initialises the RunBacktest class.

        Args:
            stocks_data (pd.DataFrame): The dataframe containing the adjusted
              close price for all stocks throughout the time frame.
            initial_aum (int): The initial asset under management amount.
            beginning_date (str): The beginning date of the backtest period.
            optimizer (str): The optimizer to use for asset allocation.
        """
        self.stocks_data: Dict[str, pd.DataFrame] = stocks_data
        self.initial_aum: int = initial_aum
        self.beginning_date: str = beginning_date
        self.optimizer: str = optimizer

        """
        portfolio_performance (pd.DataFrame): The dataframe to store the
            portfolio performance information (AUM).
        portfolio (OrderedDict[str, float]): The ordered dictionary
            containing the current portfolio. Each ticker is matched to the 
            amount of stock held.
        portfolio_record (List[OrderedDict[str, float]]): The list containing
            a record of previous portfolios. Each element is a portfolio.
        weights_record (Tuple[List[str], List[OrderedDict[str, float]]]): 
            A tuple containing a list of portfolio rebalance dates and a list
            of ordered dictionaries containing the portfolio weights. Each
            ticker is matched to the weight held in the portfolio.
        month_end_indexes (List[int]): The list of month end indexes in the 
            time frame
        """
        self.portfolio_performance: pd.DataFrame = \
            self.init_portfolio_performance()
        self.portfolio: OrderedDict[str, float] = OrderedDict()
        self.portfolio_record: List[OrderedDict[str, float]] = []
        self.weights_record: Tuple[List[str], List[OrderedDict[str, float]]] = ([], [])
        self.month_end_indexes: List[int] = self.get_month_end_indexes_from_b()

    def init_portfolio_performance(self) -> None:
        """
        None: Initialises the portfolio performance dataframe with
            the datetime indexes in the specified period and the initial
            AUM.
        """
        datetime_indexes = self.stocks_data.index.to_list()
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
        datetime_indexes = self.stocks_data.index.to_list()
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
            if amount != 0.0:
                end_close = self.stocks_data[stock].iloc[date_index]
                total_aum += amount * end_close
        return total_aum

    def update_portfolio(self, date_index: int) -> None:
        """
        Updates the portfolio at a given date index. Creates an optimizer
        object based on the optimizer and calculated the portfolio weights.
        Updates the weights record, portfolio and the portfolio record.

        Args:
            date_index (int): The index of the date at which the 
                portfolio is calculated and updated.
        """
        df = self.stocks_data[date_index - 249 : date_index + 1]
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

        date = str(self.stocks_data.index[date_index])[:10]
        self.weights_record[0].append(date)
        self.weights_record[1].append(weights)

        portfolio = weights.copy()
        aum = self.portfolio_performance.at[date_index, AUM]
        for stock, weight in portfolio.items():
            portfolio[stock] = weight * aum / self.stocks_data[stock].iloc[date_index]

        self.portfolio = portfolio
        self.portfolio_record.append(self.portfolio)

    def fill_up_portfolio_performance(self) -> None:
        """
        None: Simulates backtesting based on the user-defined optimizer and
            fills up the dataframe of portfolio performance with the calculated
            AUM for each day in the specified time period.
        """
        for date_index in range(self.month_end_indexes[0],
                                len(self.stocks_data.index)):
            if date_index != self.month_end_indexes[0]:
                self.portfolio_performance.at[date_index, AUM] =\
                    self.calc_aum(date_index)

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
