import tornado.ioloop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
import json


connected_clients = set()
pkg_num = 0


class WebSocketHandler(WebSocketHandler):
    """
    Handles WebSocket connection events to server.
    """

    def open(self, *args, **kwargs):
        print("New WebSocket connection")
        connected_clients.add(self)
        self.write_message("Welcome to EEICT Demodata -server!")

    def on_message(self, message):
        print(f"Received from client: {message}")

    def on_close(self):
        print("Client connection closed.")
        connected_clients.discard(self)


def start_server():
    """
    Creates and starts the EEICT Demodata server.
    """

    server_address = "0.0.0.0"
    server_port = 8080
    server_endpoint = "demodata"

    server = Application([(rf"/{server_endpoint}", WebSocketHandler)])

    server.listen(server_port, server_address)

    print(
        f"EEICT Demodata -server @ ws://{server_address}:{server_port}/demodata"
    )

    # Start the WS server loop and stream data to clients using given interval.
    # 64 ticks/second = 15.625ms
    interval_ms = 15.625
    tornado.ioloop.PeriodicCallback(stream_data, interval_ms).start()
    tornado.ioloop.IOLoop.current().start()


def stream_data():
    """
    To be deprecated...
    """

    global pkg_num
    pkg_num += 1
    tornado.ioloop.IOLoop.current().add_callback(
        send_data_to_clients, str(pkg_num)
    )


async def send_data_to_clients(data):
    """
    Broadcasts JSON data to all connected WebSocket clients.
    """

    if connected_clients:
        for client in list(connected_clients):
            try:
                client.write_message(data)
            except Exception:
                connected_clients.discard(client)


if __name__ == "__main__":
    start_server()
