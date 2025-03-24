import json
import ijson
import logging
from pathlib import Path
from decimal import Decimal
from tornado.web import Application
from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.websocket import WebSocketHandler
from . import messages as msg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class DemoDataWSH(WebSocketHandler):
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

    def __init__(self):
        self.class_name = "SERVER"  # Temp before custom logger is implemented
        # Server related
        self.srv_address: str = ""
        self.srv_port: int = 0
        self.srv_endpoint: str = ""
        self.loop_mode: bool = False
        self.connected_clients: set[DemoDataWSH] = set()
        # Demodata info
        self.tickrate: int = 64
        self.total_ticks: int = 0
        self.map_name: str = ""
        # Ticks related
        self.ticks_filename: Path = Path()
        self.ticks = self._ticks_chopper()
        self.tick_fetch_interval: float = 0.0
        self.tick_fetch_loop: PeriodicCallback = PeriodicCallback(
            lambda: None, 1000
        )
        # Server speed control
        self.play_nth: int = 0
        self.play_threshold: int = 0
        self.skip_counter: int = 0
        self.stream_interval: float = 0.0

    def open(self, handler: DemoDataWSH) -> int:
        """Handles new connections, sends messages to client and starts the stream."""
        self.connected_clients.add(handler)
        logging.info(
            f"{self.class_name} - {msg.CLIENT_NEW_CONNECTION}: {handler.request.remote_ip}"
        )
        logging.info(f"{self.class_name} - {self.total_clients()}")
        handler.write_message(f"{self.class_name} - {msg.CLIENT_WELCOME}")
        handler.write_message(f"{self.class_name} - {msg.CLIENT_START_STREAM}")
        self._stream_start()
        return len(self.connected_clients)

    def on_close(self, handler: DemoDataWSH) -> int:
        """Handles closed connections."""
        self.connected_clients.discard(handler)
        logging.info(
            f"{self.class_name} - {msg.CLIENT_CLOSED_CONNECTION}: {handler.request.remote_ip}"
        )
        logging.info(f"{self.class_name} - {self.total_clients()}")
        self._stream_pause()
        return len(self.connected_clients)

    def total_clients(self) -> str:
        """Formats info on clients to a single string."""
        connected_clients = len(self.connected_clients)
        return (
            f"{self.class_name} - {msg.CLIENT_TOTAL_NUM}: {connected_clients}"
        )

    def _server_info(self) -> str:
        """Formats server info to a single string."""
        return f"{self.class_name} - {self.srv_address}:{self.srv_port}/{self.srv_endpoint}"

    def _stream_start(self) -> bool:
        """Streams ticks to EEICT clients using the calculated interval (ms)."""
        if len(self.connected_clients) == 1:
            self.tick_fetch_loop = PeriodicCallback(
                self._fetch_tick, self.tick_fetch_interval
            )
            self.tick_fetch_loop.start()
        return self.tick_fetch_loop.is_running()

    def _stream_pause(self) -> bool:
        """Pause stream if no connected clients."""
        if len(self.connected_clients) == 0:
            if self.tick_fetch_loop.is_running():
                self.tick_fetch_loop.stop()
                logging.info(f"{self.class_name} - {msg.STREAM_PAUSED}")
        return self.tick_fetch_loop.is_running()

    def _create_config_filename(self) -> Path:
        """Creates $_config.json path from $.json path."""
        config_filename = self.ticks_filename.with_name(
            f"{self.ticks_filename.stem}_config.json"
        )
        return config_filename

    def _read_config(self) -> None:
        """Reads values from $_config.json and assigns them to variables."""
        config_filename = self._create_config_filename()
        try:
            with open(Path(config_filename)) as f:
                config = json.load(f)
                self.tickrate = config["tickrate"]
                self.total_ticks = config["total_ticks"]
                self.map_name = config["map_name"]
        except Exception as e:
            logging.error(f"{self.class_name} - {msg.FILE_CONFIG_ERROR}: {e}")

    def _init_values(self) -> None:
        """Calculate required values before streaming can be started."""
        self.play_nth = self._normalize_nth(self.play_nth)
        self.tick_fetch_interval = self._calc_fetch_interval(self.tickrate)
        self.stream_interval = self._calc_stream_interval(
            self.tickrate, self.play_nth
        )
        self.play_threshold = self._calc_play_threshold(self.play_nth)

    def _normalize_nth(self, play_nth: int) -> int:
        """Takes play_nth and ensures that it is at least 1."""
        return max(1, play_nth)

    def _calc_fetch_interval(self, tickrate: int) -> float:
        """Takes tickrate and converts it to fetch_interval (ms), used in fetching ticks."""
        tickrate = max(64, tickrate)
        fetch_interval: float = 1000 / tickrate
        return fetch_interval

    def _calc_stream_interval(self, tickrate: int, play_nth: int) -> float:
        """Takes tickrate and play_nth as divider and converts them to stream_interval (ms), used in client side."""
        play_nth = self._normalize_nth(play_nth)
        stream_interval: float = 1000 / (tickrate / play_nth)
        return stream_interval

    def _calc_play_threshold(self, play_nth: int) -> int:
        """Takes play_nth and creates a threshold value from it, used in skipping ticks."""
        return max(1, play_nth - 1)

    def _fetch_tick(self) -> None:
        """Fetches the next tick from the "tick_data" and sends it for streaming."""
        try:
            if self.ticks:
                tick = next(self.ticks)
            else:
                logging.warning(
                    f"{self.class_name} - {msg.STREAM_TICK_NOT_INIT}"
                )
                self.tick_fetch_loop.stop()
                return
            if self.play_nth == 1 or (
                self.skip_counter == self.play_threshold
            ):
                IOLoop.current().add_callback(self._stream_tick, tick)
                self.skip_counter = 0
            else:
                self.skip_counter += 1
        except StopIteration:
            if self.loop_mode:
                self.ticks = self._ticks_chopper()
                logging.info(f"{self.class_name} - {msg.STREAM_LOOP_MODE}")
            else:
                IOLoop.current().add_callback(self._stream_tick, "EOF")
                self.tick_fetch_loop.stop()
                logging.warning(f"{self.class_name} - {msg.STREAM_ENDED}")

    async def _stream_tick(self, tick: str) -> None:
        """Stream a single tick to all connected clients."""
        if self.connected_clients:
            for client in list(self.connected_clients):
                try:
                    await client.write_message(tick)
                except Exception:
                    self.connected_clients.discard(client)

    def _ticks_chopper(self) -> ijson.items:
        """Chops ticks from JSON data.

        This function uses Ijson (Iterative JSON parse) library for reading
        a large JSON files directly from hard-drive, without first loading
        it to main memory.
        """
        with open(self.ticks_filename, "r") as file:
            for tick in ijson.items(
                file,
                "ticks.item",
                use_float=True,
            ):
                yield json.dumps(tick)

    def ticks_file(self, ticks_filename: Path) -> Path:
        """Handles the input file for $.json (ticks)."""
        self.ticks_filename = ticks_filename
        logging.info(
            f"{self.class_name} - {msg.STREAM_INPUT_FILE}: {self.ticks_filename}"
        )
        return ticks_filename

    def start_server(
        self,
        srv_address: str,
        srv_port: int,
        srv_endpoint: str,
        loop_mode: bool = False,
        play_nth: int = 1,
    ) -> None:
        """Starts the demodata server."""
        # Init values from arguments
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.srv_endpoint = srv_endpoint
        self.loop_mode = loop_mode
        self.play_nth = play_nth
        # Read demodata config file
        self._read_config()
        # Init rest of variables
        self._init_values()
        # Start server
        app = Application(
            [(self.srv_endpoint, DemoDataWSH, dict(server=self))]
        )
        app.listen(self.srv_port, self.srv_address)
        logging.info(
            f"{self.class_name} - {msg.SERVER_START} @ {self._server_info()}"
        )
        logging.info(f"{self.class_name} - {msg.CLIENT_CAN_CONNECT}")
        # Start main loop
        IOLoop.current().start()
