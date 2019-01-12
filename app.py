import px
import pandas
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

tips = pandas.read_csv("https://plotly.github.io/datasets/tips.csv")
col_options = [dict(label=x, value=x) for x in tips.columns]

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Dropdown(id="x", options=col_options, placeholder="x"),
        dcc.Dropdown(id="y", options=col_options, placeholder="y"),
        dcc.Dropdown(id="color", options=col_options, placeholder="color"),
        dcc.Dropdown(id="col", options=col_options, placeholder="col"),
        dcc.Dropdown(id="row", options=col_options, placeholder="row"),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    Output("graph", "figure"),
    [
        Input("x", "value"),
        Input("y", "value"),
        Input("color", "value"),
        Input("col", "value"),
        Input("row", "value"),
    ],
)
def cb(x, y, color, col, row):
    return px.scatter(tips, x=x, y=y, color=color, col=col, row=row)


app.run_server(debug=True)
