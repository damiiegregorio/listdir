import os
import csv
import argparse
import sys
from pathlib import Path

files = []


def csv_write(file_path, csv_name):
    """CSV File writer"""
    for r, d, f in os.walk(file_path):
        for file in f:
            dir_path = os.path.abspath(r)
            name = os.path.basename(file)
            file_stat = os.path.getsize("{}\{}".format(r, file))
            data = [dir_path, name, file_stat]

            with open(csv_name+".csv", 'a') as output_file:
                writer = csv.writer(output_file, lineterminator='\r')
                writer.writerow(data)


def main():
    """Argument Parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)
    parser.add_argument("csv_name", type=str)
    args = parser.parse_args()

    if args.file_path.exists():
        print("Path exists!")
        csv_write(args.file_path, args.csv_name)
    else:
        print("Path does not exist.")


if __name__ == "__main__":
    main()
