"""
This module is responsible for testing the functions that fetch stock data.
"""
import sys
import unittest

from src.stocks_fetcher import StocksFetcher

sys.path.append("/.../src")


class TestStocksFetcher(unittest.TestCase):
    """
    Defines the TestStocksFetcher class which tests the StocksFetcher class.
    """
    def test_fetch_single_ticker(self):
        """
        Tests the fetch_stocks_data method with a single ticker.
        """
        start_str = "20230301"
        end_str = "20230302"
        ticker = "AAPL"
        tickers_str = [ticker]
        sf = StocksFetcher()
        res = sf.fetch_stocks_data(tickers_str, start_str, end_str)
        self.assertFalse(res.empty)
        self.assertTrue(len(res.index) > 250)
        self.assertListEqual(
            res.columns.to_list(),
            [ticker]
        )

    def test_fetch_mult_tickers(self):
        """
        Tests the fetch_stocks_data method with multiple tickers.
        """
        start_str = "20230301"
        end_str = "20230302"
        tickers_str = ["AAPL", "MSFT", "WMT"]
        sf = StocksFetcher()
        res = sf.fetch_stocks_data(tickers_str, start_str, end_str)
        self.assertFalse(res.empty)
        self.assertTrue(len(res.index) > 250)
        self.assertListEqual(
            res.columns.to_list(),
            tickers_str
        )
