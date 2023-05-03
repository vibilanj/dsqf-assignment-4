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
YF_ADJUSTED_CLOSE = "Adj Close"


class StocksFetcher:
    """
    Defines the StocksFether class which fetches stocks data from yFinance.
    """

    def __init__(self) -> None:
        """
        This method initialises the StockFetcher class.
        """

    def fetch_stocks_data(
        self, tickers: List[str], beginning_date: str, ending_date: str
    ) -> pd.DataFrame:
        """
        TODO: _summary_

        Args:
            tickers (List[str]): _description_
            beginning_date (str): _description_
            ending_date (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
        dt_start = datetime.strptime(beginning_date, DATE_FORMAT) - \
            timedelta(days=430)
        dt_end = datetime.strptime(ending_date, DATE_FORMAT) + \
            timedelta(days=1)
        data = yf.download(
            tickers, 
            dt_start.strftime(YF_DATE_FORMAT),
            dt_end.strftime(YF_DATE_FORMAT),
            progress=False)[YF_ADJUSTED_CLOSE]
        if len(tickers) == 1:
            res = data.to_frame()
            res.rename(columns = {YF_ADJUSTED_CLOSE: tickers[0]}, inplace = True)
            return res
        return data
