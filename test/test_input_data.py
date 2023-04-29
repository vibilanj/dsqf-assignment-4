"""
This module is responsible for testing the functions that validate
and organise user input.
"""
import sys
import unittest

from src.input_data import DATE_TODAY, InputData, get_args

sys.path.append("/.../src")


class TestInputData(unittest.TestCase):
    """
    Defines the TestInputData class which tests the InputData class.
    """

    def test_get_normal_args(self) -> None:
        """
        Tests the get_args method with normal input.
        """
        parser = get_args()
        args = parser.parse_args(
            [
                "--tickers",
                "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD",
                "--b",
                "20220101",
                "--e",
                "20230318",
                "--initial_aum",
                "10000",
                "--optimizer",
                "msr",
                "--plot_weights"
            ]
        )
        self.assertEqual(args.tickers,
                         "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD")
        self.assertEqual(args.b, 20220101)
        self.assertEqual(args.e, 20230318)
        self.assertEqual(args.initial_aum, 10000)
        self.assertEqual(args.optimizer, "msr")
        self.assertEqual(args.plot_weights, True)

    def test_missing_args(self) -> None:
        """
        Tests the get_args method with missing input.
        """
        parser = get_args()
        self.assertRaises(SystemExit, parser.parse_args, [])

    def test_wrong_args(self) -> None:
        """
        Tests the get_args method with wrong input.
        """
        parser = get_args()
        self.assertRaises(
            SystemExit,
            parser.parse_args,
            [
                "--tickers",
                "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,HAHAHHAAH,WMT,MCD",
                "--b",
                "jjj222",
                "--e",
                "82j23i2",
                "--initial_aum",
                "alsms12",
                "--optimizer",
                "dslkfnsndfskd",
            ],
        )

    def test_get_args_optional_end_date(self) -> None:
        """
        Tests the get_args method when the optional end date is not provided.
        """
        parser = get_args()
        args = parser.parse_args(
            [
                "--tickers",
                "AAPL,TSLA",
                "--b",
                "20220101",
                "--initial_aum",
                "10000",
                "--optimizer",
                "msr"
            ]
        )
        self.assertIsNone(args.e)
        self.assertEqual(args.plot_weights, False)

    def setUp(self):
        """
        Sets up the arguments for the tests.
        """
        self.default_args = {
            "tickers": "MSFT,AMZN,WMT",
            "b": 20220101,
            "e": 20221231,
            "initial_aum": 10000,
            "optimizer": "msr",
            "plot_weights": "True"
        }

    def test_get_tickers_valid(self):
        """
        Tests the get_tickers method with valid input.
        """
        input_data = InputData(**self.default_args)
        self.assertEqual(input_data.get_tickers(), ["MSFT", "AMZN", "WMT"])

    def test_get_tickers_invalid(self):
        """
        Tests the get_tickers method with invalid input.
        """
        for invalid_tickers in [
            "",
            "MSFT,AMZN,WMT,!",
            "MSFT,AMZN,,WMT",
            None,
            12,
            "HAAAAAAAAH",
        ]:
            with self.assertRaises(ValueError):
                input_data = InputData(
                    **{**self.default_args, "tickers": invalid_tickers}
                )
                input_data.get_tickers()

    def test_get_beginning_date_valid(self):
        """
        Tests the get_beginning_date method with valid input.
        """
        input_data = InputData(**self.default_args)
        self.assertEqual(input_data.get_beginning_date(), "20220101")

    def test_get_beginning_date_invalid(self):
        """
        Tests the get_beginning_date method with invalid input.
        """
        for invalid_b in [202201, "20220101", 20982109382180382091, None]:
            with self.assertRaises(ValueError):
                input_data = InputData(**{**self.default_args, "b": invalid_b})
                input_data.get_beginning_date()

    def test_get_ending_date_valid(self):
        """
        Tests the get_ending_date method with valid input.
        """
        input_data = InputData(**self.default_args)
        self.assertEqual(input_data.get_ending_date(), "20221231")

    def test_get_ending_date_none(self):
        """
        Tests the get_ending_date method with None input.
        """
        input_data = InputData(**{**self.default_args, "e": None})
        self.assertEqual(input_data.get_ending_date(), DATE_TODAY)

    def test_get_ending_date_invalid(self):
        """
        Tests the get_ending_date method with invalid input.
        """
        for invalid_e in [20211231, "20211231", 20231231, "dabdad"]:
            with self.assertRaises(ValueError):
                input_data = InputData(**{**self.default_args, "e": invalid_e})
                input_data.get_ending_date()

    def test_get_initial_aum_valid(self):
        """
        Tests the get_initial_aum method with valid input."""
        input_data = InputData(**self.default_args)
        self.assertEqual(input_data.get_initial_aum(), 10000)

    def test_get_initial_aum_invalid(self):
        """
        Tests the get_initial_aum method with invalid input.
        """
        for invalid_aum in ["10000", -10000, None]:
            with self.assertRaises(ValueError):
                input_data = InputData(
                    **{**self.default_args, "initial_aum": invalid_aum}
                )
                input_data.get_initial_aum()

    def test_beginning_date_greater_than_today(self):
        """
        Tests the get_beginning_date method with a beginning
        date greater than today
        """
        with self.assertRaises(ValueError):
            input_data = InputData(**{**self.default_args,
                                      "b": 99990101})
            input_data.get_beginning_date()

    def test_optimizers_valid(self):
        """
        Tests the get_optimizer method with valid input.
        """
        # valid options are msr mv and hrp
        for valid_optimizers in ["msr", "mv", "hrp", "MSR", "MV", "HRP",
                                 "MsR", "Mv", "HrP"]:
            input_data = InputData(**{**self.default_args,
                                      "optimizer": valid_optimizers})
            self.assertEqual(input_data.get_optimizer(), valid_optimizers)

    def test_optimizers_invalid(self):
        """
        Tests the get_optimizer method with invalid input.
        """
        for invalid_optimizers in ["msr,ms", "173129129","ahdahaj", "#@"]:
            with self.assertRaises(ValueError):
                input_data = InputData(**{**self.default_args,
                                          "optimizer": invalid_optimizers})
                input_data.get_optimizer()

    def test_plot_weights_valid(self):
        """
        Tests the get_plot_weights method with valid input.
        """
        input_data = InputData(**self.default_args)
        self.assertEqual(input_data.get_plot_weights(), 'True')
        input_data2 = InputData(**{**self.default_args, "plot_weights": False})
        self.assertEqual(input_data2.get_plot_weights(), False)
