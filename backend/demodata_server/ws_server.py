import logging
import ijson
from pathlib import Path
from tornado.web import Application
from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.websocket import WebSocketHandler


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Global variables
connected_clients: set[WebSocketHandler] = set()
data_stream_callback: PeriodicCallback
tick_data = None


class WSHandler(WebSocketHandler):
    """
    Handles WebSocket connection events to server.
    """

    def open(self, *args: str, **kwargs: str):
        connected_clients.add(self)

        # Client info
        logging.info(f"New client connection: {self.request.remote_ip}")
        logging.info(f"{self.total_clients()}")

        # Send messages to client
        self.write_message("Welcome to EEICT Demodata -server!")
        self.write_message("Starting stream.")

        start_data_stream()

    def on_message(self, message: str | bytes):
        logging.info(f"Received from client: {message}")

    def on_close(self):
        connected_clients.discard(self)

        logging.info(f"Client connection closed: {self.request.remote_ip}")
        logging.info(f"{self.total_clients()}")

        if len(connected_clients) == 0:
            if data_stream_callback.is_running():
                data_stream_callback.stop()
                logging.info("Callback stopped")

    def total_clients(self):
        return f"Total clients: {len(connected_clients)}"


def start_server():
    """
    Creates and starts the EEICT Demodata server.
    """

    global tick_data

    tick_data = json_chopper()

    server_address = "0.0.0.0"
    server_port = 8080
    server_endpoint = "/demodata"

    server = Application([(server_endpoint, WSHandler)])
    server.listen(server_port, server_address)

    logging.info(
        f"EEICT Demodata -server @ ws://{server_address}:{server_port}{server_endpoint}"
    )

    # Start the WS server main loop
    IOLoop.current().start()


def start_data_stream(interval_ms: float = 15.625):
    """
    Stream data to clients using the given interval,
    in example: 64 ticks/second = 15.625 ms.
    """

    global data_stream_callback

    data_stream_callback = PeriodicCallback(fetch_data, interval_ms)
    data_stream_callback.start()


def fetch_data():
    """
    Fetches the next item from the "tick_data" and sends it to clients.
    """

    global tick_data

    try:
        if tick_data:
            tick = next(tick_data)
        else:
            logging.info("Data generator is not initialized.")
            return

        IOLoop.current().add_callback(stream_data, tick)

    except StopIteration:
        # logging.info("No more data to send.")
        pass


async def stream_data(tick: str):
    """
    Stream demodata to all connected clients.
    """

    if connected_clients:
        for client in list(connected_clients):
            try:
                await client.write_message(tick)
            except Exception:
                connected_clients.discard(client)


def json_chopper():
    """
    Chop JSON data to single objects with given interval.
    This function uses Ijson (Iterative JSON parse) library for reading
    a large JSON files directly from hard-drive, without first loading it
    to main memory.
    """

    filename = "./data/test_small.json"
    file_path = Path(__file__).parent / filename

    with open(file_path, "r") as file:
        for tick in ijson.items(file, "demodata.item.ticks.item"):
            yield str(tick)


if __name__ == "__main__":
    start_server()
