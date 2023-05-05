# Assignment 4 - Alan, Vibilan, Jerri, Nahian

## Setting up virtual environment

1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate` to activate the virtual environment. This command needs to be run **before every session**.
3. To install packages, run `pip install -r requirements.txt`.
4. For testing, you might need to deactivate and reactivate the virtual environment.

### Updating environment

1. If you install new packages, run `pip freeze > requirements.txt` afterwards to update the environment requirements.

## Usage

### Portfolio Optimization

To optimize a portfolio based on the stock universe containing MSFT, WMT, LMT, SPY, GM, PG from September 15, 2022 to January 15, 2023 with an initial AUM of 10000 and using the Maximum Sharpe Ratio (MSR) optimizer, run the following:

* `python optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20220915 --e 20230115 --initial_aum 10000 --optimizer msr`

To optimize a portfolio and plot the portfolio weights based on the stock universe containing MSFT, WMT, LMT, SPY, GM, PG from June 1, 2022 to today with an initial AUM of 10000 and using the Hierarchical Risk Parity (HRP) optimizer, run the following: 

* `python optimize_portfolio.py --tickers MSFT,WMT,LMT,SPY,GM,PG --b 20220601 --initial_aum 10000 --optimizer hrp --plot_weights`

### Note

The plot filenames can be specified but defaults to `portfolio_weights`. The plot type can also be specified (`line`, `stacked_bar`, `stacked_area` or `pies`) but defaults to `line`.

## Unit Tests

Run the unit tests using the following command:

* `pytest -vv`

To see the code coverage report, run the following command:

1. `coverage run -m pytest`
2. `coverage report`

### Note

There might be an issue with `pytest` or `coverage` unable to find certain modules. If it happens, try deactivating and reactivating the virtual environment.

## Project Accomplishments

1. Produces the correct analytics and plot
2. Code coverage of the project is 99%
3. Functions have been tested for multiple scenarios
4. Functions have been correctly typed

Screenshot of pytest results of the project:

![screenshot-2023-05-05-15:41:56](https://user-images.githubusercontent.com/61618719/236402452-48e374e6-248a-4839-b617-a65858b0f3c2.png)

Screenshot of code coverage report of the project:

![screenshot-2023-05-05-15:42:17](https://user-images.githubusercontent.com/61618719/236402473-d2a03f93-0886-4431-b978-2f2d0a5f5b2d.png)

## Issues

We noticed that for some inputs, there is the possibility that a `ValueError: at least one of the assets must have an expected return exceeding the risk-free rate` is raised. An example is with the following parameters:

`python optimize_portfolio.py --tickers MSFT,WMT,GM --b 20220101 --e 20230101 --initial_aum 10000 --optimizer msr`

This error arises because the portfolio optimization algorithm requires that at least one asset in the portfolio has an expected return greater than the risk-free rate to justify taking on additional risk. If none of the assets in the portfolio have expected returns exceeding the risk-free rate, the optimization algorithm will be unable to identify a meaningful allocation that improves the risk-return tradeoff. To resolve this issue, the analysis period could be extended, risk-free rate can be adjusted from the default of 0.02, and other assets with potentially higher expected returns can be included in the portfolio
