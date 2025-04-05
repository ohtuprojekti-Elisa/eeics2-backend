import json
import ijson
import logging
from pathlib import Path
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
        self.last_tick_sent = 0

    def open(self):
        self.server.open(self)

    def on_close(self):
        self.server.on_close(self)

    async def on_message(self, message):
        await self.server.on_message(self, message)


class DemodataServer:
    """Handles WebSocket connections to EEICT client(s)."""

    def __init__(self):
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
        # Ticks
        self.ticks_filename: Path = Path()
        self.ticks = ijson.items
        self.tick_fetch_interval: float = 0.0
        self.tick_fetch_loop: PeriodicCallback = PeriodicCallback(
            lambda: None, 1000
        )
        # Burst mode
        self.burst_size = 640  # Number of ticks/burst
        self.burst_mode = False

    def _log(self, message: str, level: str = "info") -> None:
        """Helper method for logging messages with class name."""
        class_name = "SERVER"
        log_func = getattr(logging, level, logging.info)
        log_func(f"{class_name} - {message}")

    def _validate_config(self, config: dict) -> None:
        """Validates the configuration file for required keys."""
        required_keys = ["tickrate", "total_ticks", "map_name"]
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required config key: {key}")

    def _sanitize_tickrate(self, tickrate: int) -> int:
        """Ensures the tickrate is at least 64."""
        return max(64, tickrate)

    def open(self, client: DemoDataWSH) -> int:
        """Handles new connections, sends messages to client and starts the stream."""
        self.connected_clients.add(client)
        self._log(f"{msg.CLIENT_NEW_CONNECTION}: {client.request.remote_ip}")
        self._log(f"{self.total_clients()}")
        client.write_message(f"{msg.CLIENT_WELCOME}")
        self._stream_start(client)
        return len(self.connected_clients)

    def on_close(self, client: DemoDataWSH) -> int:
        """Handles closed connections."""
        self.connected_clients.discard(client)
        self._log(
            f"{msg.CLIENT_CLOSED_CONNECTION}: {client.request.remote_ip}"
        )
        self._log(f"{self.total_clients()}")
        self._stream_pause()
        return len(self.connected_clients)

    async def on_message(self, message: str) -> None:
        """Handles messages from clients."""
        try:
            data = json.loads(message)
            if data.get("tick_status") <= 200:
                self._log("Client needs more ticks")
        except json.JSONDecodeError:
            self._log(
                f"Invalid JSON received from client: {message}",
                level="warning",
            )

    def total_clients(self) -> str:
        """Formats info on clients to a single string."""
        connected_clients = len(self.connected_clients)
        return f"{msg.CLIENT_TOTAL_NUM}: {connected_clients}"

    def _server_info(self) -> str:
        """Formats server info to a single string."""
        return f"{self.srv_address}:{self.srv_port}/{self.srv_endpoint}"

    def _stream_start(self, client: DemoDataWSH) -> bool:
        """Starts the stream for a client."""
        client.write_message(f"{msg.CLIENT_START_STREAM}")
        if len(self.connected_clients) == 1:
            IOLoop.current().add_callback(self._burst_ticks, client)
            self.tick_fetch_loop.start()
        return self.tick_fetch_loop.is_running()

    def _stream_pause(self) -> bool:
        """Pause stream if no connected clients."""
        if len(self.connected_clients) == 0:
            if self.tick_fetch_loop.is_running():
                self.tick_fetch_loop.stop()
                self._log(f"{msg.STREAM_PAUSED}")
        return self.tick_fetch_loop.is_running()

    def _parse_config_filename(self) -> Path:
        """Creates $_config.json path from $.json path."""
        config_filename = self.ticks_filename.with_name(
            f"{self.ticks_filename.stem}_config.json"
        )
        return config_filename

    def _read_config(self) -> None:
        """Reads values from $_config.json and assigns them to variables."""
        config_filename = self._parse_config_filename()
        try:
            with open(Path(config_filename)) as f:
                config = json.load(f)
                self._validate_config(config)
                self.tickrate = self._sanitize_tickrate(config["tickrate"])
                self.total_ticks = config["total_ticks"]
                self.map_name = config["map_name"]
        except KeyError as e:
            self._log(f"Config validation error: {e}", level="error")
        except Exception as e:
            self._log(f"{msg.FILE_CONFIG_ERROR}: {e}", level="error")

    def _init_values(self) -> None:
        """Init required variables before streaming can be started."""
        self.ticks = self._ticks_chopper()
        self.tick_fetch_interval = self._calc_fetch_interval(self.tickrate)

    def _calc_fetch_interval(self, tickrate: int) -> float:
        """Takes tickrate and converts it to fetch_interval (ms), used in fetching ticks."""
        tickrate = self._sanitize_tickrate(tickrate)
        fetch_interval: float = 1000 / tickrate
        return fetch_interval

    def _end_of_file(self) -> None:
        """Handles the end of the tick data file."""
        IOLoop.current().add_callback(self._transmit_tick, "EOF")
        self.tick_fetch_loop.stop()
        self._log(f"{msg.STREAM_ENDED}", level="warning")

    def _burst_ticks(self, client) -> None:
        """Send a burst of ticks to a specific client."""
        self._log(f"Sending tick burst of {self.burst_size} ticks")
        ticks_sent = 0
        tick_batch = []
        last_tick_number = client.last_tick_sent
        try:
            for _ in range(self.burst_size):
                try:
                    tick = next(self.ticks)
                    filtered_tick = json.loads(tick)
                    tick_batch.append(filtered_tick)
                    ticks_sent += 1
                except StopIteration:
                    self._end_of_file()
                    break
            self._send_burst_data(
                client, tick_batch, ticks_sent, last_tick_number
            )
        except Exception as e:
            self._log(f"Error sending tick burst: {e}", level="error")
            self.connected_clients.discard(client)

    def _send_burst_data(
        self, client, tick_batch: list, ticks_sent: int, last_tick_number: int
    ) -> None:
        """Helper method to send burst data to a client."""
        burst_data = {
            "type": "tick_burst",
            "ticks": tick_batch,
            "count": ticks_sent,
        }
        IOLoop.current().add_callback(self._transmit_tick, burst_data)
        client.last_tick_sent = last_tick_number
        self._log(
            f"Sent {ticks_sent} ticks in burst to client (last tick: {last_tick_number})"
        )

    async def _transmit_tick(self, tick: dict) -> None:
        """Transmit a tick to client."""
        if self.connected_clients:
            for client in list(self.connected_clients):
                try:
                    await client.write_message(tick)  # Send as JSON object
                except Exception:
                    self.connected_clients.discard(client)

    def _ticks_chopper(self) -> ijson.items:
        """Chops ticks from JSON data.

        This function uses Iterative JSON library for reading
        a large JSON files directly from hard-drive, without first loading
        it to main memory. Handles loop mode if enabled.
        """
        while True:
            with open(self.ticks_filename, "r") as file:
                for tick in ijson.items(
                    file,
                    "ticks.item",
                    use_float=True,
                ):
                    yield json.dumps(tick)
            if not self.loop_mode:
                break
            self._log(f"{msg.STREAM_LOOP_MODE}")

    def ticks_file(self, ticks_filename: Path) -> Path:
        """Handles the input file for $.json (ticks)."""
        self.ticks_filename = ticks_filename
        self._log(f"{msg.STREAM_INPUT_FILE}: {self.ticks_filename}")
        return ticks_filename

    def start_server(
        self,
        srv_address: str,
        srv_port: int,
        srv_endpoint: str,
        loop_mode: bool = False,
        burst_size: int = 640,
    ) -> None:
        """Starts the demo data server."""
        # Init values from arguments
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.srv_endpoint = srv_endpoint
        self.loop_mode = loop_mode
        self.burst_size = burst_size
        # Read demo data config file
        self._read_config()
        # Init rest of variables
        self._init_values()
        # Init the demo data server
        app = Application(
            [(self.srv_endpoint, DemoDataWSH, dict(server=self))]
        )
        app.listen(self.srv_port, self.srv_address)
        self._log(f"{msg.SERVER_START} @ {self._server_info()}")
        self._log(f"{msg.CLIENT_CAN_CONNECT}")
        # Start main loop
        IOLoop.current().start()
