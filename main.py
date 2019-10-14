import os
import csv
import argparse
import hashlib
import configparser
from zipfile import ZipFile
files = []


def csv_write(file_path, csv_name):
    """CSV File writer"""
    for r, d, f in os.walk(file_path):
        for file in f:
            dir_path = os.path.abspath(r)
            name = os.path.basename(file)
            file_stat = os.path.getsize("{}\{}".format(r, file))
            hash_path = os.path.abspath("{}\{}".format(r, file))

            """Extract sha1 and md5"""
            sha1_extractor = hashlib.sha1()
            md5_extractor = hashlib.md5()

            with open(hash_path, 'rb') as afile:
                buf = afile.read()
                sha1_extractor.update(buf)
                md5_extractor.update(buf)
                sha1 = sha1_extractor.hexdigest()
                md5 = md5_extractor.hexdigest()

            data = [dir_path, name, file_stat, sha1, md5]

            """Create csv file"""
            with open(csv_name+".csv", 'a') as output_file:
                writer = csv.writer(output_file, lineterminator='\r')
                writer.writerow(data)

            """Create zip file"""
            with ZipFile(csv_name+".zip", 'w') as zipObj:
                zipObj.write(csv_name+'.csv')

    """Remove csv file"""
    os.remove(csv_name+'.csv')


def main():
    try:
        """ConfigParser"""
        config = configparser.ConfigParser()
        config.read('config.ini')

        """Argument Parser"""
        parser = argparse.ArgumentParser()
        parser.add_argument("file_path", nargs='?')
        parser.add_argument("csv_name", nargs='?')
        args = parser.parse_args()

        if args.file_path and args.csv_name:
            csv_write(args.file_path, args.csv_name)
        else:
            """config.ini file ['section']['name]"""
            csv_write(config['DEFAULT']['file_path'], config['DEFAULT']['csv_name'])

    except IndexError:
        print("Error!")


if __name__ == "__main__":
    main()
