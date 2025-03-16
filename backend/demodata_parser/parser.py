import ctypes
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DemodataParser:
    """"""

    def __init__(self, filename: Path):
        self.class_name = "PARSER"  # Temp before custom logger is implemented
        self.filename = filename
        self.decoded_filename = self.filename
        self.json_filename = self.parse_filename()

    def parse_filename(self):
        """Changes .dem to .json and creates a Path object"""
        json_filepath = (
            str(self.filename)
            .encode("utf-8")
            .decode("utf-8")
            .replace(".dem", ".json")
            .encode("utf-8")
        )
        json_filepath = Path(json_filepath.decode("utf-8"))
        return json_filepath

    def parse_demo(self):
        """"""
        if self.json_filename.exists():
            logging.info(
                f"{self.class_name} - JSON file '{self.json_filename}' already exists, skipping!"
            )
            return True
        else:
            logging.info(
                f"{self.class_name} - Starting new demofile parse for: '{self.decoded_filename}'"
            )

        # Demoparser Go-library related
        library_path = str(Path(__file__).parent / "demoparser.so")
        demoparser = ctypes.CDLL(library_path)
        demoparser.ParseDemo.argtypes = [ctypes.c_char_p]
        demoparser.ParseDemo.restype = ctypes.c_bool
        parsing_result = demoparser.ParseDemo(self.filename)

        if parsing_result:
            logging.info(
                f"{self.class_name} - Demofile '{self.decoded_filename}' parsed successfully!"
            )
            return True
        else:
            logging.warning(f"{self.class_name} - Demofile parsing failed!")
            return False


if __name__ == "__main__":
    # Only for quick testing, to be deprecated
    filename = Path("mirage.dem")
    parser = DemodataParser(filename)
    parser.parse_demo()
