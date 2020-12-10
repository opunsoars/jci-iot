import dash_bootstrap_components as dbc


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Individual Players", href="/player-stats")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="Home",
        brand_href="/home",
        sticky="top",
    )

    return navbar
