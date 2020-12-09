# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from plots import fig_svaHR,fig_banded_dis, fig_banded_acc, fig_HR_dist, fig_banded_HR


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
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig.update_layout(height=300, width=400)


app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.H1("Training Day Dashboard"),
                    ],
                    className="row",
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.P(
                            """
                            Dash: A web application framework for Python.
                            """
                        )
                    ],
                    className="row",
                )
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="example-graph1",
                                figure=fig_svaHR,
                                ),
                            # html.P(id="text-1", children="First paragraph")
                            ])),
                dbc.Col(
                    [
                        dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id="g1x1", figure=fig_banded_dis)],)),
                                dbc.Col(html.Div(children=[dcc.Graph(id="g1x2", figure=fig_banded_acc)],))]),
                        dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id="g2x1", figure=fig_HR_dist)],)),
                                dbc.Col(html.Div(children=[dcc.Graph(id="g2x2", figure=fig_banded_HR)],))]),
                        dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id="g3x1", figure=fig)],)),
                                dbc.Col(html.Div(children=[dcc.Graph(id="g3x2", figure=fig)],))]),
                        # dbc.Row([dbc.Col(html.Div(children=[dcc.Graph(id="g4x1", figure=fig)],)),
                        #         dbc.Col(html.Div(children=[dcc.Graph(id="g4x2", figure=fig)],))]),
                    ]
                ),
            ]
        ),
    ]
)

# app.layout = html.Div(

#     html.H1(
#         children='Hello Dash',
#         style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}
#     ),
#     html.Div(
#         children='''
#                     Dash: A web application framework for Python.
#                 ''',
#         style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}
#     ),
#     dcc.Graph(
#         id='example-graph',
#         figure=fig_svaHR,

#     ),
# )

# applayout = html.Div(
#     [
#         # row,
#         # row 1 - title
#         dbc.Row(
#             dbc.Col(
#                 html.Div(
#                     children=[
#                         html.H1("Training Day Dashboard"),
#                     ],
#                     className="row",
#                 )
#             )
#         ),
#         # row 2 - description
#         dbc.Row(
#             dbc.Col(
#                 html.Div(
#                     children=[
#                         html.Div(
#                             """
#                         Dash: A web application framework for Python.
#                     """
#                         ),
#                     ],
#                     className="row",
#                 )
#             )
#         ),
#         # row 3
#         #   row 3.1 inline - subplots
#         html.Div(
#             children=[
#                 html.Div(
#                     children=[
#                         dcc.Graph(
#                             id="example-graph1",
#                             figure=fig_svaHR,
#                         ),
#                         html.P(id="text-1", children="First paragraph"),
#                     ],
#                     # style={
#                     #     "display": "inline-block",
#                     #     "vertical-align": "top",
#                     #     "margin-left": "3vw",
#                     #     "margin-top": "3vw",
#                     # },
#                 ),
#                 #   row 3.2 inline - 4x2 grid of plots
#                 html.Div(
#                     children=[
#                         # 4 rows 2 cols
#                         # row 3.2.1
#                         html.Div(
#                             children=[
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-1-1", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-1-2", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                             ],
#                         ),
#                         # row 3.2.2
#                         html.Div(
#                             children=[
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-2-1", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-2-2", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                             ],
#                         ),
#                         # row 3.2.3
#                         html.Div(
#                             children=[
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-3-1", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-3-2", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                             ],
#                         ),
#                         # row 3.2.4
#                         html.Div(
#                             children=[
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-4-1", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                                 html.Div(
#                                     children=[dcc.Graph(id="grid-plot-3-2-4-2", figure=fig)],
#                                     style={
#                                         "display": "inline-block",
#                                         "vertical-align": "top",
#                                         "margin-left": "3vw",
#                                         "margin-top": "3vw",
#                                     },
#                                 ),
#                             ],
#                         ),
#                         # dcc.Graph(
#                         #     id="example-graph2",
#                         #     figure=fig_svaHR,
#                         # ),
#                         html.P(id="text-2", children="Second paragraph"),
#                     ],
#                     style={
#                         "display": "inline-block",
#                         "vertical-align": "top",
#                         "margin-left": "3vw",
#                         "margin-top": "3vw",
#                     },
#                 ),
#             ],
#             style={
#                         "display": "inline-block",
#                         "vertical-align": "top",
#                         "margin-left": "3vw",
#                         "margin-top": "3vw",
#                     }
#         ),
#     ]
# )

# l2 = html.Div(
#     [
#         # first row
#         html.Div(
#             children=[
#                 # first column of first row
#                 html.Div(
#                     children=[
#                         dcc.RadioItems(
#                             id="radio-item-1",
#                             options=[
#                                 dict(label="option A", value="A"),
#                                 dict(label="option B", value="B"),
#                                 dict(label="option C", value="C"),
#                             ],
#                             value="A",
#                             labelStyle={"display": "block"},
#                         ),
#                         html.P(id="text-1", children="First paragraph"),
#                     ],
#                     style={
#                         "display": "inline-block",
#                         "vertical-align": "top",
#                         "margin-left": "3vw",
#                         "margin-top": "3vw",
#                     },
#                 ),
#                 # second column of first row
#                 html.Div(
#                     children=[
#                         dcc.RadioItems(
#                             id="radio-item-2",
#                             options=[
#                                 dict(label="option 1", value="1"),
#                                 dict(label="option 2", value="2"),
#                                 dict(label="option 3", value="3"),
#                             ],
#                             value="1",
#                             labelStyle={"display": "block"},
#                         ),
#                         html.P(id="text-2", children="Second paragraph"),
#                     ],
#                     style={
#                         "display": "inline-block",
#                         "vertical-align": "top",
#                         "margin-left": "3vw",
#                         "margin-top": "3vw",
#                     },
#                 ),
#                 # third column of first row
#                 html.Div(
#                     children=[
#                         html.Div(dcc.Graph(id="main-graph", figure=figure)),
#                     ],
#                     style={
#                         "display": "inline-block",
#                         "vertical-align": "top",
#                         "margin-left": "3vw",
#                         "margin-top": "3vw",
#                     },
#                 ),
#             ],
#             className="row",
#         ),
#         # second row
#         html.Div(
#             children=[
#                 html.Div(
#                     dash_table.DataTable(
#                         id="main-table",
#                         columns=[{"name": i, "id": i} for i in df.columns],
#                         data=df.to_dict("records"),
#                         style_table={"margin-left": "3vw", "margin-top": "3vw"},
#                     )
#                 ),
#             ],
#             className="row",
#         ),
#     ]
# )

if __name__ == "__main__":
    app.run_server(debug=True)