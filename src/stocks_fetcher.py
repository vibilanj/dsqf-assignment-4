"""
This module is responsible for fetching the stocks data.
"""
from datetime import datetime, timedelta
from typing import List

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

    def fetch_stocks_data(
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
        data = yf.download(
            tickers, 
            dt_start.strftime(YF_DATE_FORMAT), 
            dt_end.strftime(YF_DATE_FORMAT))["Adj Close"]
        if (len(tickers) == 1):
            res = data.to_frame()
            res.rename(columns = {'Adj Close': tickers[0]}, inplace = True)
            return res
        return data
