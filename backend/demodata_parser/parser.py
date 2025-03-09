import ctypes
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DemodataParser:
    """"""

    def __init__(self, filename):
        self.class_name = "PARSER"
        self.filename = filename
        self.json_filename = self.parse_filename()

    def parse_filename(self):
        """Changes .dem to .json and creates a Path object"""
        json_filepath = (
            self.filename.decode("utf-8")
            .replace(".dem", ".json")
            .encode("utf-8")
        )
        json_filepath = Path(json_filepath.decode("utf-8"))
        return json_filepath

    def parse_demo(self):
        """"""
        if self.json_filename.exists():
            logging.info(
                f"{self.class_name} - File: {self.json_filename} already exists, skipping!"
            )
            return
        else:
            logging.info(
                f"{self.class_name} - Starting a new demofile parsing for: {self.filename}"
            )

        # Demoparser Go-library related
        library_path = str(Path(__file__).parent / "demoparser.so")
        demoparser = ctypes.CDLL(library_path)
        demoparser.ParseDemo.argtypes = [ctypes.c_char_p]
        demoparser.ParseDemo.restype = ctypes.c_bool
        parsing_result = demoparser.ParseDemo(self.filename)

        if parsing_result:
            logging.info(f"{self.class_name} - Demofile parsing successful!")
        else:
            logging.warning(f"{self.class_name} - Demofile parsing failed!")


if __name__ == "__main__":
    # Only for quick testing, to be deprecated
    filename = "mirage.dem".encode("utf-8")
    parser = DemodataParser(filename)
    parser.parse_demo()
