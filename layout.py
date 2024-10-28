import panel as pn
from charts import (
    create_hist,
    create_scatter_chart,
    create_bar_chart,
    create_corr_heatmap,
    create_geo_map,
)
import os


def create_pages(
    covid_df,
    top_25_df,
    dist_feature,
    x_axis,
    y_axis,
    avg_feature,
    last_year_df,
    monthly_df,
):
    # Save the monthly aggregated data to a CSV file
    if not os.path.exists("data"):
        os.makedirs("data")
    monthly_df.to_csv("data/monthly.csv", index=False)

    def create_intro_page():
        descr = """
        ## Introduction

        This dashboard provides an overview of the COVID-19 pandemic using various
        visualizations. You can navigate through different sections using the sidebar
        to explore the data in detail.
        """
        return pn.Column(
            pn.pane.Markdown(descr, styles={"font-size": "14pt"}), align="center"
        )

    def create_dataset_page():
        descr = """
        ## Dataset Explorer

        This section allows you to explore the first 50 rows of the dataset.
        """
        return pn.Column(
            pn.pane.Markdown(descr, styles={"font-size": "14pt"}),
            pn.pane.DataFrame(covid_df.head(50), height=450, width=850),
            align="center",
        )

    def create_distribution_page():
        descr = """
        ## Explore Distribution of Features

        This section allows you to explore the distribution of various features in the
        dataset.
        """
        return pn.Column(
            pn.pane.Markdown(descr, styles={"font-size": "14pt"}),
            dist_feature,
            pn.bind(create_hist, monthly_df, dist_feature),
            align="center",
        )

    def create_relationship_page():
        descr = """
        ## Explore Relationship Between Features

        This section allows you to analyze the relationship between different features
        in the dataset.
        """
        top_25_monthly_df = monthly_df[monthly_df["Country"].isin(top_25_df["Country"])]
        return pn.Column(
            pn.pane.Markdown(descr, styles={"font-size": "14pt"}),
            pn.Row(x_axis, y_axis),
            pn.bind(create_scatter_chart, top_25_monthly_df, x_axis, y_axis),
            align="center",
        )

    def create_avg_features_page():
        descr = """
        ## Explore Avg Values of Features per Month (Last Year, Aggregated by Month)

        This section allows you to view the average values of features per month.
        """
        return pn.Column(
            pn.pane.Markdown(descr, styles={"font-size": "14pt"}),
            avg_feature,
            pn.bind(create_bar_chart, monthly_df, avg_feature),
            align="center",
        )

    def create_correlation_page():
        descr = """
        ## Features Correlation Heatmap

        This section provides a heatmap showing the correlation between different
        features in the dataset.
        """
        return pn.Column(
            pn.pane.Markdown(descr, styles={"font-size": "14pt"}),
            create_corr_heatmap(monthly_df),
            align="center",
        )

    def create_geo_map_page():
        descr = """
        ## Geospatial Map of Accumulated Deaths

        This section provides a geospatial map showing the accumulated deaths across
        different countries.
        """
        return pn.Column(
            pn.pane.Markdown(descr, styles={"font-size": "14pt"}),
            create_geo_map(covid_df),
            align="center",
        )

    return {
        "IntroPage": create_intro_page,
        "DatasetPage": create_dataset_page,
        "DistributionPage": create_distribution_page,
        "RelationshipPage": create_relationship_page,
        "AvgFeaturesPage": create_avg_features_page,
        "CorrelationPage": create_correlation_page,
        "GeoMapPage": create_geo_map_page,
    }


def create_layout(pages, buttons):
    sidebar = pn.Column(*buttons, styles={"width": "80%"})
    main_area = pn.Column(pages["IntroPage"](), styles={"width": "100%"})
    return sidebar, main_area
