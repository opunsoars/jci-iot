import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar

nav = Navbar()

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("About"),
                        dcc.Markdown(
                            """\
                            Developed for an assignment in the course **Data Analytics in Sport** by **Vinay Warrier**. \n
                            This course is taught by Luca Spinelli at [*Johan Cruyff Institute*](https://johancruyffinstitute.com/en/).

                            Nov-Dec 2020\n

                            Find me <@opunsoars>:
                            [Twitter](http://www.twitter.com/opunsoars) | [Github](https://github.com/opunsoars) | [LinkedIn](https://www.linkedin.com/in/opunsoars/)
                            
                            
                            
                            
                            
                            """
                        ),
                        # dbc.Button("View details", color="secondary"),
                    ],
                    # md=4,
                ),
                # dbc.Col(
                #     [
                #         html.H2("Graph"),
                #         dcc.Graph(figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}),
                #     ]
                # ),
            ]
        )
    ],
    # className="mt-4",
)


def About():
    layout = html.Div([nav, body])

    return layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = About()

if __name__ == "__main__":
    app.run_server()