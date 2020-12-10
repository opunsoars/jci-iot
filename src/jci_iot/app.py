import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from plots import players


nav = Navbar()
header = html.H3("Individual player dashboard", style={"text-align": "center"})
player_selector = dbc.Row(
    dbc.Col(
        html.Div(
            children=[
                dcc.Dropdown(
                    id="player-selector",
                    options=[{"label": i, "value": i} for i in players],
                    value=1,
                    placeholder="Select a player",
                )
            ]
        ),
        width={"size": 2, "offset": 5},
    )
)

player_card = dbc.Col(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Player"),
                    html.H2(id="player-card"),
                ]
            ),
            color="dark",
            inverse=True,
            style={"height": "90%"},
        )
    ],
    width={"size": 1},
)

table_row = dbc.Col(
    html.Div(id="df"),
)


def App():
    layout = html.Div(
        [
            nav,
            header,
            player_selector,
            dbc.Row([player_card, table_row], no_gutters=True),
            # table_row,
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            children=[
                                dcc.Graph(id="timeseries"),
                            ]
                        )
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(children=[dcc.Graph(id="banded-distance")])),
                                    dbc.Col(
                                        html.Div(
                                            children=[dcc.Graph(id="banded-acc")],
                                        )
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            children=[dcc.Graph(id="distro-hr")],
                                        )
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            children=[dcc.Graph(id="banded-hr")],
                                        )
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
                no_gutters=True,
            ),
        ]
    )
    return layout


# def build_graph(city):
#     data = [go.Scatter(x=df.index, y=df[city], marker={"color": "orange"})]
#     graph = dcc.Graph(
#         figure={
#             "data": data,
#             "layout": go.Layout(
#                 title="{} Population Change".format(city), yaxis={"title": "Population"}, hovermode="closest"
#             ),
#         }
#     )
#     return graph
