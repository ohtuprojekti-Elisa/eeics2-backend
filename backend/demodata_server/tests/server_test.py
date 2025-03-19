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
        self.filename = Path("test.json")

    def test_demodata_input(self):
        # Arrange
        expected_output = self.filename
        # Act
        output = self.demodata_server.demodata_input(self.filename)
        # Assert
        assert output == expected_output

    def test_stream_start(self):
        # Arrange
        expected_output = False
        # Act
        output = self.demodata_server._stream_start()
        # Assert
        assert output == expected_output

    def test_stream_pause(self):
        # Arrange
        self.demodata_server._stream_start()
        expected_output = False
        # Act
        output = self.demodata_server._stream_pause()
        # Assert
        assert output == expected_output

    def test_total_clients(self):
        # Arrange
        expected_output = 0
        # Act
        output = len(self.demodata_server.connected_clients)
        # Assert
        assert output == expected_output
