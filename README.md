# Assignment 4 - Alan, Vibilan, Jerri, Nahian

## TODO
- [x] Fix linting spaces, install autoformatter
- [x] Cleanup old requirements
- [x] Change InputData to handle new arguments
- [x] Change RunBacktest to use PyPortfolioOpt
- [x] Filter BacktestStats to produces new statistics
- [x] Update requirements
- [ ] Testing
- [ ] Documentation
- [ ] Linting

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

python -i optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20220915 --e 20230115 --initial_aum 10000 --optimizer msr

python -i optimize_portfolio.py --tickers AAPL,TGT,RTX,VOO,BA,JNJ --b 20210915 --e 20230115 --initial_aum 10000 --optimizer msr --plot_weights

python -i optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20210915 --e 20230115 --initial_aum 10000 --optimizer msr --plot_weights