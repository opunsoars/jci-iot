import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px

import dash_html_components as html
from dash.dependencies import Input, Output

from app import App
from homepage import Homepage
from about import About
from plots import get_updated_data, player_aggs

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([dcc.Location(id="url", refresh=False), html.Div(id="page-content")])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/player-stats":
        return App()
    elif pathname == "/about":
        return About()
    else:
        return Homepage()


# @app.callback(Output("output", "children"), [Input("pop_dropdown", "value")])
# def update_graph(city):
#     graph = build_graph(city)
#     return graph


@app.callback(
    Output("timeseries", "figure"),
    Output("banded-distance", "figure"),
    Output("banded-acc", "figure"),
    Output("distro-hr", "figure"),
    Output("banded-hr", "figure"),
    Output("df", "children"),
    Output("player-card", "children"),
    Input("player-selector", "value"),
)
def update_graph(player_selector_value):
    fig_svaHR, fig_banded_dis, fig_banded_acc, fig_HR_dist, fig_banded_HR, info_table2 = get_updated_data(
        player_selector_value
    )
    card = player_selector_value

    return fig_svaHR, fig_banded_dis, fig_banded_acc, fig_HR_dist, fig_banded_HR, info_table2, card


@app.callback(
    Output("scatters", "figure"),
    Input("xcol", "value"),
    Input("ycol", "value"),
    # Input('xaxis-type', 'value'),
    # Input('yaxis-type', 'value'),
    # Input('year--slider', 'value')
)
def update_graph(
    xcol_value,
    ycol_value,
    #  xaxis_type, yaxis_type,year_value
):
    fig = px.scatter(
        x=player_aggs[xcol_value],
        y=player_aggs[ycol_value],
        hover_name=player_aggs["player_id"].apply(lambda x: f"P{x}"),
        trendline="ols"
    )

    # dff = df[df['Year'] == year_value]

    # fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
    #                  y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
    #                  hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_layout(
        margin={"l": 0, "b": 0, "t": 10, "r": 0},
        hovermode="closest"
    )

    fig.update_xaxes(title=xcol_value,
                    #  type='linear' if xaxis_type == 'Linear' else 'log'
                     )

    fig.update_yaxes(title=ycol_value,
                    #  type='linear' if yaxis_type == 'Linear' else 'log'
                     )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
