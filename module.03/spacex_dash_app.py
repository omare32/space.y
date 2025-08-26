from __future__ import annotations
import os
import requests
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)
DATA_LOCAL = os.path.join(os.path.dirname(__file__), "spacex_launch_dash.csv")


def load_spacex_dash(url: str = DATA_URL, local: str = DATA_LOCAL) -> pd.DataFrame:
    """Load SpaceX Dash CSV with local cache.
    Tries local file first; if missing, downloads from URL.
    """
    if os.path.exists(local):
        return pd.read_csv(local)
    # Download and save
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(local, "wb") as f:
            f.write(r.content)
    except Exception as e:
        # Fall back to direct read from URL
        try:
            return pd.read_csv(url)
        except Exception:
            raise RuntimeError(f"Failed to load dataset from {url} or local cache: {e}")
    return pd.read_csv(local)


# Load data
spacex_df = load_spacex_dash()
min_payload = int(spacex_df["Payload Mass (kg)"].min())
max_payload = int(spacex_df["Payload Mass (kg)"].max())

# Build Dash app
app = Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"

site_options = (
    [{"label": "All Sites", "value": "ALL"}]
    + [{"label": s, "value": s} for s in sorted(spacex_df["Launch Site"].unique())]
)

app.layout = html.Div([
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={"textAlign": "center", "color": "#503D36", "font-size": 40},
    ),

    # TASK 1: Dropdown for launch site selection
    dcc.Dropdown(
        id="site-dropdown",
        options=site_options,
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True,
        clearable=False,
        style={"width": "80%", "margin": "auto"},
    ),

    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id="success-pie-chart")),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Range slider for payload
    dcc.RangeSlider(
        id="payload-slider",
        min=0, max=10000, step=1000,
        value=[min_payload, max_payload],
        marks={i: str(i) for i in range(0, 10001, 2500)},
    ),

    html.Br(),

    # TASK 4: Scatter chart
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
], style={"padding": "0 25px"})


# Callback for pie chart
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value")
)
def update_pie(selected_site: str):
    if selected_site == "ALL":
        # Success count per site (class == 1)
        success_counts = (
            spacex_df.groupby("Launch Site")["class"].sum().reset_index(name="successes")
        )
        fig = px.pie(
            success_counts,
            values="successes",
            names="Launch Site",
            title="Total Success Launches by Site",
        )
        return fig
    # Specific site: success vs failure counts
    dff = spacex_df[spacex_df["Launch Site"] == selected_site]
    outcome_counts = (
        dff["class"].value_counts().rename_axis("Outcome").reset_index(name="count")
    )
    outcome_counts["Outcome"] = outcome_counts["Outcome"].map({1: "Success", 0: "Failure"})
    fig = px.pie(
        outcome_counts,
        values="count",
        names="Outcome",
        title=f"Total Launch Outcomes for {selected_site}",
        color="Outcome",
        color_discrete_map={"Success": "green", "Failure": "red"},
    )
    return fig


# Callback for scatter chart
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def update_scatter(selected_site: str, payload_range: list[int]):
    low, high = payload_range
    mask = (spacex_df["Payload Mass (kg)"] >= low) & (spacex_df["Payload Mass (kg)"] <= high)
    dff = spacex_df[mask]
    if selected_site != "ALL":
        dff = dff[dff["Launch Site"] == selected_site]

    fig = px.scatter(
        dff,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title=(
            "Correlation between Payload and Success for All Sites"
            if selected_site == "ALL"
            else f"Correlation between Payload and Success for {selected_site}"
        ),
        hover_data=["Launch Site"],
    )
    fig.update_yaxes(tickmode="array", tickvals=[0, 1], ticktext=["Failure", "Success"])
    return fig


if __name__ == "__main__":
    # Running with debug True is useful during development
    app.run(debug=True, host="127.0.0.1", port=8050)
