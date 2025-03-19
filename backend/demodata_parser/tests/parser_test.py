import unittest
from pathlib import Path
from demodata_parser import DemodataParser, messages


class TestDemodataParser(unittest.TestCase):

    def setUp(self) -> None:
        self.demo_filename = Path("test.dem")
        self.json_filename = Path("test.json")
        self.parser = DemodataParser()

    def test_demofile_true(self):
        # Arrange
        expected_output = self.demo_filename
        # Act
        output = self.parser.demofile(self.demo_filename)
        # Assert
        assert output == expected_output

    def test_demofile_false(self):
        # Arrange
        expected_output = messages.INVALID_DEMOFILE
        error_input = Path("testfile.xyz")
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.parser.demofile(error_input)
        self.assertEqual(str(context.exception), expected_output)

    def test_parse_filename_true(self):
        # Arrange
        expected_output = self.json_filename
        self.parser.demofile(self.demo_filename)
        # Act
        output = self.parser.parse_filename()
        # Assert
        assert output == expected_output
