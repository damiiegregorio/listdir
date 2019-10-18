import os
import csv
import argparse
import hashlib
import configparser
from zipfile import ZipFile
from datetime import datetime


def extract_sha1(hash_path):
    """Extract sha1"""
    sha1_extractor = hashlib.sha1()

    with open(hash_path, 'rb') as afile:
        buf = afile.read()
        sha1_extractor.update(buf)
        sha1 = sha1_extractor.hexdigest()
    return sha1


def extract_md5(hash_path):
    """Extract sha1"""
    md5_extractor = hashlib.md5()

    with open(hash_path, 'rb') as afile:
        buf = afile.read()
        md5_extractor.update(buf)
        md5 = md5_extractor.hexdigest()
    return md5


def csv_write(file_path, csv_name):
    """CSV File writer"""
    for r, d, f in os.walk(file_path):
        for file in f:
            dir_path = os.path.abspath(r)
            name = os.path.basename(file)
            file_stat = os.path.getsize("{}\{}".format(r, file))
            hash_path = os.path.abspath("{}\{}".format(r, file))
            sha1 = extract_sha1(hash_path)
            md5 = extract_md5(hash_path)
            data = [dir_path, name, file_stat, sha1, md5]

            today = datetime.now().strftime("_%Y%m%d_%I-%M_%p")
            filename = csv_name + today

            """Create csv file"""
            with open(filename+".csv", 'a', newline='') as output_file:
                writer = csv.writer(output_file, lineterminator='\r')
                writer.writerow(data)

            """Create zip file"""
            with ZipFile(filename+".zip", 'w') as zipObj:
                zipObj.write(filename+'.csv')


def main():
    try:
        """ConfigParser"""
        config = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        config.read(path + '/config.ini')

        """Argument Parser"""
        parser = argparse.ArgumentParser()
        parser.add_argument("file_path", nargs='?')
        parser.add_argument("csv_name", nargs='?')
        args = parser.parse_args()

        if args.file_path and args.csv_name:
            csv_write(args.file_path, args.csv_name)
            print("Success!")
        else:
            """config.ini file ['section']['name]"""
            csv_write(config['DEFAULT']['file_path'], config['DEFAULT']['filename'])
            print("Success!")

    except IndexError:
        print("Error!")


if __name__ == "__main__":
    main()