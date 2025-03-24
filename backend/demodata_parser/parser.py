import ctypes
import logging
from pathlib import Path
from . import messages as msg


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DemodataParser:
    """A parser for CS2-demodata files that uses an external Go-based library."""

    def __init__(self):
        self.class_name = "PARSER"  # Temp before custom logger is implemented
        self.demo_filename: Path = Path()
        self.json_filename: Path = Path()
        self.overwrite: bool = False
        self.parsing_result = False

    def _ext_parser(self) -> None:
        """Uses an external Go based library to parse the demo file."""
        library_path = str(Path(__file__).parent / "demoparser.so")
        demoparser = ctypes.CDLL(library_path)
        demoparser.ParseDemo.argtypes = [ctypes.c_char_p]
        demoparser.ParseDemo.restype = ctypes.c_bool
        self.parsing_result = demoparser.ParseDemo(
            ctypes.c_char_p(str(self.demo_filename).encode("utf-8"))
        )

    def demofile(self, filename: Path, overwrite: bool = False) -> Path:
        """Checks that the file extension is .dem and sets overwrite status."""
        if filename.suffix != ".dem":
            raise ValueError(msg.INVALID_DEMOFILE)
        self.demo_filename = filename
        self.overwrite = overwrite
        return self.demo_filename

    def parse_filename(self) -> Path:
        """Replaces .dem with .json in filename."""
        json_filepath = (
            str(self.demo_filename)
            .encode("utf-8")
            .decode("utf-8")
            .replace(".dem", ".json")
            .encode("utf-8")
        )
        self.json_filename = Path(json_filepath.decode("utf-8"))
        return self.json_filename

    def parse(self) -> bool:
        """Initiates the parsing process and handles the result."""
        self.parse_filename()
        if self.json_filename.exists() and self.overwrite == False:
            logging.info(
                f"{self.class_name} - {self.json_filename} {msg.PARSE_SKIP}"
            )
            return True
        else:
            logging.info(
                f"{self.class_name} - {self.demo_filename} {msg.PARSE_STARTING}"
            )
        # Initiate external parser
        self._ext_parser()
        if self.parsing_result:
            logging.info(
                f"{self.class_name} - {msg.PARSE_COMPLETED}: {self.demo_filename}"
            )
            return True
        else:
            logging.warning(
                f"{self.class_name} - {msg.PARSE_FAILED}: {self.demo_filename}"
            )
            return False
