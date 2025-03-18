import unittest
from pathlib import Path
from demodata_server import DemodataServer


class TestDemodataServer(unittest.TestCase):

    def setUp(self) -> None:
        self.srv_address = "0.0.0.0"
        self.srv_port = 8080
        self.srv_endpoint = "/test"
        self.developer_mode = False
        self.demodata_server = DemodataServer(
            self.srv_address,
            self.srv_port,
            self.srv_endpoint,
            self.developer_mode,
        )

    def test_parse_filename(self):
        # Arrange
        test_input = Path("test.json")
        test_output = test_input

        # Act
        output = self.demodata_server.demodata_input(test_input)

        # Assert
        assert output == test_output

    def test_stream_pause(self):
        # Arrange
        self.demodata_server.stream_start()
        test_output = False

        # Act
        output = self.demodata_server.stream_pause()

        # Assert
        assert output == test_output
