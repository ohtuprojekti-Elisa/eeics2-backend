import ctypes
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DemodataParser:
    """"""

    def __init__(self):
        self.class_name = "PARSER"  # Temp before custom logger is implemented
        self.demo_filename: Path = Path()
        self.json_filename: Path = Path()
        self.msg_demofile_error = "Please input CS2 demofile (.dem)"

    def demofile(self, filename: Path) -> Path:
        """Checks that the file extension is .dem"""
        if filename.suffix != ".dem":
            raise ValueError(self.msg_demofile_error)
        self.demo_filename = filename
        return self.demo_filename

    def parse_filename(self) -> Path:
        """Replaces .dem with .json"""
        json_filepath = (
            str(self.demo_filename)
            .encode("utf-8")
            .decode("utf-8")
            .replace(".dem", ".json")
            .encode("utf-8")
        )
        self.json_filepath = Path(json_filepath.decode("utf-8"))
        return self.json_filepath

    def parse(self) -> bool:
        """"""
        self.parse_filename()
        if self.json_filename.exists():
            logging.info(
                f"{self.class_name} - JSON file '{self.json_filename}' already exists, skipping!"
            )
            return True
        else:
            logging.info(
                f"{self.class_name} - Starting new demofile parse for: '{self.demo_filename}'"
            )

        # Demoparser Go-library related
        library_path = str(Path(__file__).parent / "demoparser.so")
        demoparser = ctypes.CDLL(library_path)
        demoparser.ParseDemo.argtypes = [ctypes.c_char_p]
        demoparser.ParseDemo.restype = ctypes.c_bool
        parsing_result = demoparser.ParseDemo(self.demo_filename)

        if parsing_result:
            logging.info(
                f"{self.class_name} - Demofile '{self.demo_filename}' parsed successfully!"
            )
            return True
        else:
            logging.warning(f"{self.class_name} - Demofile parsing failed!")
            return False
