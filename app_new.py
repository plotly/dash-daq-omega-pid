import time
import datetime
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import State, Input, Output
import plotly.graph_objs as go
import random
import minimalmodbus
app = dash.Dash(__name__)

server = app.server
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True


def rgb_convert_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

# ser = minimalmodbus.Instrument('COM4', 1, mode='rtu')


# CSS Imports
external_css = ["https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://cdn.rawgit.com/matthewchan15/dash-css-style-sheets/adf070fa/banner.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})


app.layout = html.Div(
    [
        html.Div(
            id="container",
            style={"background-color": "#119DFF"},

            children=[
                html.H2(
                    "Dash DAQ: Omega Platnium Controller",
                ),
                html.A(
                    html.Img(
                        src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/excel/dash-daq/dash-daq-logo-by-plotly-stripe+copy.png",
                    ),
                    href="http://www.dashdaq.io"
                )

            ],
            className="banner"
        ),
        html.Div(
            [
                html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                daq.Indicator(
                                    id="graph-on-off",
                                    label="",
                                    value=True,
                                    color="#00cc96",
                                    className="one columns",
                                    labelPosition="top",
                                    style={"position": "absolute",
                                           "left": "20%", "top": "33%"}
                                ),
                                html.H4(
                                    "Temperature vs. Time Graph",
                                    className=" three columns",
                                    style={"textAlign": "center",
                                           "width": "41%"}
                                ),
                                daq.StopButton(
                                    id="reset-button",
                                    buttonText="Reset",
                                    style={"display": "flex",
                                               "justify-content": "center",
                                               "align-items": "center",
                                               "width": "10%"},
                                    n_clicks=0,
                                    className="three columns"
                                ),
                            ], className="row", style={"marginTop": "1%",
                                                       "marginBottom": "2%",
                                                       "justify-content": "center",
                                                       "align-items": "center",
                                                       "display": "flex",
                                                       "position": 'relative'}
                        ),
                        dcc.Graph(
                            id="graph-data",
                            style={"height": "254px"},
                            figure={
                                'data': [
                                    go.Scatter(
                                        x=[""],
                                        y=[""],
                                        mode='markers',
                                        marker={'size': 6}
                                    )
                                ],
                                'layout': go.Layout(
                                    xaxis={
                                        'title': 'Time (s)', "autorange": True},
                                    yaxis={'title': 'Temperature (C)'},
                                    margin={
                                        'l': 70, 'b': 100, 't': 0, 'r': 25},
                                )
                            }
                        )
                    ], className="twelve columns", style={"border-radius": "5px",
                                                          "border-width": "5px",
                                                          "border": "1px solid rgb(216, 216, 216)",
                                                          "marginBottom": "2%"
                                                          }
                ),
            ], className="row", style={"marginTop": "3%"}
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Control Panel",
                            style={"textAlign": "center"}
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                    id="action",
                                    options=[
                                        {'label': 'Direct', 'value': 'direct'},
                                        {'label': 'Reverse', 'value': 'reverse'}
                                    ],
                                    placeholder="Action",
                                     
                                ),
                                    ], className="four columns", style={"marginLeft": "14%",
                                                                        "marginRight": "9%"
                                                                        }
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="outputs-mode",
                                            options=[
                                                {'label': 'Off',
                                                    'value': 'off'},
                                                {'label': 'On',
                                                    'value': 'on'},
                                                {'label': 'PID',
                                                 'value': 'pid'},
                                            ],
                                            placeholder="Output"
                                        )

                                    ], className="four columns", style={
                                                                        "zIndex":"50"}
                                )
                    
                            ], className="row", style={"marginTop":"5%", "marginBottom":"4%"}
                        ),
                        html.Div(
                            [
                                daq.Knob(
                                    id="filter-rate",
                                    label="Filter Rate",
                                    labelPosition="bottom",
                                    size=65,
                                    value=0,
                                    scale={"custom": {
                                        "0": "1X", "1": "2X", "2": "X4", "3": "X8", "4": "X16", "5": "X32", "6": "X64", "7": "X128"}},
                                    color="#FF5E5E",
                                    max=7,
                                    className="six columns",
                                    style={"display": "flex",
                                           "justify-content": "center",
                                           "align-items": "center"}
                                ),
                                daq.Knob(
                                    id="thermo-type",
                                    label="Couple",
                                    labelPosition="bottom",
                                    size=65,
                                    value=0,
                                    scale={"custom": {"0": "J", "1": "K", "2": "T", "3": "E",
                                                      "4": "N", "5": "RES", "6": "R", "7": "S", "8": "B", "9": "C"}},
                                    color="#FF5E5E",
                                    max=9,
                                    className="six columns",
                                    style={"display": "flex",
                                           "justify-content": "center",
                                           "align-items": "center"}
                                )
                            ], className="row", style={"display": "flex",
                                                       "justify-content": "center",
                                                       "align-items": "center", }
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                daq.StopButton(
                                                    id="start-button",
                                                    buttonText="Start",
                                                    style={"display": "flex",
                                                           "justify-content": "center",
                                                           "align-items": "center",
                                                           "paddingBottom": "22%"},
                                                    n_clicks=0
                                                ),
                                                daq.StopButton(
                                                    id="stop-button",
                                                    buttonText="Stop",
                                                    style={"display": "flex",
                                                           "justify-content": "center",
                                                           "align-items": "center"},
                                                    n_clicks=0
                                                )
                                            ], className="three columns", style={"marginLeft": "13%"}
                                        ),
                                        daq.Knob(
                                            id="refresh-rate",
                                            label="Refresh",
                                            labelPosition="bottom",
                                            size=65,
                                            value=1,
                                            scale={"interval": 1},
                                            color="#FF5E5E",
                                            max=10,
                                            className="six columns",
                                            style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center",
                                                   "marginLeft": "17%",
                                                   "marginTop": "-11%"}
                                        ),
                                    ], className="row"
                                ),

                            ]
                        ),

                    ], className="four columns", style={"border-radius": "5px",
                                                        "border-width": "5px",
                                                        "border": "1px solid rgb(216, 216, 216)",
                                                        "height":"434px"}
                ),
                html.Div(
                    [
                        html.H3(
                            "PID Control",
                            style={"textAlign": "center"}
                        ),
                        daq.ToggleSwitch( # SWITCH Modes
                            id="PID-man-auto",
                            label=["Autotune", "Manual"],
                            color="#FF5E5E",
                            size=32,
                            style={"justify-content":"center"}
                        ),
                        html.Div(
                            id="autotune-box",
                            children=[
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                daq.BooleanSwitch(
                                                    id="adaptive-switch",
                                                    label="Adaptive Control",
                                                    labelPosition="bottom",
                                                    on=True,
                                                    style={"paddingTop":"8.5%",
                                                           "paddingBottom":"13%"}
                                                ),
                                                daq.NumericInput(
                                                    id="max-rate",
                                                    label="Max Rate (/min)",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom":"25%"}
                                                ),
                                                daq.StopButton(
                                                    id="autotune-button",
                                                    buttonText="Autotune",
                                                    style={"display": "flex",
                                                           "justify-content": "center",
                                                           "align-items": "center",
                                                           "paddingBottom": "34%"},
                                                    n_clicks=0
                                                ),

                                            ], className="five columns"
                                        ),
                                        html.Div(
                                            [
                                                daq.NumericInput(
                                                    id="PID-setpoint",
                                                    label="PID Setpoint 1 (C°)",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom": "5%"}
                                                ),
                                                daq.NumericInput(
                                                    id="autotune-timeout",
                                                    label="Autotune Timeout (s)",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom":"8%"}
                                                ),
                                                html.Div(
                                                    [
                                                        daq.Indicator(
                                                            id="output-1",
                                                            label="Out 1",
                                                            value=True,
                                                            color="#EF553B",
                                                            className="eight columns",
                                                            labelPosition="bottom",
                                                            size=20,
                                                            style={
                                                                "paddingLeft": "19%"}
                                                        )
                                                    ], className="row", style={"display": "flex",
                                                                               "justify-content": "center",
                                                                               "align-items": "center"}
                                                )

                                            ]
                                        ),
                                    ], className="row", style={"marginLeft": "12%", "marginBottom": "9%"}
                                ),
                            ], style={"marginTop":"5%", "position":"absolute", "height":"100%", "width":"100%"}
                        ),
                        html.Div(
                                id="manual-box",
                            children = [
                                html.Div(
                                    [
                                        html.Div( 
                                            [
                                                daq.BooleanSwitch(
                                                    id="adaptive-switch",
                                                    label="Adaptive Control",
                                                    labelPosition="bottom",
                                                    on=True,
                                                    style={"paddingTop":"8.5%",
                                                           "paddingBottom":"13%"}
                                                ),
                                                daq.NumericInput(
                                                    id="max-rate",
                                                    label="Max Rate (/min)",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom":"13%"}
                                                ),
                                                daq.NumericInput(
                                                    id="dev-gain",
                                                    label="Derivative Gain",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom":"21%"}
                                                ),
                                                daq.StopButton(
                                                    id="manual-button",
                                                    buttonText="Set PID",
                                                    style={"display": "flex",
                                                           "justify-content": "center",
                                                           "align-items": "center"},
                                                    n_clicks=0
                                                ),
                                            ], className="five columns"
                                        ),
                                        html.Div(
                                            [
                                                daq.NumericInput(
                                                    id="PID-setpoint",
                                                    label="PID Setpoint (C°)",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom": "5%"}
                                                ),
                                                daq.NumericInput(
                                                    id="pro-gain",
                                                    label="Propotional Gain",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom":"5%"}
                                                ),
                                                daq.NumericInput(
                                                    id="int-gain",
                                                    label="Integral Gain",
                                                    value=0.00,
                                                    max=300,
                                                    min=0,
                                                    size=75,
                                                    labelPosition="bottom",
                                                    style={"paddingBottom":"6%"}
                                                ),
                                                html.Div(
                                                    [
                                                        daq.Indicator(
                                                            id="output-1",
                                                            label="Out 1",
                                                            value=True,
                                                            color="#EF553B",
                                                            className="eight columns",
                                                            labelPosition="bottom",
                                                            size=20,
                                                            style={
                                                                "paddingLeft": "20%"}
                                                        )
                                                    ], className="row", style={"display": "flex",
                                                                               "justify-content": "center",
                                                                               "align-items": "center"}
                                                )

                                            ]
                                        ),
                                    ], className="row", style={"marginLeft": "12%", "marginBottom": "9%"}
                                ),
                            ], style={"marginTop":"5%", "position":"absolute", "height":"100%", "width":"100%"}
                        )
                    ], className="four columns", style={"border-radius": "5px",
                                                        "border-width": "5px",
                                                        "border": "1px solid rgb(216, 216, 216)",
                                                        "position":"relative",
                                                        "height":"435px"}
                ),
                html.Div(
                    [   html.H3(
                        "Data Response",
                        style={"textAlign":"center"}
                    ),
                        html.Div(
                            [
                                daq.LEDDisplay(
                                    id="omega-display",
                                    value="0.12345",
                                    style={"display": "flex",
                                           "justify-content": "center",
                                           "align-items": "center",
                                           "paddingTop": "1.6%",
                                           "paddingLeft": "5%",
                                           "marginLeft": "2.5%"},
                                    className="eight columns",
                                    size=36
                                ),
                                html.Div(
                                    id="unit-holder",
                                    children=[
                                        html.H5(
                                            "C°",
                                            id="unit",
                                            style={"border-radius": "3px",
                                                   "border-width": "5px",
                                                   "border": "1px solid rgb(216, 216, 216)",
                                                   "font-size": "47px",
                                                   "color": "#2a3f5f",
                                                   "display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center",
                                                   "width": "23%",
                                                   "marginLeft":"3%"
                                                   },
                                            className="four columns"
                                        ),
                                    ]
                                )
                            ], className="row", style={"marginBottom":"2%"}
                        ),
                        html.Div(
                            [
                                daq.LEDDisplay(
                                    id="PID-display",
                                    value="0.12",
                                    style={"display": "flex",
                                           "justify-content": "center",
                                           "align-items": "center",
                                           "paddingTop": "1.6%",
                                           "paddingLeft": "5%",
                                           "marginLeft": "7%"},
                                    className="four columns",
                                    size=36
                                ),
                                html.Div(
                                    id="unit-holder",
                                    children=[
                                        html.H5(
                                            "PID %",
                                            id="unit",
                                            style={"border-radius": "3px",
                                                   "border-width": "5px",
                                                   "border": "1px solid rgb(216, 216, 216)",
                                                   "font-size": "47px",
                                                   "color": "#2a3f5f",
                                                   "display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center",
                                                   "width": "40%",
                                                   "marginLeft":"16%"
                                                   },
                                            className="six columns"
                                        ),
                                    ]
                                )
                            ], className="row", style={"marginBottom":"4%"}
                        ),
                        dcc.Textarea(
                            id="status-monitor",
                            placeholder='Enter a value...',
                            value='This is a TextArea component',
                            style={'width': '85%', "height": "157px",
                                                   "marginLeft": "8.7%", "marginBottom": "6%"}
                        )
                    ], className="four columns", style={"border-radius": "5px",
                                                        "border-width": "5px",
                                                        "border": "1px solid rgb(216, 216, 216)",
                                                        "height":"436px"}
                )

            ], className="row"
        ),
        html.Div(
            [
                html.Div(id="stop-timestamp"),
                html.Div(id="start-timestamp"),
                html.Div(id="reset-timestamp"),
                html.Div(id="autotune-timestamp"),
                html.Div(id="graph-data-send"),
                html.Div(id="temperature-store"),
                html.Div(id="command-string"),
                html.Div(id="thermotype-hold"),
                html.Div(id="filter-hold"),
                html.Div(id="autotune-start"),
                html.Div(id="autotune-setpoint"),
                html.Div(id="autotune-adapt"),
                html.Div(id="manual-start"),
                html.Div(id="pid-action"),
                html.Div(id="output-mode"),
                # dcc.Interval(
                #     id="graph-interval",
                #     interval=100000,
                #     n_intervals=0
                # )

            ], style={"visibility": "hidden"}
        )
    ], style={'padding': '0px 30px 0px 30px'}
)


            ],
            style={'padding': '0px 10px 0px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "1180px",
              'height': "955px",
              'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
        )
        
