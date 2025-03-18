import logging
import argparse
from pathlib import Path
from demodata_parser import DemodataParser
from demodata_server import DemodataServer


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_relative_path(filename):
    """"""
    demofile_folder = "demofiles"
    full_path = Path(__file__).parent / demofile_folder / filename
    if not full_path.exists():
        logging.error(f"File {filename} does not exist.")
        return None
    relative_path = full_path.relative_to(Path(__file__).parent)
    return relative_path


if __name__ == "__main__":
    # Arguments
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
    args = parser.parse_args()

    # Set variables
    filename = get_relative_path(args.file)
    developer_mode = args.developer
    parser_status = False

    # Parser
    if not developer_mode and filename is not None:
        demodata_parser = DemodataParser()
        demodata_parser.demofile(filename)
        parser_status = demodata_parser.parse()
        filename = demodata_parser.parse_filename()

    # Server
    if (parser_status or developer_mode) and filename is not None:
        demodata_server = DemodataServer(
            "0.0.0.0",
            8080,
            "/demodata",
            developer_mode,
        )
        demodata_server.demodata_input(filename)
        demodata_server.start_server()
    else:
        logging.error(f"ORCHESTRATOR - Something went wrong!")
