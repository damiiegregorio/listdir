from unittest import TestCase
import listdir


class TestJoke(TestCase):
    def test_is_string(self):
        s = listdir.csv_write(r"C:\Users\TEU_USER\packaging\test\test_directory", r"output_test")
        self.assertTrue(isinstance(s))
