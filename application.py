import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_daq as daq

import pandas as pd
import psycopg2

from names import items, champs

items = items()
champs = champs()

app = dash.Dash()
application  = app.server
app.config["suppress_callback_exceptions"] = True


suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("League of Legends Metrics [placeholder]"),
                    html.H6("Advanced analytics of League of Legends"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    )
                ],
            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="champion-tab",
                        label="Champions",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="item-tab",
                        label="Items",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )
def get_game_count():
    host = os.environ['HOST']
    user = os.environ['USER2']
    password = os.environ['PASSWORD']
    with psycopg2.connect(host=host, user=user, password=password) as conn:
        curr = conn.cursor()
        try:
            curr.execute("select count(*) from game;")
            conn.commit()
            x = curr.fetchone()
            return x
        except:
            return 0

def get_game_version():
    host = os.environ['HOST']
    user = os.environ['USER2']
    password = os.environ['PASSWORD']
    with psycopg2.connect(host=host, user=user, password=password) as conn:
        curr = conn.cursor()
        try:
            curr.execute("select gameVersion from game;")
            conn.commit()
            x = curr.fetchone()
            return x
        except:
            return 0

game_count = get_game_count()

game_version = get_game_version()

def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Total Games Sampled"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=game_count,
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=50,
                    ),
                ],
            ),
            html.Div(
                id="card-2",
                children=[
                    html.P("Patch Version"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=game_version[0][:4],
                        color="#92e0d3",
                        backgroundColor="#1e2130",
                        size=50,
                    ),
                ],
            ),
        ],
    )

def build_tab_1():
    return [
        # Manually select metrics
        html.Div(
            id="set-specs-intro-container",
            # className='twelve columns',
            children=html.P(
                "Use historical control limits to establish a benchmark, or set new values."
            ),
        ),
        html.Div(
            id="settings-menu",
            children=[
                html.Div(
                    id="metric-select-menu",
                    # className='five columns',
                    children=[
                        html.Label(id="metric-select-title", children="Select Metrics"),
                        html.Br(),
                        dcc.Dropdown(
                            id="metric-select-dropdown",
                            options=list(
                                {"label": param, "value": param} for param in params[1:]
                            ),
                            value=params[1],
                        ),
                    ],
                ),
                html.Div(
                    id="value-setter-menu",
                    # className='six columns',
                    children=[
                        html.Div(id="value-setter-panel"),
                        html.Br(),
                        html.Div(
                            id="button-div",
                            children=[
                                html.Button("Update", id="value-setter-set-btn"),
                                html.Button(
                                    "View current setup",
                                    id="value-setter-view-btn",
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(
                            id="value-setter-view-output", className="output-datatable"
                        ),
                    ],
                ),
            ],
        ),
    ]

def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### What is this app about?

                        Provides visualization of League of Legends metrics and in-depth analysis of statistics to optimize player efficiency.

                        ###### What does this app shows

                        Metrics pulled from Riot's Developer API and soon to have scikit-learn enhanced analytics.

                        ###### Notice

                        League of Legends Metrics [Placeholder] isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games
                        or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are
                        trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.


                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )
def get_playrate_and_winrate(id):
    host = os.environ['HOST']
    user = os.environ['USER2']
    password = os.environ['PASSWORD']
    with psycopg2.connect(host=host, user=user, password=password) as conn:
        curr = conn.cursor()
        try:
            curr.execute("select win.winCount, lose.loseCount from (select count(*) as winCount from participant where win = 'true' and championId = %s) as win, (select count(*) as loseCount from participant where win = 'false' and championId = %s) as lose;", (id, id))
            conn.commit()
            x = curr.fetchone()
            return (int(id), int(x[0]), int(x[1]))
        except:
            return (int(id), 0, 0)


def generate_champion_graph():
    statsList = []
    for x in champs.keys():
        curr = get_playrate_and_winrate(x)
        win_percent = 0
        if curr[2] == 0:
            win_percent = 0
        else:
            win_percent = curr[1] / (curr[2] + curr[1])
        total_games = curr[2]+curr[1]
        statsList.append((champs[x], total_games, win_percent))
    return html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=[i[1]],
                    y=[i[2]],
                    text=i[0],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i[0]
                ) for i in statsList
            ],
            'layout': go.Layout(
    width=1400,
    height=700,
                xaxis={'type': 'log', 'title': 'Pick Rate'},
                yaxis={'title': 'Winrate'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

def get_playrate_and_winrate_items(id):
    host = os.environ['HOST']
    user = os.environ['USER2']
    password = os.environ['PASSWORD']
    with psycopg2.connect(host=host, user=user, password=password) as conn:
        curr = conn.cursor()
        curr.execute("select win.winCount, lose.loseCount from (select count(*) as winCount from participant where win = 'true' and (item0 = %s or item1 = %s or item2 = %s or item3 = %s or item4 = %s or item5 = %s or item6 = %s)) as win, (select count(*) as loseCount from participant where win = 'false' and (item0 = %s or item1 = %s or item2 = %s or item3 = %s or item4 = %s or item5 = %s or item6 = %s)) as lose;", (id, id,id,id,id,id,id,id,id,id,id,id,id,id))
        conn.commit()
        x = curr.fetchone()
    return (id,x[0],x[1])
def generate_champion_items():
    statsList = []
    for x in items.keys():
        curr = get_playrate_and_winrate_items(x)
        win_percent = 0
        if curr[2] == 0:
            win_percent = 0
        else:
            win_percent = curr[1] / (curr[2] + curr[1])
        total_games = curr[2]+curr[1]
        statsList.append((items[x], total_games, win_percent))
    return html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp-items',
        figure={
            'data': [
                go.Scatter(
                    x=[i[1]],
                    y=[i[2]],
                    text=i[0],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i[0]
                ) for i in statsList
            ],
            'layout': go.Layout(
    width=1400,
    height=700,
                xaxis={'type': 'log', 'title': 'Buy Rate'},
                yaxis={'title': 'Winrate'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

preprocess_graph_champion = generate_champion_graph()
preprocess_graph_item = generate_champion_items()

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="n-interval-stage", data=50),
        generate_modal(),
    ],
)

@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}

@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                preprocess_graph_champion

            ],
        ),
        stopped_interval,
    ), stopped_interval
    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                preprocess_graph_item
            ],
        ),
        stopped_interval,
    )

# Running the server
if __name__ == "__main__":
    application.run(debug=False, port=8080)
