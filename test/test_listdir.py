import unittest
from datetime import datetime
import listdir

hash_path = "C:\\Users\\TEU_USER\\listdir\\test_directory\\sample.txt"
test_name = "output_test"


class TestListDir(unittest.TestCase):
    def test_csv_today(self):
        today = datetime.now().strftime("_%Y%m%d_%I-%M_%p")
        file_test = "output_test{}".format(today)
        assert listdir.date_today(test_name) == file_test

    def test_md5(self):
        md5 = "c18c23a4ae40eaa0e92d232ab4a976d1"
        assert listdir.extract_md5(hash_path) == md5

    def test_sha1(self):
        sha1 = "51aa976f9114a6c458e5fe466cfd00ad0cae6450"
        assert listdir.extract_sha1(hash_path) == sha1

    def test_csv(self):
        result = listdir.csv_write(file_path="C:\\Users\\TEU_USER\\listdir\\test\test_directory", filename="test_output")
        assert result is not None


# if __name__ == '__main__':
#     unittest.main()
