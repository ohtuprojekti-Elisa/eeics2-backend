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
tick_fetch_interval: PeriodicCallback
ticks = None
stream_timeout_s = 60


class WSHandler(WebSocketHandler):
    """
    Handles WebSocket connections to EEICT server.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream_timeout_s = stream_timeout_s
        self.stop_stream = None

    def open(self, *args: str, **kwargs: str):
        """
        Handles new connections.
        """
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

        stream_start()

    def on_close(self):
        """
        Handles closed connections.
        """
        connected_clients.discard(self)

        # Client info
        logging.info(f"Client connection closed: {self.request.remote_ip}")
        logging.info(f"{self.total_clients()}")

        # Check if server has no clients
        if len(connected_clients) == 0:
            if tick_fetch_interval.is_running():
                tick_fetch_interval.stop()
                logging.info("Streaming paused ...")

            # Stop JSON stream after n seconds
            self.stop_stream = IOLoop.current().call_later(
                self.stream_timeout_s, stream_timeout
            )

    def total_clients(self):
        return f"Total clients: {len(connected_clients)}"


def start_server():
    """
    Creates and starts the EEICT server.
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


def stream_start(interval_ms: float = 15.625):
    """
    Streams demodata to EEICT clients using the given interval,
    in example: 64 ticks/second = 15.625 ms.
    """
    global tick_fetch_interval
    global ticks

    ticks = ticks_chopper()

    tick_fetch_interval = PeriodicCallback(fetch_tick, interval_ms)
    tick_fetch_interval.start()


def stream_timeout():
    """
    After the last client has disconnected from EEICT server,
    this will unload the previously loaded demodata.
    """
    global ticks

    ticks = None

    logging.info(
        f"No clients connected for {stream_timeout} seconds. Resetting JSON stream."
    )


def fetch_tick():
    """
    Fetches the next tick from the "tick_data" and sends it for streaming.
    """
    global tick_fetch_interval
    global ticks

    try:
        if ticks:
            next_tick = next(ticks)
        else:
            logging.info("Tick stream is not initialized.")
            return

        IOLoop.current().add_callback(stream_tick, next_tick)

    except StopIteration:
        IOLoop.current().add_callback(stream_tick, "EOF")
        tick_fetch_interval.stop()

        logging.info("Stream ended!")


async def stream_tick(tick: str):
    """
    Stream a single tick to all connected clients.
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
    Chops ticks from JSON data.
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
