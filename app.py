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

# ser = minimalmodbus.Instrument('COM16', 1, mode='rtu')


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
                            style={"height": "820px"},
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
                    ], className="eight columns", style={"border-radius": "5px",
                                                         "border-width": "5px",
                                                         "border": "1px solid rgb(216, 216, 216)",
                                                         "paddingBottom": "2%"}
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
                                        daq.LEDDisplay(
                                            id="omega-display",
                                            value="0.12345",
                                            style={"display": "flex",
                                                   "justify-content": "center",
                                                   "align-items": "center",
                                                   "paddingTop": "1.5%",
                                                   "paddingLeft": "5%",
                                                   "marginLeft": "2.5%"},
                                            className="eight columns"
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
                                                           "font-size": "52px",
                                                           "color": "#2a3f5f",
                                                           "display": "flex",
                                                           "justify-content": "center",
                                                           "align-items": "center",
                                                           "width": "23%"
                                                           },
                                                    className="four columns"
                                                ),
                                            ]
                                        )
                                    ], className="row"
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
                                            label="Couple Type",
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
                                            label="Refresh Rate",
                                            labelPosition="bottom",
                                            size=65,
                                            value=1,
                                            min=1,
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

                            ], style={"border-radius": "5px",
                                      "border-width": "5px",
                                      "border": "1px solid rgb(216, 216, 216)",
                                      "height": "465px",
                                      "marginBottom":"5%"}
                        ),
                        html.Div(
                            [
                                html.H4(
                                    "PID Control",
                                    style={"textAlign": "center"}
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                [
                                                    daq.StopButton(
                                                        id="autotune-button",
                                                        buttonText="Autotune",
                                                        style={"display": "flex",
                                                               "justify-content": "center",
                                                               "align-items": "center",
                                                               "marginBottom":"30%"},
                                                        n_clicks=0
                                                    ),
                                                    daq.BooleanSwitch(
                                                        id="adaptive-switch",
                                                        label="Adaptive Control",
                                                        labelPosition="bottom",
                                                        on=True
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
                                                        style={"paddingBottom":"9%",
                                                               "paddingRight":"22%"}
                                                    ),
                                            html.Div(
                                            [
                                                daq.Indicator(
                                                    id="output-1",
                                                    label="Out 1",
                                                    value=True,
                                                    color="#EF553B",
                                                    className="six columns",
                                                    labelPosition="bottom",
                                                    size=20,
                                                    style={"paddingLeft":"5%"}
                                                ),
                                                daq.Indicator(
                                                    id="output-2",
                                                    label="Out 2",
                                                    value=True,
                                                    color="#EF553B",
                                                    className="six columns",
                                                    labelPosition="bottom",
                                                    size=20
                                                )
                                            ], className="row", style={"display": "flex",
                                                                         "justify-content": "center",
                                                                         "align-items": "center"}
                                        )

                                                ],className="seven columns"
                                            )
                                            ], className="row", style={"marginLeft":"12%", "marginBottom":"9%"}
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Textarea(
                                            id="status-monitor",
                                            placeholder='Enter a value...',
                                            value='This is a TextArea component',
                                            style={'width': '90%', "height": "185px",
                                                   "marginLeft": "4.7%", "marginBottom": "6%"}
                                        )
                                    ]
                                )
                            ], style={"border-radius": "5px",
                                      "border-width": "5px",
                                      "border": "1px solid rgb(216, 216, 216)"}
                        )
                    ], className="four columns"
                )
            ], className="row", style={"marginTop": "3%"}
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
                dcc.Interval(
                    id="graph-interval",
                    interval=100000,
                    n_intervals=0
                )

            ], style={"visibility": "hidden"}
        )
    ], style={'padding': '0px 10px 0px 10px',
              'marginLeft': 'auto',
              'marginRight': 'auto',
              "width": "1200px",
              'height': "1070px",
              'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}
)

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

# Autotune
@app.callback(
    Output("autotune-start", "children"),
    [Input("command-string", "children")]
)
def autotune_time(command):
    if command == "AUTO":
        ser.write_register(579, 1, 0, 16, False)
        return 

# Autotune Setpoint
@app.callback(
    Output("autotune-setpoint", "children"),
    [Input("PID-setpoint", "value")]
)
def autotune_setpoint(value):
        ser.write_long(548, value, False)
        return 

# Autotune OUT LED 1
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
        

# Autotune OUT LED 2
@app.callback(
    Output("output-2", "color"),
    [Input("graph-interval", "n_intervals")]
)
def autotune_setpoint(value):
        output_2 = ser.read_register(561, 0, 3, False)
        if output_2 == 1:
            return "#00cc96"
        return "#EF553B"

# Autotune Adaptive Control
@app.callback(
    Output("autotune-adapt", "children"),
    [Input("adaptive-switch", "on")]
)
def autotune_adaptive(control):
    if control:
        ser.write_register(672,1,0,16, False)
        return 
    ser.write_register(672,0,0,16, False)
    return 


# Rate
@app.callback(
    Output("graph-interval", "interval"),
    [Input("command-string", "children"),
     Input("refresh-rate", "value")]
)
def graph_control(command, rate):
    if command == "START":
        ser.write_register(576, 6, 0, 16, False) # Run Mode
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
    Output("status-monitor","value"),
    [Input("graph-interval","n_intervals")]
)
def serial_monitor(intervals):

    system_state = ser.read_register(576, 0, 3, False)
    proportional_gain = str(ser.read_float(676, 3, 2))
    integral_gain = str(ser.read_float(676, 3, 2))
    derivative_gain = str(ser.read_float(676, 3, 2))
    pid_percent_high = str(ser.read_float(684, 3, 2))
    pid_percent_low = str(ser.read_float(682, 3, 2))
    pid_output_level = str(ser.read_float(554, 3, 2))
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
    status = ("-----------STATUS------------\n"+
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
              "\nPID Percent Low: "+
              pid_percent_low +
              "\nPID Output Level: "+
              pid_output_level)
              
    return status

# Graph

@app.callback(
    Output("graph-data", "figure"),
    [Input("temperature-store", "children")],
    [State("graph-data", "figure"),
     State("command-string", "children"),
     State("start-timestamp", "children"),
     State("start-button", "n_clicks")]
)
def graph_data(temperature, figure, command, start, start_button):
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
                mode='lines+markers',
                marker={'size': 6}
            )
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
