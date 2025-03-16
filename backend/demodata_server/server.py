import json
import ijson
import logging
from pathlib import Path
from decimal import Decimal
from tornado.web import Application
from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.websocket import WebSocketHandler


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class DemodataWebSocketHandler(WebSocketHandler):
    def initialize(self, server):
        self.server = server

    def open(self):
        self.server.open(self)

    def on_close(self):
        self.server.on_close(self)

    async def on_message(self, message):
        # Handle incoming messages if needed
        pass


class DemodataServer:
    """Handles WebSocket connections to EEICT client(s)."""

    def __init__(
        self,
        srv_address: str,
        srv_port: int,
        srv_endpoint: str,
        developer_mode: bool = False,
    ):
        self.class_name = "SERVER"  # Temp before custom logger is implemented
        self.developer_mode = developer_mode
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.srv_endpoint = srv_endpoint
        self.filename = ""
        self.connected_clients: set[WebSocketHandler] = set()
        self.tick_fetch_interval: PeriodicCallback
        self.ticks = None

    def open(self, handler: WebSocketHandler):
        """Handles new connections."""
        self.connected_clients.add(handler)
        logging.info(f"New client connection: {handler.request.remote_ip}")
        logging.info(f"{self.total_clients()}")
        # Send messages to client and start server
        handler.write_message("Welcome to EEICT Demodata -server!")
        handler.write_message("Starting stream ...")
        self.stream_start()

    def on_close(self, handler: WebSocketHandler):
        """Handles closed connections."""
        self.connected_clients.discard(handler)
        logging.info(
            f"{self.class_name} - Client connection closed: {handler.request.remote_ip}"
        )
        logging.info(f"{self.class_name} - {self.total_clients()}")
        # Check if server has no clients
        if len(self.connected_clients) == 0:
            logging.info(f"{self.class_name} - Streaming paused ...")

    def total_clients(self):
        return f"Total clients: {len(self.connected_clients)}"

    def stream_start(self, interval_ms: float = 15.625):
        """
        Streams demodata to EEICT clients using the given interval,
        in example: 64 ticks/second = 15.625 ms.
        """
        self.ticks = self.ticks_chopper()
        self.tick_fetch_interval = PeriodicCallback(
            self.fetch_tick, interval_ms
        )
        self.tick_fetch_interval.start()

    def stream_pause(self):
        """When client disconnects,  stream gets paused."""
        if len(self.connected_clients) == 0:
            if self.tick_fetch_interval.is_running():
                self.tick_fetch_interval.stop()
                logging.info(f"{self.class_name} - Streaming paused ...")

    def fetch_tick(self):
        """Fetches the next tick from the "tick_data" and sends it for streaming."""
        try:
            if self.ticks:
                next_tick = next(self.ticks)
            else:
                logging.warning(
                    f"{self.class_name} - Tick stream is not initialized."
                )
                self.tick_fetch_interval.stop()
                return
            IOLoop.current().add_callback(self.stream_tick, next_tick)
        except StopIteration:
            IOLoop.current().add_callback(self.stream_tick, "EOF")
            self.tick_fetch_interval.stop()
            logging.warning(f"{self.class_name} - Stream ended!")

    async def stream_tick(self, tick: str):
        """Stream a single tick to all connected clients."""
        if self.connected_clients:
            for client in list(self.connected_clients):
                try:
                    await client.write_message(tick)
                except Exception:
                    self.connected_clients.discard(client)

    def convert_values(self, obj):
        """Convert ijson's mangled data back to normal (quickfix)."""
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bool):
            return obj
        elif isinstance(obj, dict):
            return {k: self.convert_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_values(v) for v in obj]
        return obj

    def ticks_chopper(self):
        """Chops ticks from JSON data.

        This function uses Ijson (Iterative JSON parse) library for reading
        a large JSON files directly from hard-drive, without first loading it
        to main memory.
        """
        filename = self.filename
        with open(filename, "r") as file:
            for tick in ijson.items(file, "ticks.item"):
                cleaned_tick = self.convert_values(tick)
                yield json.dumps(cleaned_tick)

    def demodata_input(self, filename: Path):
        """Handles the input file for demodata."""
        self.filename = filename
        logging.info(f"{self.class_name} - Received a file '{filename}'")

    def start_server(self):
        """Starts the demodata server."""
        app = Application(
            [
                (
                    self.srv_endpoint,
                    DemodataWebSocketHandler,
                    dict(server=self),
                )
            ]
        )
        app.listen(self.srv_port, self.srv_address)
        logging.info(
            f"{self.class_name} - EEICT Demodata -server @ ws://{self.srv_address}:{self.srv_port}{self.srv_endpoint}"
        )
        logging.info(f"{self.class_name} - EEICT client(s) can now connect!")
        IOLoop.current().start()
