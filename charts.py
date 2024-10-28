import hvplot.pandas  # noqa: F401
import geopandas as gpd
import geoviews as gv  # noqa: F401
import requests
import tempfile
import zipfile
import pandas as pd


def create_hist(covid_df, sel_feature):
    return covid_df.hvplot.hist(y=sel_feature, bins=50, height=600, width=1200).opts(
        active_tools=[]
    )


def create_scatter_chart(covid_df, x_axis, y_axis):
    # Ensure the Country column is present
    if "Country" not in covid_df.columns:
        raise ValueError("The 'Country' column is not present in the DataFrame.")

    return covid_df.hvplot.scatter(
        x=x_axis, y=y_axis, size=100, alpha=0.9, rot=45, height=600, width=1200
    ).opts(active_tools=[])


def create_bar_chart(covid_df, sel_col):
    return covid_df.hvplot.bar(
        x="Date", y=sel_col, bar_width=0.5, rot=45, height=600, width=1200, color="blue"
    ).opts(
        active_tools=[],
        tools=["hover"],
        hover_fill_color="red",
        hover_fill_alpha=0.7,
        hover_line_color="white",
        hover_line_width=2,
        hover_line_alpha=1.0,
        hover_tooltips=[("Value", "@{sel_col}")]
    )


def create_corr_heatmap(covid_df):
    numeric_df = covid_df.select_dtypes(include=["number"])
    covid_corr = numeric_df.corr()
    return covid_corr.hvplot.heatmap(cmap="Blues", rot=45, height=600, width=1200).opts(
        active_tools=[]
    )


def create_geo_map(covid_df):
    url = (
        "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    )
    response = requests.get(url)
    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpfile.write(response.content)
        tmpfile.flush()
        with zipfile.ZipFile(tmpfile.name, "r") as zip_ref:
            zip_ref.extractall("data/naturalearth_lowres")
    world = gpd.read_file("data/naturalearth_lowres/ne_110m_admin_0_countries.shp")

    # Fix country name mismatches
    covid_df["Country"] = covid_df["Country"].replace(
        {
            "Burma": "Myanmar",
            "Taiwan*": "Taiwan",
            "US": "United States of America",
            "Congo (Brazzaville)": "Congo",
            "Congo (Kinshasa)": "Dem. Rep. Congo",
        }
    )

    # Ensure the dataset is sorted correctly by date
    covid_df["Date"] = pd.to_datetime(covid_df["Date"])
    covid_df = covid_df.sort_values("Date")

    # Get the last confirmed number of deaths for each country
    last_deaths = covid_df.groupby("Country").last().reset_index()

    # Save the result as a CSV file
    last_deaths.to_csv("countries_latest_confirmed.csv", index=False)

    world = world.merge(last_deaths, how="left", left_on="NAME", right_on="Country")
    world = world.fillna(0)
    return world.hvplot.polygons(
        "geometry",
        hover_cols=["NAME", "Deaths"],
        color="Deaths",
        cmap="Reds",
        height=600,
        width=1200,
        tools=["hover"],
        hover_formatters={"@Deaths": "numeral"},
    )
