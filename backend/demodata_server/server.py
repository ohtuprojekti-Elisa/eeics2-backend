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
        self.srv_port: int = -1
        self.srv_endpoint: str = ""
        self.loop_mode: bool = False
        self.connected_clients: set[DemoDataWSH] = set()
        # Demodata info
        self.tickrate: int = 64
        self.total_ticks: int = -1
        self.map_name: str = ""
        # Ticks
        self.ticks_filename: Path = Path()
        self.ticks: ijson.items = ijson.items
        self.interval_ms: float = 15.625  # Server master clock
        self.current_tick: int = 0  # Server playhead
        # Burst mode
        self.burst_size: int = -1  # Number of ticks/burst
        self.ticks_buffer: list = []
        self.timer_callback = PeriodicCallback(
            self._update_buffer, self.interval_ms
        )

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
        self._stream_start()
        client.write_message(f"{msg.CLIENT_START_STREAM}")
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
            if data.get("request") == "Give more ticks!":
                self._log(f"{msg.CLIENT_REQUEST_MORE_TICKS}: {data}")
                ticks = self._gather_ticks(self.burst_size)
                self._send_burst_data(ticks)
        except json.JSONDecodeError:
            self._log("Invalid message format received.", level="error")
        except Exception as e:
            self._log(f"Error handling client message: {e}", level="error")

    def total_clients(self) -> str:
        """Formats info on clients to a single string."""
        connected_clients = len(self.connected_clients)
        return f"{msg.CLIENT_TOTAL_NUM}: {connected_clients}"

    def _server_info(self) -> str:
        """Formats server info to a single string."""
        return f"{self.srv_address}:{self.srv_port}/{self.srv_endpoint}"

    def _stream_start(self) -> bool:
        """Starts the stream for a client."""
        if len(self.connected_clients) == 1:
            self.timer_callback.start()
        return self.timer_callback.is_running()

    def _stream_pause(self) -> bool:
        """Pause stream if no connected clients."""
        if len(self.connected_clients) == 0:
            if self.timer_callback.is_running():
                self.timer_callback.stop()
                self._log(f"{msg.STREAM_PAUSED}")
        return self.timer_callback.is_running()

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
        self.interval_ms = self._calc_interval_ms(self.tickrate)

    def _calc_interval_ms(self, tickrate: int) -> float:
        """Takes tickrate and converts it to interval (ms), used as a internal clock."""
        tickrate = self._sanitize_tickrate(tickrate)
        interval_ms: float = 1000 / tickrate
        return interval_ms

    def _end_of_file(self) -> None:
        """Handles the end of the tick data file."""
        IOLoop.current().add_callback(self._transmit_ticks, "EOF")
        self._log(f"{msg.STREAM_ENDED}", level="warning")

    def _update_buffer(self) -> None:
        """Update buffers and send data to clients based on the threshold counter."""
        try:
            # Send the first burst of ticks
            if not self.ticks_buffer:
                self.ticks_buffer = self._gather_ticks(self.burst_size)
                self._send_burst_data(self.ticks_buffer)
            # Send concurrent bursts of ticks
            if self.current_tick >= self.burst_size:
                self.ticks_buffer = self._gather_ticks(self.burst_size)
                self._send_burst_data(self.ticks_buffer)
                self.current_tick = 0
            self.current_tick += 1
        except Exception as e:
            self._log(f"Error in buffer update: {e}", level="error")

    def _gather_ticks(self, burst_size: int) -> list:
        """Gather a specified number of ticks."""
        ticks = []
        try:
            for _ in range(burst_size):
                tick = next(self.ticks)
                ticks.append(json.loads(tick))
        except StopIteration:
            self._end_of_file()
        except Exception as e:
            self._log(f"Error gathering ticks: {e}", level="error")
        return ticks

    def _send_burst_data(self, ticks_buffer: list) -> None:
        """Send a batch of ticks to all connected clients."""
        burst_data = {
            "ticks": ticks_buffer,
            "count": len(ticks_buffer),
        }
        for client in list(self.connected_clients):
            IOLoop.current().add_callback(
                self._transmit_ticks, client, burst_data
            )
        self._log(f"{msg.STREAM_SENT_TICKS}: {self.burst_size}")

    async def _transmit_ticks(self, client, tick: dict) -> None:
        """Transmit ticks to client."""
        if self.connected_clients:
            for client in list(self.connected_clients):
                try:
                    await client.write_message(tick)
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
        burst_size: int = 16,
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
