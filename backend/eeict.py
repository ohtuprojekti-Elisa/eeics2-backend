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
    settings = json.load(f)


def get_relative_path(filename: str) -> Path:
    """"""
    demofile_folder = "demofiles"
    full_path = Path(__file__).parent / demofile_folder / filename
    if not full_path.exists():
        logging.error(f"File {filename} does not exist.")
        return Path()
    relative_path = full_path.relative_to(Path(__file__).parent)
    return relative_path


def parser_process(filename: Path, queue: Queue) -> None:
    """"""
    demodata_parser = DemodataParser()
    demodata_parser.demofile(filename)
    parser_status = demodata_parser.parse()
    parsed_filename = demodata_parser.parse_filename()
    queue.put((parser_status, parsed_filename))


def server_process(filename: Path, developer_mode: bool) -> None:
    """"""
    demodata_server = DemodataServer(
        settings["srv_address"],
        settings["srv_port"],
        settings["srv_endpoint"],
        developer_mode,
    )
    demodata_server.demodata_input(filename)
    demodata_server.start_server()


def get_arguments():
    """"""
    parser = argparse.ArgumentParser(
        description="Process and stream CS2 demodata file."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="input CS2 demodata filename: -f mirage.dem",
    )
    parser.add_argument(
        "-d",
        "--developer",
        action="store_true",
        help="enter developer mode (bool), skips parser, use custom JSON: -d -f dev.json",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Set arguments
    args = get_arguments()
    filename = get_relative_path(args.file)
    developer_mode = args.developer

    # Start processes
    process_queue = Queue()
    if not developer_mode and filename is not None:
        parser_proc = Process(
            target=parser_process, args=(filename, process_queue)
        )
        parser_proc.start()
        parser_proc.join()
        parser_status, parsed_filename = process_queue.get()
        filename = parsed_filename
    else:
        parser_status = True

    if (parser_status or developer_mode) and filename is not None:
        server_proc = Process(
            target=server_process, args=(filename, developer_mode)
        )
        server_proc.start()
        server_proc.join()
    else:
        logging.error(f"ORCHESTRATOR - Something went wrong!")