# Manual and Auto
@app.callback(
    Output("manual-box", "style"),
    [Input("PID-man-auto", "value")],
    [State("manual-box", "style")]
)
def capture_components(value, style):
    if value:
        style["visibility"] = "hidden"
        style["zIndex"] = "-10"
    else:
        style["visibility"] = "visible"
        style["zIndex"] = "20"
    return style


@app.callback(
    Output("autotune-box", "style"),
    [Input("PID-man-auto", "value")],
    [State("autotune-box", "style")]
)
def sweep_components(value, style):
    if value:
        style["visibility"] = "visible"
        style["zIndex"] = "20"
    else:
        style["visibility"] = "hidden"
        style["zIndex"] = "-10"
    return style

# Filter Rate
@app.callback(
    Output("filter-hold", "children"),
    [Input("filter-rate", "value")]
)
def filter_hold(filter_knob):
    filter_knob = int(filter_knob)
    ser.write_register(655, filter_knob, 0, 16, False)
    return filter_hold

# Thermocouple


@app.callback(
    Output("thermotype-hold", "children"),
    [Input("thermo-type", "value")]
)
def thermotype_hold(thermo_knob):
    thermo_knob = int(thermo_knob)
    if thermo_knob == 5:
        return
    ser.write_register(643, thermo_knob, 0, 16, False)
    return thermo_knob

