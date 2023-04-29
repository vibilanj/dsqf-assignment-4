"""
This module is responsible for fetching the stocks data.
"""
from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd
import yfinance as yf

# Constants
DATE_FORMAT = "%Y%m%d"
YF_DATE_FORMAT = "%Y-%m-%d"


class StocksFetcher:
    """
    Defines the StocksFether class which fetches stocks data from yFinance.
    """

    def __init__(self) -> None:
        """
        This method initialises the StockFetcher class.
        """

    def fetch_stock_data(
        self, ticker_symbol: str, dt_start: datetime, dt_end: datetime
    ) -> pd.DataFrame:
        """
        Fetches the stock data from yFinance from the start date to the
        end date provided.

        Args:
          ticker_symbol (str): The ticker symbol of the stock.
          dt_start (datetime): The beginning date at which yFinance starts
            collecting data
          dt_end (datetime): The ending date at which yFinance starts
            collecting data

        Returns:
          pd.Dataframe: Returns a dataframe containing the stock data.
        """
        res = yf.Ticker(ticker_symbol).history(start=dt_start, end=dt_end)
        assert not res.empty
        return res

    def fetch_stocks_data(
        self, ticker_symbols: List[str], beginning_date: str, ending_date: str
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetches the stock data of multiple tickers from yFinance
        with an additional 1 year 2 months from the expected begin to end date.

        Args:
          ticker_symbol (List[str]): The ticker symbols of each stock in the
            universe.
          beginning_date (str): The beginning date inputted by the user.
          ending_date (str): The ending date inputted by the user.

        Returns:
          Dict[str, pd.DataFrame]: Returns a dictionary that maps each stock 
            ticker to the dataframe containing the stock data for that stock.
        """
        dt_start = datetime.strptime(beginning_date, DATE_FORMAT) - \
            timedelta(days=430)
        dt_end = datetime.strptime(ending_date, DATE_FORMAT) + \
            timedelta(days=1)
        res = {}
        for ticker_symbol in ticker_symbols:
            res[ticker_symbol] = \
                self.fetch_stock_data(ticker_symbol, dt_start, dt_end)
        return res
    def fetch(
        self, tickers: List[str], start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        TODO: _summary_

        Args:
            tickers (List[str]): _description_
            start_date (str): _description_
            end_date (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
        dt_start = datetime.strptime(start_date, DATE_FORMAT) - \
            timedelta(days=430)
        dt_end = datetime.strptime(end_date, DATE_FORMAT)
        return yf.download(
            tickers, 
            dt_start.strftime(YF_DATE_FORMAT), 
            dt_end.strftime(YF_DATE_FORMAT))