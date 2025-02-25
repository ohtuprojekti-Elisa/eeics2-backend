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


# Global
connected_clients: set[WebSocketHandler] = set()
tick_fetch_interval: PeriodicCallback
ticks = None


class WSHandler(WebSocketHandler):
    """
    Handles WebSocket connections to the EEICT server.
    """

    def open(self, *args: str, **kwargs: str):
        """
        Handles new connections.
        """
        connected_clients.add(self)

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

        stream_pause()

    def total_clients(self):
        return f"Total clients: {len(connected_clients)}"


def start_server():
    """
    Creates and starts the EEICT server.
    """

    global ticks

    ticks = ticks_chopper()

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

    tick_fetch_interval = PeriodicCallback(fetch_tick, interval_ms)
    tick_fetch_interval.start()


def stream_pause():
    """
    When client disconnects, stream gets paused.
    """

    global tick_fetch_interval
    global connected_clients

    # Check if server has no clients
    if len(connected_clients) == 0:
        if tick_fetch_interval.is_running():
            tick_fetch_interval.stop()

            logging.info("Streaming paused ...")


def settings_reader():
    """
    Reads static information from given JSON file,
    to be assigned to different settings values.
    """

    pass


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
            tick_fetch_interval.stop()  # remove this!
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


def ticks_chopper():
    """
    Chops ticks from JSON data.
    This function uses Ijson (Iterative JSON parse) library for reading
    a large JSON files directly from hard-drive, without first loading it
    to main memory.
    """

    filename = "./data/test_large.json"
    file_path = Path(__file__).parent / filename

    with open(file_path, "r") as file:
        for tick in ijson.items(file, "ticks.item"):
            yield str(tick)


if __name__ == "__main__":
    start_server()
