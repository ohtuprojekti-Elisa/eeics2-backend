import json
import logging
import argparse
from pathlib import Path
from demodata_parser import DemodataParser
from demodata_server import DemodataServer
from multiprocessing import Process, Queue

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load settings file
with open(Path(__file__).parent / "settings.json") as f:
    settings_file = json.load(f)


def get_arguments() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process and stream given CS2 demodata file to EEICT-client. "
        "Arguments can be combined i.e.: -lof mirage.dem (reparses and loops mirage.dem)"
    )
    parser.add_argument(
        "-f",
        type=str,
        required=True,
        dest="filename",
        help="input CS2 demodata filename: -f mirage.dem",
    )
    parser.add_argument(
        "-l",
        dest="loop",
        action="store_true",
        required=False,
        default=False,
        help="enter loop mode to stream until stopped: -l -f mirage.dem",
    )
    parser.add_argument(
        "-o",
        dest="overwrite",
        action="store_true",
        required=False,
        default=False,
        help="overwrites previously parsed JSON files: -o -f mirage.med",
    )
    parser.add_argument(
        "-p",
        dest="frame",
        type=int,
        required=False,
        default=1,
        help='play Nth frame, i.e. "-p 2" plays every 2nd frame: -p 2 -f mirage.med',
    )
    return parser.parse_args()


def get_relative_path(
    filename: str,
) -> Path:
    """Get the relative path of the demodata file."""
    demofile_folder = "demofiles"
    full_path = Path(__file__).parent / demofile_folder / filename
    if not full_path.exists():
        logging.error(f"File {filename} does not exist.")
        return Path()
    relative_path = full_path.relative_to(Path(__file__).parent)
    return relative_path


def parser_process(
    filename: Path,
    overwrite: bool,
    queue: Queue,
) -> None:
    """Run the parser process on the demodata file."""
    demodata_parser = DemodataParser()
    demodata_parser.demofile(filename, overwrite)
    parser_status = demodata_parser.parse()
    parsed_filename = demodata_parser.parse_filename()
    queue.put((parser_status, parsed_filename))


def server_process(
    filename: Path,
    loop_mode: bool,
    play_nth: int,
) -> None:
    """Run the server process to stream the demodata."""
    demodata_server = DemodataServer()
    demodata_server.ticks_file(filename)
    demodata_server.start_server(
        settings_file["srv_address"],
        settings_file["srv_port"],
        settings_file["srv_endpoint"],
        loop_mode,
    )


def start_processes(
    filename: Path,
    overwrite: bool,
    loop_mode: bool,
    play_nth: int,
) -> None:
    """Start the parser and server processes."""
    process_queue = Queue()
    # Parser
    if filename is not None:
        parser_proc = Process(
            target=parser_process, args=(filename, overwrite, process_queue)
        )
        parser_proc.start()
        parser_proc.join()
        parser_status, parsed_filename = process_queue.get()
        filename = parsed_filename
    else:
        parser_status = True
    # Server
    if (parser_status or loop_mode) and filename is not None:
        server_proc = Process(
            target=server_process, args=(filename, loop_mode, play_nth)
        )
        server_proc.start()
        server_proc.join()
    else:
        logging.error(f"ORCHESTRATOR - Something went wrong!")


if __name__ == "__main__":
    # Set arguments
    args = get_arguments()
    filename = get_relative_path(args.filename)
    loop_mode = args.loop
    overwrite_mode = args.overwrite
    play_nth = args.frame

    # Start processes
    start_processes(filename, overwrite_mode, loop_mode, play_nth)
