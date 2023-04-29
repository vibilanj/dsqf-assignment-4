"""
This module is responsible for getting, validating and organizing user input.
"""
import argparse
from datetime import datetime
from typing import List

# Constants
DATETIME_FORMAT = "%Y%m%d"
DATE_TODAY = datetime.today().strftime(DATETIME_FORMAT)
MIN_TICKER_LENGTH = 1
MAX_TICKER_LENGTH = 5
MIN_DAYS = 1
MAX_DAYS = 250
MIN_PCT = 1
MAX_PCT = 100
DATE_LENGTH = 8
OPTIMIZERS = ["msr", "mv", "hrp"]


def get_args() -> argparse.Namespace:
    """
    argparse.Namespace: Returns the command line arguments entered
      by the user
    """
    parser = argparse.ArgumentParser(
        description="""Fetches daily close prices from the internet for given
    tickers and time frame and then back tests some
    simple momentum and reversal monthly strategies."""
    )
    parser.add_argument(
        "--tickers",
        type=str,
        help="The comma-separated stock tickers (e.g., MSFT,AMZN,WMT)",
        required=True,
    )
    parser.add_argument(
        "--b",
        type=int,
        help="The beginning date of the period in format YYYYMMDD",
        required=True,
    )
    parser.add_argument(
        "--e",
        type=int,
        help="The ending date of the period in format YYYYMMDD (optional)",
        required=False,
    )
    parser.add_argument(
        "--initial_aum",
        type=int,
        help="The initial asset under management (e.g., USD 10000)",
        required=True,
    )
    parser.add_argument(
        "--optimizer",
        type=str,
        help="The optimizer to use (e.g., msr, mv, hrp)",
        required=True,
    )
    parser.add_argument(
        "--plot_weights",
        help="Whether to plot the weights of the portfolio",
        action="store_true"
    )

    return parser


class InputData:
    """
    Defines the InputData class which validates and organises user input.
    """

    def __init__(
        self,
        tickers: str = -1,
        b: int = -1,
        e: int = -1,
        initial_aum: int = -1,
        optimizer: str = -1,
        plot_weights: bool = -1,
    ) -> None:
        """
        This method initialises the InputData class.

        Attributes:
          tickers (str): The user input of stocks in the universe.
          b (int): The user input of beginning date.
          e (int): The user input of ending date.
          intial_aum (int): The user input of initial AUM.
          strategy1_type (str): The user input of strategy 1 type.
          strategy2_type (str): The user input of strategy 2 type.
          days1 (int): The user input of number of days for strategy 1.
          days2 (int): The user input of number of days for strategy 2.
          top_pct (int): The user input of percentage of stocks to pick.
        """
        if tickers == -1:
            self.tickers = get_args().parse_args().tickers
        else:
            self.tickers = tickers

        if b == -1:
            self.b = get_args().parse_args().b
        else:
            self.b = b

        if e == -1:
            self.e = get_args().parse_args().e
        else:
            self.e = e

        if initial_aum == -1:
            self.initial_aum = get_args().parse_args().initial_aum
        else:
            self.initial_aum = initial_aum

        if optimizer == -1:
            self.optimizer = get_args().parse_args().optimizer
        else:
            self.optimizer = optimizer

        if plot_weights == -1:
            self.plot_weights = get_args().parse_args().plot_weights
        else:
            self.plot_weights = plot_weights

    def get_tickers(self) -> List[str]:
        """
        Returns a validated list of tickers from user input.

        Raises:
          ValueError: If the ticker symbol is not a string, is not alphanumeric,
            is not between 1 to 5 characters long, or is not a valid
            ticker symbol.

        Returns:
          List[str]: Returns the list of tickers if each ticker has been
            validated.
        """
        if self.tickers is None:
            raise ValueError("Tickers must be specified.")
        if isinstance(self.tickers, int):
            raise ValueError("Ticker must be a string.")
        tickers = [ticker.strip() for ticker in self.tickers.split(",")]
        for ticker in tickers:
            if not ticker.isalnum():
                raise ValueError(\
                    "Ticker must be a string of alphanumeric characters.")
            if len(ticker) > MAX_TICKER_LENGTH \
                or len(ticker) < MIN_TICKER_LENGTH:
                raise \
                    ValueError("Ticker must be between 1 to 5 characters long.")
        return tickers

    def get_beginning_date(self) -> str:
        """
        Returns a validated beginning date from the user input.

        Raises:
          ValueError: If the beginning date is not an integer, is not in format
            YYYYMMDD, is greater than the ending date, or is greater than the
            current date.

        Returns:
          str: Returns the beginning date if it has been validated.
        """
        if self.b is None:
            raise ValueError("Beginning date must be specified")
        if not isinstance(self.b, int):
            raise ValueError("Beginning date must be an integer.")
        if len(str(self.b)) != DATE_LENGTH:
            raise ValueError("Beginning date must be in format YYYYMMDD.")
        if int(str(self.b)) > int(DATE_TODAY):
            raise ValueError(
                """
      Beginning date must be less than or equal to the current date."""
            )
        return str(self.b)

    def get_ending_date(self) -> str:
        """
        Returns a validated ending date from the user input.

        Raises:
          ValueError: If the ending date is not an integer, is not in format
            YYYYMMDD, is less than the beginning date, or is greater than the
            current date.

        Returns:
          str: Returns the ending date if it has been validated.
        """
        if self.e is None:
            return str(DATE_TODAY)
        if len(str(self.e)) != DATE_LENGTH:
            raise ValueError("Ending date must be in format YYYYMMDD.")
        if int(str(self.e)) < int(str(self.b)):
            raise ValueError(
                """Ending date must be greater than or equal to the beginning
 date."""
            )
        if int(str(self.e)) > int(DATE_TODAY):
            raise ValueError(
                "Ending date must be less than or equal to the current date."
            )
        return str(self.e)

    def get_initial_aum(self) -> int:
        """
        Returns a validated initial asset under management from the user input.

        Raises:
          ValueError: If the initial asset under management is not an integer or
            is not a positive integer.

        Returns:
          int: Returns the initial asset under management if it has been 
            validated.
        """
        if self.initial_aum is None:
            raise ValueError("Initial AUM must be specified.")
        if not isinstance(self.initial_aum, int):
            raise ValueError("Initial AUM must be an integer.")
        if self.initial_aum < 0:
            raise ValueError("Initial AUM must be a positive integer.")
        return self.initial_aum

    def get_optimizer(self) -> str:
        """
        Returns a validated optimizer from the user input.

        Raises:
          ValueError: If the optimizer is not a string or is not a valid
            optimizer.

        Returns:
          str: Returns the optimizer if it has been validated.
        """
        if self.optimizer is None:
            raise ValueError("Optimizer must be specified.")
        if not isinstance(self.optimizer, str):
            raise ValueError("Optimizer must be a string.")
        if self.optimizer.lower() not in OPTIMIZERS:
            raise ValueError(
                "Optimizer must be one of the following: msr, mv, hrp"
            )
        return self.optimizer

    def get_plot_weights(self) -> bool:
        """
        Returns a validated plot_weights from the user input.

        Raises:
          ValueError: If the plot_weights is not a boolean.

        Returns:
          bool: Returns the plot_weights if it has been validated.
        """
        if self.plot_weights is None:
            raise ValueError("Plot weights must be specified.")
        return self.plot_weights
