import dash_bootstrap_components as dbc
from dash import html
import dash

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div("Column"), style={"background": "#ff0000"}, md=6, sm=4),
        dbc.Col(html.Div("Column"), style={"background": "#ff0ff0"}, md=3, sm=4),
        dbc.Col(html.Div("Column"), style={"background": "#ffff00"}, md=3, sm=4),
    ])
])

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8051, debug=True)