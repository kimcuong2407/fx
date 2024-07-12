from websocket import WebSocketApp


def on_message(wsapp, message):
    print(message)


wsapp = WebSocketApp("wss://stream.binance.com:9443/ws/block", on_message=on_message)
wsapp.run_forever()
