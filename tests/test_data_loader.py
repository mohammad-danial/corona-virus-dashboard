import unittest
import pandas as pd
from data_loader import load_data, get_top_25_countries, aggregate_by_month


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sample_data = {
            "Date": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04"],
            "Country": ["CountryA", "CountryA", "CountryB", "CountryB"],
            "Confirmed": [10, 20, 30, 40],
            "Recovered": [1, 2, 3, 4],
            "Deaths": [0, 1, 0, 1],
        }
        self.covid_df = pd.DataFrame(self.sample_data)

    def test_load_data(self):
        # Test if the data is loaded correctly
        covid_df = load_data()
        self.assertIsInstance(covid_df, pd.DataFrame)
        self.assertIn("Country", covid_df.columns)

    def test_get_top_25_countries(self):
        # Test if the top 25 countries are selected correctly
        top_25_df = get_top_25_countries(self.covid_df)
        self.assertEqual(len(top_25_df["Country"].unique()), 2)

    def test_aggregate_by_month(self):
        # Test if the data is aggregated by month correctly
        monthly_df = aggregate_by_month(self.covid_df)
        self.assertEqual(len(monthly_df), 2)
        self.assertIn("Month", monthly_df.columns)
        self.assertIn("Country", monthly_df.columns)


if __name__ == "__main__":
    unittest.main()
