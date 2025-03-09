from pathlib import Path
from demodata_parser import DemodataParser
from demodata_server import DemodataServer


def get_relative_path(filename):
    """"""
    demofile_folder = "demofiles"
    full_path = Path(__file__).parent / demofile_folder / filename
    relative_path = full_path.relative_to(Path(__file__).parent)
    return str(relative_path).encode("utf-8")


if __name__ == "__main__":
    # Parser
    demodata_filename = get_relative_path("mirage.dem")
    demodata_parser = DemodataParser(demodata_filename)
    demodata_parser.parse_demo()

    # Server
    demodata_server = DemodataServer("0.0.0.0", 8080, "/demodata")
    demodata_server.demodata_input("./demofiles/mirage.json")
    demodata_server.start_server()
