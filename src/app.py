#!/usr/bin/env python

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# import dash
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

try:
    from nineblock.processing import get_dataset
    from nineblock.generators import generate_controls
except ImportError:
    from processing import get_dataset
    from generators import generate_controls

app = Dash(__name__)

@app.callback(
    Output("nineblock", "children"),
    [Input("employee", "value"), Input("groupby", "value")]
)
def show_data(employee, groupby):
    (dataset, groupby, tablecolumns) = get_dataset(employee, groupby)
    
    fig = px.scatter(
        dataset,
        y="capability",
        x="performance",
        color=groupby,
        size='size',
        hover_data={
          groupby: False,
          'matches': True,
          'size': False
        },
        range_x=[-0.5, 9.5],
        range_y=[-0.5, 9.5],
        width=1200,
        height=1200,
    )

    fig.update_layout(
        xaxis=dict(tickmode="array", tickvals=[0, 3, 6, 9], ticktext=[0, 3, 6, 9]),
        yaxis=dict(tickmode="array", tickvals=[0, 3, 6, 9], ticktext=[0, 3, 6, 9]),
    )

    graph = dcc.Graph(id="graph", figure=fig)

    table = dash_table.DataTable(
        id="summary",
        columns=[
            {"name": i, "id": i} for i in tablecolumns
        ],
        data=dataset.to_dict("records"),
        style_as_list_view=True,
    )

    sidebar = html.Div([table,generate_controls(employee, groupby)], id='sidebar')


    return [graph, sidebar]


app.layout = html.Div(
    children=[
        html.H1(children="9 Block Visualization"),
        html.Div(children=generate_controls(), id="nineblock"),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
