import pandas as pd
import plotly.graph_objects as go
import csv
from dash import Dash,html, dash_table, dcc, Input, Output
import websocket, json

from threading import Thread
import threading

#HTML layout
app = Dash(__name__)
app.layout = html.Div([
    html.H4('BTCUSD stock candlestick chart'),
    dcc.Checklist(
        id = 'toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id = "graph"),
    dcc.Interval(
        id = 'interval-component',
        interval=1*1000,
        n_intervals = 0
    )
])

#Socket information
cc = 'btcusd'
interval = '1m'
socket = f'wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}'
opens   = []
closes  = []
highs   = []
lows    = []
volumes = []
col_name = ['Open', 'Close', 'High', 'Low', 'Volume']
data_frame = pd.DataFrame(columns=col_name)
stop_condition = False

#Server callback
@app.callback(
    Output("graph", "figure"), 
    Input("toggle-rangeslider", "value"),
    Input('interval-component','n_intervals'))

def display_candlestick(value,n):
    fig = go.Figure(data=[go.Candlestick(open = data_frame['Open'], high = data_frame['High'],low = data_frame['Low'], close = data_frame['Close'])])

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig


#Collecting data
def on_message(ws, message):
    global stop_condition
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    open   = candle['o']
    close  = candle['c']
    high   = candle['h']
    low    = candle['l']
    volume = candle['v']

    if is_candle_closed:
        opens.append(open)
        closes.append(close)
        highs.append(high)
        lows.append(low)
        volumes.append(volume)
        
        new_row = [open,close,high,low,volume]
        data_frame.loc[len(data_frame.index)] = new_row

        if len(opens) > 10:  # For example, stop after receiving 10 candles
            data_frame.drop(index=data_frame.index[0],axis=0,inplace=True)
            #stop_condition = True
            #ws.close()
        print(data_frame)

def on_close(ws):
    print("Connection closed")

#Multithreading
def run_dash_server():
    app.run_server(debug = True, use_reloader = False)

def collect_data():
    while not stop_condition:
        ws.run_forever()

if __name__ == '__main__':
    ws = websocket.WebSocketApp(socket,on_message = on_message, on_close = on_close)
    dash_process = threading.Thread(target=run_dash_server)
    data_process = threading.Thread(target=collect_data)

    dash_process.start()
    data_process.start()

    dash_process.join()
    data_process.join()