# Buttons


@app.callback(
    Output("start-timestamp", "children"),
    [Input("start-button", "n_clicks")]
)
def start_time(start):
    if start >= 1:
        return time.time()
    return 0.0


@app.callback(
    Output("stop-timestamp", "children"),
    [Input("stop-button", "n_clicks")]
)
def start_time(stop):
    return time.time()


@app.callback(
    Output("reset-timestamp", "children"),
    [Input("reset-button", "n_clicks")]
)
def reset_time(reset):
    return time.time()


@app.callback(
    Output("autotune-timestamp", "children"),
    [Input("autotune-button", "n_clicks")]
)
def autotune_time(autotune):
    return time.time()
# Button Control Panel


@app.callback(
    Output("command-string", "children"),
    [Input("start-timestamp", "children"),
     Input("stop-timestamp", "children"),
     Input("reset-timestamp", "children"),
     Input("autotune-timestamp", "children")]
)
def command_string(start_button, stop_button, reset_button, autotune_button):
    master_command = {"START": start_button,
                      "STOP": stop_button, "RESET": reset_button, "AUTO": autotune_button}
    recent_command = max(master_command, key=master_command.get)
    print(recent_command)
    return recent_command

# Action
@app.callback(
    Output("pid-action", "children"),
    [Input("action", "value")]
)
def action(action_value):
    if action_value == "direct": 
        ser.write_register(673, 1, 0, 16, False) #PID Action
    elif action_value == "reverse": 
        ser.write_register(673, 0, 0, 16, False) #PID Action

