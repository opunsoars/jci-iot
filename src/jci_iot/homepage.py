import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from navbar import Navbar
from plots import available_indicators
from traces import fig_agg_distance, fig_agg_hr, fig_agg_hr_bands, fig_agg_speed

nav = Navbar()
header = html.H3("Training Session Dashboard", style={"text-align": "center"})
body = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Div(dcc.Graph(figure=fig_agg_distance, id="agg-distance"))),
                        dbc.Col(html.Div(dcc.Graph(figure=fig_agg_speed, id="agg-speed"))),
                    ],
                    no_gutters=True,
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(dcc.Graph(figure=fig_agg_hr, id="agg-hr"))),
                        dbc.Col(html.Div(dcc.Graph(figure=fig_agg_hr_bands, id="agg-hr-bands"))),
                    ],
                    no_gutters=True,
                ),
            ],  # width=7
        ),
        dbc.Col(
            # player pick | xaxis col | yaxis col | reset
            [
                html.P("Select the X and Y axes metrics to compare across players"),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="xcol",
                                    options=[{"label": i, "value": i} for i in available_indicators],
                                    value="Distance[km]",
                                ),
                                # dcc.RadioItems(
                                #     id="xaxis-type",
                                #     options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
                                #     value="Linear",
                                #     labelStyle={"display": "inline-block"},
                                # ),
                            ],
                            style={"width": "48%", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="ycol",
                                    options=[{"label": i, "value": i} for i in available_indicators],
                                    value="#sprints_[25+ km/h]",
                                ),
                                # dcc.RadioItems(
                                #     id="yaxis-type",
                                #     options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
                                #     value="Linear",
                                #     labelStyle={"display": "inline-block"},
                                # ),
                            ],
                            style={
                                "width": "45%",
                                "float": "right",
                                "display": "inline-block",
                            },
                        ),
                    ]
                ),
                html.Div(dcc.Graph(id="scatters"), style={"margin-right": "10px"}),
                html.Div(
                    dcc.Markdown(
                        """
                            Total number of players in session: 9\n
                            #16 did not attend second half of the session.\n
                            #10 leads with most distance covered, highest mean heart rate, and number of sprints.\n
                            Check out individual player dashboards via the navigation bar.


                            """
                    )
                )
            ],
        ),
    ]
)


def Homepage():
    layout = html.Div([nav, header, body])

    return layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = Homepage()


if __name__ == "__main__":
    app.run_server()
