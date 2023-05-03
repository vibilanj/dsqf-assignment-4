"""
This module is responsible for testing the functions that simulate
the backtest
"""
import sys
import unittest

import pandas as pd

from src.run_backtest import (
    DATE_FORMAT,
    MSR,
    MV,
    HRP,
    RunBacktest,
)

sys.path.append("/.../src")

# Ticker Constants
MSFT = "MSFT"
WMT = "WMT"
LMT = "LMT"
SPY = "SPY"
GM = "GM"
PG = "PG"



class TestRunBacktest(unittest.TestCase):
    """
    Defines the TestRunBacktest class which tests the RunBacktest class.
    """

    tickers = [MSFT, WMT, LMT, SPY, GM, PG]

    # RunBacktest parameters
    start_str = "20220701"
    end_str = "20230131"
    initial_aum = 10000

    path = "./test/data/run_backtest/data.csv"
    stocks_data = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    stocks_data.index = stocks_data.index.map(pd.Timestamp)

    def init_run_backtest(self):
        """
        Tests the RunBacktest class instantiation.
        """
        return RunBacktest(
            self.stocks_data,
            self.initial_aum,
            self.start_str,
            MSR
        )

    def test_get_month_end_indexes_from_b(self):
        """
        Tests the get_month_end_indexes_from_b method.
        """
        rbt = self.init_run_backtest()
        self.assertEqual(len(rbt.month_end_indexes), 5)
        date_indexes = self.stocks_data[self.tickers[3]].index
        expected = ["20220729", "20220831", "20220930", "20221031", "20221130", "20221230"]
        for idx, month_end_index in enumerate(rbt.month_end_indexes):
            self.assertEqual(
                date_indexes[month_end_index].strftime(DATE_FORMAT),
                expected[idx]
            )

    def test_calc_portfolio(self):
        """
        Tests the calc_portfolio method.
        """
        self.assertEqual(0, 0)


    def test_fill_up_portfolio_performance(self):
        """
        Tests the fill_up_portfolio_performance method.
        """
        self.assertEqual(0, 0)