# Output Mode
@app.callback(
    Output("output-mode", "children"),
    [Input("outputs-mode", "value")]
)
def action(output_value):
    if output_value == "off": 
        ser.write_register(1025, 0, 0, 16, False) #Output 1 Mode
    elif output_value == "on": 
        ser.write_register(1025, 2, 0, 16, False) #Output 1 Mode
    elif output_value == "pid":
        ser.write_register(1025, 1, 0, 16, False) #Output 1 Mode
# Adaptive Control
@app.callback(
    Output("autotune-adapt", "children"),
    [Input("adaptive-switch", "on")]
)
def autotune_adaptive(control):
    if control:
        ser.write_register(672, 1, 0, 16, False)
        return
    ser.write_register(672, 0, 0, 16, False)
    return

# Manual
@app.callback(
    Output("manual-start", "children"),
    [Input("manual-button", "n_clicks")],
    [State("max-rate","value"),
    State("dev-gain","value"),
    State("pro-gain","value"),
    State("int-gain","value"),
    State("PID-setpoint","value"),
    ]
)
def set_PID(button, max_rate, dev_gain, pro_gain, int_gain, PID_setpoint):
    if button >= 1:
        ser.write_float(676, pro_gain, 2) 
        ser.write_float(678, int_gain, 2)
        ser.write_float(680, dev_gain, 2)
        ser.write_float(682, max_rate, 2)
        ser.write_float(544, PID_setpoint, 2)
        return
