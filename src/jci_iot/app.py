# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plots import get_updated_data, info_table2
from traces import players


def create_card(card_id, title, description):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, id=f"{card_id}-title"),
                html.H2("100", id=f"{card_id}-value"),
                html.P(description, id=f"{card_id}-description"),
            ]
        )
    )


cards = [create_card(x, "Max Acc", "4.4 m/s2") for x in range(7)]
# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


header = dbc.Row(html.Div(children=[html.H1("Training Day Dashboard")]), justify="center")
desc = dbc.Row(html.Div(children=[html.P("""Dash: A web application framework for Python.""")]), justify="center")
player_selector = dbc.Row(
    dbc.Col(
        html.Div(
            children=[dcc.Dropdown(id="player-selector", options=[{"label": i, "value": i} for i in players], value=1)]
        ),
        width={"size": 2, "offset": 5},
    )
)
table_row = dbc.Row(dbc.Col(html.Div(children=[info_table2]), width={"size": 10, "offset": 1}))

app.layout = html.Div(
    [
        header,
        desc,
        player_selector,
        table_row,
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="timeseries",
                                # figure=fig_svaHR,
                            ),
                            # html.P(id="text-1", children="First paragraph")
                        ]
                    )
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        children=[
                                            dcc.Graph(
                                                id="banded-distance",
                                                # figure=fig_banded_dis
                                            )
                                        ],
                                    )
                                ),
                                dbc.Col(
                                    html.Div(
                                        children=[
                                            dcc.Graph(
                                                id="banded-acc",
                                                # figure=fig_banded_acc
                                            )
                                        ],
                                    )
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        children=[
                                            dcc.Graph(
                                                id="distro-hr",
                                                # figure=fig_HR_dist
                                            )
                                        ],
                                    )
                                ),
                                dbc.Col(
                                    html.Div(
                                        children=[
                                            dcc.Graph(
                                                id="banded-hr",
                                                # figure=fig_banded_HR
                                            )
                                        ],
                                    )
                                ),
                            ]
                        ),
                        # dbc.Row(dbc.Col(html.Div(children=[info_table]))),
                        # dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id="g3x1", figure=fig)],)),
                        #         dbc.Col(html.Div(children=[dcc.Graph(id="g3x2", figure=fig)],))]),
                        # dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id="g4x1", figure=fig)],)),
                        #         dbc.Col(html.Div(children=[dcc.Graph(id="g4x2", figure=fig)],))]),
                    ]
                ),
            ],
            no_gutters=True,
        ),
    ]
)


@app.callback(
    Output("timeseries", "figure"),
    Output("banded-distance", "figure"),
    Output("banded-acc", "figure"),
    Output("distro-hr", "figure"),
    Output("banded-hr", "figure"),
    Input("player-selector", "value"),
)
def update_graph(player_selector_value):
    fig_svaHR, fig_banded_dis, fig_banded_acc, fig_HR_dist, fig_banded_HR = get_updated_data(player_selector_value)

    # pdf = get_player_data(player)
    # fig_svaHR = get_fig_svaHR(pdf=pdf)
    # fig_banded_dis = get_fig_banded_dis(pdf=pdf)
    # fig_banded_acc = get_fig_banded_acc(pdf=pdf)
    # fig_HR_dist = get_fig_HR_dist(pdf=pdf)
    # fig_banded_HR = get_fig_banded_HR(pdf=pdf)

    return fig_svaHR, fig_banded_dis, fig_banded_acc, fig_HR_dist, fig_banded_HR


if __name__ == "__main__":
    app.run_server(debug=True)
