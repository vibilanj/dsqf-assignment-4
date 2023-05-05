# Assignment 4 - Alan, Vibilan, Jerri, Nahian

## TODO
- [x] Fix linting spaces, install autoformatter
- [x] Cleanup old requirements
- [x] Change InputData to handle new arguments
- [x] Change RunBacktest to use PyPortfolioOpt
- [x] Filter BacktestStats to produces new statistics
- [x] Update requirements
- [x] Testing
- [x] Documentation
    - [x] `optimize_portfolio.py`
    - [x] `input_data.py`
    - [x] `stocks_fetcher.py`
    - [x] `run_backtest.py`
    - [x] `backtest_stats.py`
    - [x] `test_input_data.py`
    - [x] `test_stocks_fetcher.py`
    - [x] `test_run_backtest.py`
    - [x] `test_backtest_stats.py`
- [ ] Autoformat, Sort Imports and Linting
    - [x] `optimize_portfolio.py`
    - [x] `input_data.py`
    - [x] `stocks_fetcher.py`
    - [x] `run_backtest.py`
    - [x] `backtest_stats.py`
    - [ ] `test_input_data.py`
    - [ ] `test_stocks_fetcher.py`
    - [ ] `test_run_backtest.py`
    - [ ] `test_backtest_stats.py`
- [ ] Decide what the default plot type is going to be
- [ ] Delete scripts
- [ ] Update README images
- [ ] Test clean clone

## Setting up virtual environment

1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate` to activate the virtual environment. This command needs to be run **before every session**.
3. To install packages, run `pip install -r requirements.txt`.
4. For testing, you might need to deactivate and activate the virtual environment again.

### Updating environment

1. If you install new packages, run `pip freeze > requirements.txt` afterwards to update the environment requirements.

## Usage

### Portfolio Optimization

To optimize a portfolio based on the stock universe containing MSFT, WMT, LMT, SPY, GM, PG from September 15, 2022 to January 15, 2023 with an initial AUM of 10000 and using the Maximum Sharpe Ratio (MSR) optimizer, run the following:

* `python -i optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20220915 --e 20230115 --initial_aum 10000 --optimizer msr`

To optimize a portfolio and plot the portfolio weights based on the stock universe containing MSFT, WMT, LMT, SPY, GM, PG from June 1, 2022 to today with an initial AUM of 10000 and using the Hierarchical Risk Parity (HRP) optimizer, run the following: 

* `python -i optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20220601 --initial_aum 10000 --optimizer hrp --plot_weights`

### Note

The plot filenames can be specified but default to `portfolio_weights`. The plot type can also be specified (`line`, `stacked_bar`, `stacked_area` or `pies` ) but default to `line`.

## Unit Tests

Run the unit tests using the following command:

* `pytest -vv`

To see the code coverage report, run the following command:

1. `coverage run -m pytest`
2. `coverage report`

## Project Accomplishments

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


python -i optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20220915 --e 20230115 --initial_aum 10000 --optimizer msr