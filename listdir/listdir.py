import os
import csv
import argparse
import hashlib
import configparser
from zipfile import ZipFile
from datetime import datetime
import logging
import logging.config
import yaml
import json


def setup_yaml():
    """Setup logging configuration """
    default_level = logging.DEBUG
    yaml_path = 'config.yaml'
    value = os.getenv("LOG_CFG", None)

    if value:
        yaml_path = value
    if os.path.exists(yaml_path):
        with open(yaml_path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level, filename="debug.log")
    else:
        logging.basicConfig(level=default_level, filename="debug.log")
        print('Failed to load configuration file. Using default configs')


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


def date_today(csv_name):
    today = datetime.now().strftime("_%Y%m%d_%I-%M_%p")
    filename = csv_name + today
    return filename


def zip_file(filename):

    zipped_file = filename + ".zip"
    with ZipFile(zipped_file, 'w') as zipObj:
        zipObj.write(filename + '.csv')
    return zipObj


def csv_file(data, filename):
    with open(filename + ".csv", 'a', newline='') as output_file:
        writer = csv.writer(output_file, lineterminator='\r')
        writer.writerow(data)
        return filename


def json_file(file_path, csv_name):
    data_list = []
    data_dict = {"files": data_list}

    with open(csv_name+'.json', 'a') as json_file:
        for r, d, f in os.walk(file_path):
            for file in f:
                dir_path = os.path.abspath(r)
                name = os.path.basename(file)
                file_stat = os.path.getsize("{}{}{}".format(r, os.sep, file))
                hash_path = os.path.abspath("{}{}{}".format(r, os.sep, file))
                sha1 = extract_sha1(hash_path)
                md5 = extract_md5(hash_path)
                data = {
                    "path": dir_path,
                    "filename": name,
                    "file_size": file_stat,
                    "sha1": sha1,
                    "md5": md5
                }
                logger.debug(data)
                data_list.append(data)
        json.dump(data_dict, json_file, indent=2)


def csv_write(file_path, filename):
    """CSV File writer"""
    for r, d, f in os.walk(file_path):
        for file in f:
            dir_path = os.path.abspath(r)
            name = os.path.basename(file)
            file_stat = os.path.getsize("{}{}{}".format(r, os.sep, file))
            hash_path = os.path.abspath("{}{}{}".format(r, os.sep, file))
            sha1 = extract_sha1(hash_path)
            md5 = extract_md5(hash_path)
            data = [dir_path, name, file_stat, sha1, md5]

            logger.debug(data)

            """Create csv file"""
            csv_file(filename, data)

            """Create zip file"""
            zip_file(filename)


def main():
    try:
        """ConfigParser"""
        config = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        config.read(path + '/config.ini')

        """Argument Parser"""
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        parser.add_argument("file_path", nargs='?')
        parser.add_argument("csv_name", type=str)
        group.add_argument("-j", "--json", help="Create a json file", action="store_true")
        args = parser.parse_args()

        if args.file_path is None and args.csv_name is None:
            """config.ini file ['section']['name]"""
            csv_write(config['DEFAULT']['file_path'], config['DEFAULT']['filename'])
            print("------Action completed------")
        elif args.json:
            json_file(args.file_path, args.csv_name)
            print("------Json file completed------")
        else:
            csv_write(args.file_path, args.csv_name)
            print("------Action completed------")

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    setup_yaml()
    logger = logging.getLogger(__name__)
    main()

