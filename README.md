# Assignment 4 - Alan, Vibilan, Jerri, Nahian

## TODO
- [x] Fix linting spaces, install autoformatter
- [x] Cleanup old requirements
- [x] Change InputData to handle new arguments
- [x] Change RunBacktest to use PyPortfolioOpt
- [x] Filter BacktestStats to produces new statistics
- [ ] Update requirements
- [ ] Testing
- [ ] Documentation
- [ ] Linting

## run_backtest.py
1. parameters: DONE
   1. stocks_data: pd.DataFrame, 
   2. initial_aum: int, 
   3. beginning_date: str, 
   4. optimizer: str
2. attributes: DONE
   1. self.stocks_data: pf.DataFrame
   2. self.initial_aum: int,
   3. self.beginning_date: str
   4. self.portfolio_performance: pd.DataFrame 
      1. Date starting from first month end to ending date
      2. AUM
   5. self.portfolio: List[Tuple[str, float]]
   6. self.portfolio_record: List[List[Tuple[str, float]]]
   7. self.month_end_indexes: List[int]
3. methods
   1. init_portfolio_performance(self) -> None DONE
   2. get_month_end_indexes_from_b(self) -> List[int] DONE
   3. calc_aum(self, date_index: int) -> float
   4. update_portfolio(self, date_index: int, optimizer) -> List[Tuple[str, float]]
      1. df = self.stocks_date[date_index - 250, date_index]
      2. if optimizer is "msr" or "mv":
         1. mu = expected_returns.mean_historical_return(df)
         2. S = risk_models.sample_cov(df)
         3. model = EfficientFrontier(mu, S)
         4. weights = 
            1. model.max_sharpe(), or
            2. model.min_volatility()
      3. else if it is "hrp":
         1. model = HRPOpt(df)
         2. model.optimize()
         3. weights = model.clean_weights()
         4. model.portfolio_performance(verbose=True)
      4. else:
         1. raise exception
      5. update_portfolio
         1. append weights to self.portfolio_record
      6. TODO: update portfolio_performance with annual volatility etc check if needs to be kept in some dataframe
   5. fill_up_portfolio_performance(self) -> None
      1. loop through Date starting from the first month end index to the ending date
      2. calculate the aum at that date and update self.portfolio_performance
         1. self.calc_aum(date_index)
      3. if the date is a month end index, rebalance:
         1. self.update_portfolio()
      4. cut portfolio performance to only start from from the first end of month

## Testing steps
1. run test/test_month.py based on the index required on google sheets (e.g. 309 for first rebalancing)
2. take note of the weights printed and transfer them to google sheets
3. To rebalance:
   1. calculate the temporary aum from the previous day portfolio and today's stock price
   2. using the temporary aum and the weights, calculate the new portfolio
   3. copy the portfolio until a day before the next rebalancing day

## Setting up virtual environment (recommended)

1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate` to activate the virtual environment. This command needs to be run **before every session**.

## Direction of use

1. To install packages, run `pip install -r requirements.txt`.

## Updating environment

1. If you install new packages, run `pip freeze > requirements.txt` afterwards to update the environment requirements.

## Usage

### Backtesting Strategy

To backtest a linear combination of 1) momentum strategy with 60 days, and 2) reversal strategy with 30 days, with an initial AUM of 10000, and on the top 10% of the stock universe containing AAPL, TSLA, LMT, BA, GOOG, AMZN, NVDA, META, WMT, MCD from January 1, 2022 to January 1, 2023, run the following: 

* `python backtest_two_signal_strategy.py --tickers AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD --b 20220101 --e 20230101 --initial_aum 10000 --strategy1_type M --days1 60 --strategy2_type R --days2 30 --top_pct 10`

To backtest a linear combination of 1) reversal strategy with 10 days, and 2) momentum strategy with 40 days, with an initial AUM of 10000, and on the top 20% of the stock universe containing AAPL, TSLA, LMT, BA, GOOG, AMZN, NVDA, META, WMT, MCD from June 1, 2022 to today run the following: 

* `python backtest_two_signal_strategy.py --tickers AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD --b 20220601 --initial_aum 10000 --strategy1_type R --days1 10 --strategy2_type M --days2 40 --top_pct 20`

### Note

The plot filenames can be specified but default to `daily_aum.png` and `cumulative_ic.png`.

### Unit Tests

Run the unit tests using the following command:

* `pytest -vv`

To see the code coverage report, run the following command:

1. `coverage run -m pytest`
2. `coverage report`

### Project Accomplishments

1. Produces the correct analytics and plot
2. Code coverage of the project is 99%
3. Functions have been tested for multiple scenarios
4. Functions have been correctly typed

Screenshot of pytest results of the project:

![screenshot-2023-04-16-22:41:38](https://user-images.githubusercontent.com/61618719/232320678-3178ae53-d758-46fb-b245-ad3ee802e5f5.png)

Screenshot of code coverage report of the project:

![screenshot-2023-04-16-22:42:09](https://user-images.githubusercontent.com/61618719/232320687-6ded09ee-e30b-4d49-a783-56b0762b579e.png)

python -i optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20220101 --e 20230101 --initial_aum 10000 --optimizer msr