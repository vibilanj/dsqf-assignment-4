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
        self,
        tickers: List[str],
        beginning_date: str,
        ending_date: str
    ) -> pd.DataFrame:
        """
        Fetches the adjusted closing prices for multiple tickers from Yahoo
        Finance with an additional 430 days from the given beginning date 
        to the given ending date.

        Args:
            ticker_symbol (List[str]): The ticker symbols of each stock in
                the universe.
            beginning_date (str): The beginning date given by the user.
            ending_date (str): The ending date given by the user.

        Returns:
            pd.DataFrame: Returns a dataframe containing the adjusted 
                close price for each stock in the universe at each 
                trading date in the time frame.
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
            res.rename(columns = {YF_ADJUSTED_CLOSE: tickers[0]},
                       inplace = True)
            return res
        return data
