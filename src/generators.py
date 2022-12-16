import os

from dash import Dash, dcc, html, dash_table

try:
    from nineblock.processing import parse_team_info
except ImportError:
    from processing import parse_team_info

BASE_DATADIR = 'datasets'

def generate_datasetlist():
    os.listdir(BASE_DATADIR)
    return

def generate_groupbys():
    return [
        {"label": "Reviewer", "value": "reviewer"},
        {"label": "Role", "value": "role"},
        {"label": "Team", "value": "team"},
        {"label": "Title", "value": "title"},
    ]

def generate_employeelist():
    employeelist = [
        {"label": "Whole Team", "value": "all"}
    ]
    for line in parse_team_info():
        employeelist.append({
            "label": line['name'], "value": line['initials'].upper()
        })
    return employeelist

def generate_controls(employee='all', groupby='role'):
            # html.Div([
        #     html.Span("Dataset"),
        #     dcc.Dropdown(id="employee", options=generate_datasetlist(), value="")
        # ], id='control-employee'),
    return html.Div([
        html.Div([
            html.Span("Employee"),
            dcc.Dropdown(id="employee", options=generate_employeelist(), value=employee)
        ], id='control-employee'),
        html.Div([
            html.Span("Group By"),
            dcc.Dropdown(id="groupby", options=generate_groupbys(), value=groupby)
        ], id='control-groupby')
    ], id='controls')
