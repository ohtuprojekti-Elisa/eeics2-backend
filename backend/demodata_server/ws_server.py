import ijson
import logging
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
stream_timeout = 60


class WSHandler(WebSocketHandler):
    """
    Handles WebSocket connection events to server.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop_stream = None
        self.stream_timeout = stream_timeout

    def open(self, *args: str, **kwargs: str):
        connected_clients.add(self)

        # Cancel the stop stream timeout if a new client connects
        if self.stop_stream:
            IOLoop.current().remove_timeout(self.stop_stream)
            self.stop_stream = None

        logging.info(f"New client connection: {self.request.remote_ip}")
        logging.info(f"{self.total_clients()}")

        # Send messages to client
        self.write_message("Welcome to EEICT Demodata -server!")
        self.write_message("Starting stream ...")

        start_stream()

    def on_message(self, message: str | bytes):
        logging.info(f"Received from client: {message}")

    def on_close(self):
        connected_clients.discard(self)

        # Client info
        logging.info(f"Client connection closed: {self.request.remote_ip}")
        logging.info(f"{self.total_clients()}")

        # Check if server has no clients
        if len(connected_clients) == 0:
            if data_stream_callback.is_running():
                data_stream_callback.stop()
                logging.info("Streaming paused ...")

            # Stop JSON stream after n seconds
            self.stop_stream = IOLoop.current().call_later(
                self.stream_timeout, timeout_stream
            )

    def total_clients(self):
        return f"Total clients: {len(connected_clients)}"


def start_server():
    """
    Creates and starts the EEICT Demodata server.
    """
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


def start_stream(interval_ms: float = 15.625):
    """
    Stream data to clients using the given interval,
    in example: 64 ticks/second = 15.625 ms.
    """
    global data_stream_callback
    global tick_data

    tick_data = ticks_chopper()

    data_stream_callback = PeriodicCallback(fetch_data, interval_ms)
    data_stream_callback.start()


def timeout_stream():
    """
    After given interval after last client has disconnected
    server will unload the previously loaded demodata.
    """
    global tick_data

    tick_data = None

    logging.info(
        f"No clients connected for {stream_timeout} seconds. Resetting JSON stream."
    )


def fetch_data():
    """
    Fetches the next item from the "tick_data" and sends it to clients.
    """
    global data_stream_callback
    global tick_data

    try:
        if tick_data:
            next_tick = next(tick_data)
        else:
            logging.info("Tick stream is not initialized.")
            return

        IOLoop.current().add_callback(stream_data, next_tick)

    except StopIteration:
        IOLoop.current().add_callback(stream_data, "EOF")
        data_stream_callback.stop()

        logging.info("Stream ended!")


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


def settings_reader():
    """
    Reads static information from given JSON file,
    to be assigned to different settings values.
    """
    pass


def ticks_chopper():
    """
    Chop JSON data (ticks list) to single objects with given interval.
    This function uses Ijson (Iterative JSON parse) library for reading
    a large JSON files directly from hard-drive, without first loading it
    to main memory.
    """
    filename = "./data/test_small.json"
    file_path = Path(__file__).parent / filename

    with open(file_path, "r") as file:
        for tick in ijson.items(file, "ticks.item"):
            yield str(tick)


if __name__ == "__main__":
    start_server()
