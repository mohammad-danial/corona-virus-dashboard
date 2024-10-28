import panel as pn
import warnings
from data_loader import (
    load_data,
    get_top_25_countries,
    filter_last_year,
    aggregate_by_month,
)
from widgets import create_widgets, create_buttons
from layout import create_pages, create_layout

warnings.filterwarnings("ignore")


def main():
    # Load data
    covid_df = load_data()
    top_25_df = get_top_25_countries(covid_df)
    last_year_df = filter_last_year(covid_df)
    monthly_df = aggregate_by_month(last_year_df)

    # Create widgets
    dist_feature, x_axis, y_axis, avg_feature = create_widgets(covid_df)

    # Create buttons
    buttons = create_buttons()

    # Create pages
    pages = create_pages(
        covid_df,
        top_25_df,
        dist_feature,
        x_axis,
        y_axis,
        avg_feature,
        last_year_df,
        monthly_df,
    )

    # Create layout
    sidebar, main_area = create_layout(pages, buttons)

    # Set fixed width and height for main_area and sidebar
    sidebar.width = 250
    main_area.height = 800

    # Button callbacks
    def show_page(page_key):
        main_area.clear()
        main_area.append(pages[page_key]())

    buttons[0].on_click(lambda event: show_page("IntroPage"))
    buttons[1].on_click(lambda event: show_page("DatasetPage"))
    buttons[2].on_click(lambda event: show_page("DistributionPage"))
    buttons[3].on_click(lambda event: show_page("RelationshipPage"))
    buttons[4].on_click(lambda event: show_page("AvgFeaturesPage"))
    buttons[5].on_click(lambda event: show_page("CorrelationPage"))
    buttons[6].on_click(lambda event: show_page("GeoMapPage"))

    # Create and serve the Panel app
    template = pn.template.BootstrapTemplate(
        title="COVID-19 Dashboard",
        sidebar=[sidebar],
        main=[main_area],
        site="COVID-19 Data",
        logo="cc.png",
        theme=pn.template.DarkTheme,
        sidebar_width=250,
        busy_indicator=None,
    )

    template.servable()
    pn.serve(template)


if __name__ == "__main__":
    main()
