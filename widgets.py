import panel as pn


def create_widgets(covid_df):
    numerical_features = covid_df.select_dtypes(include=["number"]).columns.tolist()
    dist_feature = pn.widgets.Select(name="Feature", options=numerical_features)
    x_axis = pn.widgets.Select(name="X-Axis", options=covid_df.columns.tolist())
    y_axis = pn.widgets.Select(
        name="Y-Axis", options=covid_df.columns.tolist(), value="Deaths"
    )
    avg_feature = pn.widgets.Select(
        name="Average Feature", options=numerical_features, value="Confirmed"
    )
    return dist_feature, x_axis, y_axis, avg_feature


def create_buttons():
    buttons = [
        pn.widgets.Button(
            name="Introduction",
            button_type="warning",
            icon="file-info",
            styles={"width": "100%"},
        ),
        pn.widgets.Button(
            name="Dataset",
            button_type="warning",
            icon="clipboard-data",
            styles={"width": "100%"},
        ),
        pn.widgets.Button(
            name="Distribution",
            button_type="warning",
            icon="chart-histogram",
            styles={"width": "100%"},
        ),
        pn.widgets.Button(
            name="Relationship",
            button_type="warning",
            icon="chart-dots-filled",
            styles={"width": "100%"},
        ),
        pn.widgets.Button(
            name="Average Features",
            button_type="warning",
            icon="chart-bar",
            styles={"width": "100%"},
        ),
        pn.widgets.Button(
            name="Correlation",
            button_type="warning",
            icon="chart-treemap",
            styles={"width": "100%"},
        ),
        pn.widgets.Button(
            name="Geo Map",
            button_type="warning",
            icon="chart-treemap",
            styles={"width": "100%"},
        ),
    ]
    return buttons
