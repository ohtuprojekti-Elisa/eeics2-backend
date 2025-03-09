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
    relative_path = full_path.relative_to(Path(__file__).parent)
    return str(relative_path).encode("utf-8")


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description="Process demodata file.")
    parser.add_argument(
        "-f", "--file", type=str, required=True, help="CS2 demodata filename"
    )
    args = parser.parse_args()

    # Parser
    demodata_filename = get_relative_path(args.file)
    demodata_parser = DemodataParser(demodata_filename)
    parser_status = demodata_parser.parse_demo()

    # Server
    if parser_status:
        json_filename = demodata_parser.parse_filename()
        demodata_server = DemodataServer("0.0.0.0", 8080, "/demodata")
        demodata_server.demodata_input(json_filename)
        demodata_server.start_server()
    else:
        logging.warning(f"ORCHESTRATOR - Something went wrong!")
