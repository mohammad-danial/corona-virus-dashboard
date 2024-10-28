import os
import pandas as pd
import requests


def load_data():
    data_dir = "data"
    data_file = os.path.join(data_dir, "countries-aggregated.csv")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(data_file):
        url = (
            "https://raw.githubusercontent.com/datasets/covid-19/main/data/"
            "countries-aggregated.csv"
        )
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        with open(data_file, "w") as f:
            f.write(response.text)

    covid_df = pd.read_csv(data_file)
    return covid_df


def get_top_25_countries(covid_df):
    top_25_countries = covid_df.groupby("Country")["Confirmed"].max().nlargest(25).index
    return covid_df[covid_df["Country"].isin(top_25_countries)]


def filter_last_year(covid_df):
    covid_df["Date"] = pd.to_datetime(covid_df["Date"])
    last_year = covid_df["Date"].max() - pd.DateOffset(years=1)
    return covid_df[covid_df["Date"] > last_year]


def aggregate_by_month(covid_df):
    covid_df["Date"] = pd.to_datetime(covid_df["Date"])
    covid_df["Month"] = covid_df["Date"].dt.to_period("M")
    monthly_df = (
        covid_df.groupby(["Month", "Country"])
        .agg({"Confirmed": "sum", "Recovered": "sum", "Deaths": "sum"})
        .reset_index()
    )
    monthly_df["Date"] = monthly_df["Month"].dt.to_timestamp()
    return monthly_df