# Autotune
@app.callback(
    Output("autotune-start", "children"),
    [Input("manual-button", "n_clicks")],
    [State("max-rate","value"),
    State("autotune-timeout","value"),
    State("PID-setpoint","value"),
    ]
)
def set_PID(button, max_rate, autotune_timeout, PID_setpoint):
    if button >= 1:
        ser.write_float(682, max_rate, 2)
        ser.write_float(544, PID_setpoint, 2)
        ser.write_long(674, autotune_timeout, False)
        ser.write_register(579, 1, 0, 16, False) #Autotune Start
        return

# @app.callback(
#     Output("autotune-start", "children"),
#     [Input("command-string", "children")]
# )
# def autotune_time(command):
#     if command == "AUTO":
#         ser.write_register(579, 1, 0, 16, False)
#         return

# Autotune Setpoint


# @app.callback(
#     Output("autotune-setpoint", "children"),
#     [Input("PID-setpoint", "value")]
# )
# def autotune_setpoint(value):
#     ser.write_long(548, value, False)
#     return

# OUT LED 1


@app.callback(
    Output("output-1", "color"),
    [Input("graph-interval", "n_intervals")]
)
def autotune_setpoint(value):
    output_1 = ser.read_register(560, 0, 3, False)
    print(output_1)
    if output_1 != 0:
        return "#00cc96"
    return "#EF553B"



# Rate
@app.callback(
    Output("graph-interval", "interval"),
    [Input("command-string", "children"),
     Input("refresh-rate", "value")]
)
def graph_control(command, rate):
    if command == "START":
        ser.write_register(576, 6, 0, 16, False)  # Run Mode
        rate = int(rate) * 1000
        return rate
    else:
        return 2500

# Temperature Store


@app.callback(
    Output("temperature-store", "children"),
    [Input("command-string", "children"),
     Input("graph-interval", "n_intervals")]
)
def graph_control(command, rate):
    if command == "START":
        # return
        temperature = ser.read_float(528, 3, 2)
        return temperature


# LED Control Panel
@app.callback(
    Output("omega-display", "value"),
    [Input("temperature-store", "children")],
    [State("command-string", "children")]
)
def graph_control(temperature, command):
    if command == "START":
        temperature = round(temperature, 3)
        return temperature
    return 321.25

