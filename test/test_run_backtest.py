"""
This module is responsible for testing the functions that simulate
the backtest
"""
import pickle
import sys
import unittest

import pandas as pd

from src.run_backtest import AUM, DATE_FORMAT, HRP, MSR, MV, RunBacktest

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
    start_str = "20220915"
    end_str = "20230115"
    initial_aum = 10000

    data_path = "./test/data/"
    stocks_path = data_path + "stocks_data.csv"

    stocks_data = pd.read_csv(stocks_path,
                              parse_dates=["Date"],
                              index_col="Date")
    stocks_data.index = stocks_data.index.map(pd.Timestamp)

    def init_run_backtest(self, optimizer: str):
        """
        Tests the RunBacktest class instantiation.
        """
        return RunBacktest(
            self.stocks_data,
            self.initial_aum,
            self.start_str,
            optimizer
        )

    def test_get_month_end_indexes_from_b(self):
        """
        Tests the get_month_end_indexes_from_b method.
        """
        rbt = self.init_run_backtest(MSR)
        self.assertEqual(len(rbt.month_end_indexes), 4)
        month_end_dates = self.stocks_data\
            .index[rbt.month_end_indexes]\
            .map(lambda s: s.strftime(DATE_FORMAT)).to_list()
        expected = ["20220930", "20221031", "20221130", "20221230"]
        self.assertListEqual(month_end_dates, expected)

    def helper_portfolio_performance(self, optimizer: str):
        """
        Auxiliary function that tests the fill_up_portfolio_performance method
        for a given optimizer.
        """
        rbt = self.init_run_backtest(optimizer)
        rbt.fill_up_portfolio_performance()

        # test weights
        file_wr = open(self.data_path + optimizer + "_weights_record.obj", "rb")
        weights_record = pickle.load(file_wr)
        file_wr.close()
        self.assertEqual(weights_record, rbt.weights_record)

        # test portfolio performance
        portfolio_perf = pd.read_csv(
            self.data_path + optimizer + "_portfolio_performance.csv")
        res = rbt.portfolio_performance[AUM]
        expected = portfolio_perf[AUM]
        for i in range(len(res)):
            self.assertAlmostEqual(res.iloc[i], expected.iloc[i])

    def test_fill_up_portfolio_performance_msr(self):
        """
        Tests the fill_up_portfolio_performance method with the Maximum
        Sharpe Ratio (MSR) optimizer.
        """
        self.helper_portfolio_performance(MSR)

    def test_fill_up_portfolio_performance_mv(self):
        """
        Tests the fill_up_portfolio_performance method with the Minimum
        Variance (MV) optimizer.
        """
        self.helper_portfolio_performance(MV)

    def test_fill_up_portfolio_performance_hrp(self):
        """
        Tests the fill_up_portfolio_performance method with the Hierarchical
        Risk Parity (HRP) optimizer.
        """
        self.helper_portfolio_performance(HRP)

