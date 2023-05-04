"""
This module is responsible for testing the functions that calculate
backtest statistics.
"""
import os.path
import sys
import unittest
import pickle

import pandas as pd
import pytest

from src.run_backtest import MSR
from src.backtest_stats import BacktestStats

sys.path.append("/.../src")

class TestBacktestStats(unittest.TestCase):
    """
    Defines the TestBacktestStats class which tests the BacktestStats class.
    """

    def init_backtest_stats(self, optimizer: str):
        """
        Tests the BacktestStats class instantiation.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        portfolio_performance = pd.read_csv(
            os.path.join(
                current_dir,
                "data",
                optimizer + "_portfolio_performance.csv"
            ),
            dtype={"aum": "float64"},
            parse_dates=["datetime"],
        )

        weights_record_file = open(os.path.join(
                current_dir,
                "data",
                optimizer + "_weights_record.obj"
            ), "rb")
        weights_record = pickle.load(weights_record_file)
        weights_record_file.close()

        return BacktestStats(
            portfolio_performance,
            weights_record
        )

    def test_get_number_of_days(self):
        """
        Tests the get_number_of_days function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        number_of_days = backtest_stats.get_number_of_days()
        self.assertIsInstance(number_of_days, int)
        self.assertEqual(number_of_days, 120)

    def test_get_initial_aum(self):
        """
        Tests the get_initial_aum function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        initial_aum = backtest_stats.get_initial_aum()
        self.assertIsInstance(initial_aum, float)
        self.assertAlmostEqual(initial_aum, 10000.0)

    def test_get_final_aum(self):
        """
        Tests the get_final_aum function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        final_aum = backtest_stats.get_final_aum()
        self.assertIsInstance(final_aum, float)
        self.assertAlmostEqual(final_aum, 11705.99611698764)

    def test_get_profit_loss(self):
        """
        Tests the get_profit_loss function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        profit_loss = backtest_stats.get_profit_loss()
        self.assertIsInstance(profit_loss, float)
        self.assertAlmostEqual(profit_loss, 1705.9961169876406)

    def test_get_total_stock_return(self):
        """
        Tests the get_total_stock_return function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        total_stock_return = backtest_stats.get_total_stock_return()
        self.assertIsInstance(total_stock_return, float)
        self.assertAlmostEqual(total_stock_return, 0.17059961169876406)

    def test_get_annualized_rate_of_return(self):
        """
        Tests the get_annualized_rate_of_return function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        annualized_rate_of_return = \
            backtest_stats.get_annualized_rate_of_return()
        self.assertIsInstance(annualized_rate_of_return, float)
        self.assertAlmostEqual(annualized_rate_of_return, 0.6146391409654741)

    def test_get_daily_returns(self):
        """
        Tests the get_daily_returns function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        daily_returns = backtest_stats.get_daily_returns()
        self.assertIsInstance(daily_returns, list)
        daily_returns = [-0.14573694540287038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03481832327091306, 0.05130854393913742, 0.006929621538552025, -0.016005462098776374, 0.0036022626649987884, 0.025975316455011006, 0.01757611937741039, -0.03065927541816946, -0.01240701858838909, -0.020154991263109597, -0.02130749838608972, 0.10895969375730562, 0.10734686103117246, 0.02894584594974327, 0.0332985265030473, 0.029526956294118254, 0.012186271366384817, 0.01114858009498555, 0.025600362635148765, 0.04823150738750517, 0.03125460190286738, 0.0015774779242429258, -0.009482942403023359, -0.001667964424818854, -0.0008090366982534751, 0.007858642964813778, 0.0258475861260621, -0.007060614203302044, -0.006779793512445937, -0.04394242404942352, -0.05854060651059418, 0.007308211412118826, 0.009090056067473252, 0.011813821047666546, 0.02269221946677242, 0.017281137466977466, 0.005620570895451491, 0.0002703069284735159, 0.008258583432862737, 0.004448356744182193, 0.0013238447565757433, 0.010358983882585939, 0.005519088553211, 0.02250152531497666, 0.014057538789495805, -0.02460458588551084, -0.01926391233529495, 0.002758677930510106, 0.004565252774600558, 0.0018370893157625577, -0.006644117775047999, -0.0024189184586771895, -0.003140006752400823, -0.00728234341349974, 0.005931649147175071, 0.009050329616448754, 0.01222445901647702, -0.013951886460723581, -0.008951387419472356, 0.012788777666430391, -0.00037949716093836866, 0.0029912788458587264, 0.00672357518494679, -0.019564480431645832, -0.02053483983432188, -0.0009632920704258156, -0.006841596696523714, -0.037898020331356155, -0.02313832384659289, 0.008736603429808297, -0.0011897532945902467, -0.028444958734563305]
        for exp, act in zip(backtest_stats.get_daily_returns(), daily_returns):
            self.assertAlmostEqual(exp, act, 5)

    def test_get_average_daily_return(self):
        """
        Tests the get_average_daily_return function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        average_daily_return = backtest_stats.get_average_daily_return()
        self.assertIsInstance(average_daily_return, float)
        self.assertAlmostEqual(average_daily_return, 0.0026551631928844574)

    def test_get_daily_standard_deviation(self):
        """
        Tests the get_daily_standard_deviation function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        daily_standard_deviation = backtest_stats.get_daily_standard_deviation()
        self.assertIsInstance(daily_standard_deviation, float)
        self.assertAlmostEqual(daily_standard_deviation, 0.029477810451124346)

    def test_get_annualized_volatility(self):
        """
        TODO
        """
        backtest_stats = self.init_backtest_stats(MSR)
        daily_standard_deviation = backtest_stats.get_annualized_volatility()
        self.assertIsInstance(daily_standard_deviation, float)
        self.assertAlmostEqual(daily_standard_deviation, 0.4660851834598849)

    def test_get_daily_sharpe_ratio(self):
        """
        Tests the get_daily_sharpe_ratio function.
        """
        backtest_stats = self.init_backtest_stats(MSR)
        daily_sharpe_ratio = backtest_stats.get_daily_sharpe_ratio()
        self.assertIsInstance(daily_sharpe_ratio, float)
        self.assertAlmostEqual(daily_sharpe_ratio, 0.08668090179632043)

    def test_get_annualized_sharpe_ratio(self):
        """
        TODO
        """
        backtest_stats = self.init_backtest_stats(MSR)
        daily_standard_deviation = backtest_stats.get_annualized_sharpe_ratio()
        self.assertIsInstance(daily_standard_deviation, float)
        self.assertAlmostEqual(daily_standard_deviation, 1.3705452496776156)

    # Allows us to capture printing to standard output
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def test_print_summary(self):
        """
        Tests the print_summary method.
        """
        out_str = """
    Backtest Stats

    Annual Return: 61.464%
    Annual Volatility: 46.609%
    Annual Sharpe Ratio: 1.37055
    Total Stock Return: 17.060%
    Profit and Loss: 1705.99612
    
"""
        bts = self.init_backtest_stats(MSR)
        bts.print_summary()
        captured = self.capsys.readouterr()
        assert len(captured.out) == len(out_str)

    def test_plot_portfolio_weights(self):
        """
        Tests the plot_portfolio_weights method.
        """
        bts = self.init_backtest_stats(MSR)
        bts.plot_portfolio_weights(path="portfolio_line", plot="line")
        bts.plot_portfolio_weights(path="portfolio_bar", plot="stacked_bar")
        bts.plot_portfolio_weights(path="portfolio_area", plot="stacked_area")
        bts.plot_portfolio_weights(path="portfolio_pie", plot="pies")

        parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        expected_path = os.path.join(parent_dir, "portfolio_line.png")
        self.assertTrue(os.path.isfile(expected_path))

        parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        expected_path = os.path.join(parent_dir, "portfolio_bar.png")
        self.assertTrue(os.path.isfile(expected_path))

        parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        expected_path = os.path.join(parent_dir, "portfolio_area.png")
        self.assertTrue(os.path.isfile(expected_path))

        parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        expected_path = os.path.join(parent_dir, "portfolio_pie.gif")
        self.assertTrue(os.path.isfile(expected_path))