@app.callback(
    Output("PID-display", "value"),
    [Input("graph-interval", "n_intervals")],
    [State("command-string", "children")]
)
def PID_percent(n_intervals, command):
    if command == "START":
        percent = ser.read_float(554, 3, 2)
        percent = round(percent, 1)
        return percent
    return 0.00
# Graph LED


@app.callback(
    Output("graph-on-off", "color"),
    [Input("command-string", "children")]
)
def graph_LED(command):
    if command == "START":
        return "#00cc96"
    ser.write_register(576, 5, 0, 16, False)
    return "#EF553B"


# Serial Monitor
@app.callback(
    Output("status-monitor", "value"),
    [Input("graph-interval", "n_intervals")]
)
def serial_monitor(intervals):

    system_state = ser.read_register(576, 0, 3, False)
    proportional_gain = str(ser.read_float(676, 3, 2))
    integral_gain = str(ser.read_float(678, 3, 2))
    derivative_gain = str(ser.read_float(680, 3, 2))
    pid_percent_high = str(ser.read_float(684, 3, 2))
    pid_percent_low = str(ser.read_float(682, 3, 2))
 
    if system_state == 6:
        state = "Running"
    elif system_state == 7:
        state = "Standby"
    elif system_state == 5:
        state = "Wait"
    elif system_state == 12:
        state = "Autotune in Progress"
    elif system_state == 8:
        state = "Stop"
    elif system_state == 11:
        state = "Shutdown"
    elif system_state == 0:
        state = "Stop"
    elif system_state == 1:
        state = "Idle"
    elif system_state == 2:
        state = "Adjusting input value"
    elif system_state == 3:
        state = "Adjusting output value"
    elif system_state == 4:
        state = "Modify Parameter in OPER Mode"
    elif system_state == 9:
        state = "Paused"
    elif system_state == 10:
        state = "Fault"
    
    status = ("-----------STATUS------------\n" +
              "System Status: " +
              state +
              "\nProportional Gain: " +
              proportional_gain +
              "\nIntegral Gain: " +
              integral_gain +
              "\nDerivative Gain: " +
              derivative_gain +
              "\nPID Percent High: " +
              pid_percent_high +
              "\nPID Percent Low: " +
              pid_percent_low)

    return status

# Graph


@app.callback(
    Output("graph-data", "figure"),
    [Input("temperature-store", "children")],
    [State("graph-data", "figure"),
     State("command-string", "children"),
     State("start-timestamp", "children"),
     State("start-button", "n_clicks"),
     State("PID-setpoint","value")]
)
def graph_data(temperature, figure, command, start, start_button, PID):
    # x_range_min_num = figure["layout"]["xaxis"]["range"]
    # x_range_max_num = figure["layout"]["xaxis"]["range"]

    if command == "START":
        diff = int(time.time() - start)

        time_now = datetime.datetime.now().strftime("%H:%M:%S")

        temperature = round(temperature, 1)
        # print(diff)
        x = figure["data"][0]['x']
        y = figure["data"][0]['y']
        # print(x_range_max_num)
        # x_range_min = x_range_min_num[0]
        # x_range_max = x_range_max_num[1]
        # print(x_range_min)
        x.append(time_now)
        y.append(temperature)
        # if diff == x_range_max:
        #     x_range_min_num[0] = diff
        #     x_range_max_num[1] = diff + 20
        #     x_range_min = x_range_min_num[0]
        #     x_range_max = x_range_max_num[1]
    elif command == "RESET":
        x = [""]
        y = [""]
        # x_range_min_num[0] = 0
        # x_range_max_num[1] = 10
        # x_range_min = x_range_min_num[0]
        # x_range_max = x_range_max_num[1]
    return {
        'data': [
            go.Scatter(
                x=x,
                y=y,
                mode='lines',
                marker={'size': 6}
            ),
            # go.Scatter(
            #     x=PID,
            #     y=y,
            #     mode='lines',
            #     marker={'size': 6}

            # )
        ],
        'layout': go.Layout(
            autosize=True,
            xaxis={
                'title': 'Time (s)', "autorange": True},
            yaxis={
                'title': 'Temperature(C)', "autorange": True},
            margin={
                'l': 70, 'b': 100, 't': 0, 'r': 25},
        )
    }


if __name__ == '__main__':

    app.run_server(debug=False)
