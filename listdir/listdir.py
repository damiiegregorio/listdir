import os
import csv
import argparse
import hashlib
import configparser
import logging
import logging.config
import yaml
import json
import getpass
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pika

yaml_file = 'config.yaml'


def publish_queue(file_path):
    global yaml_file
    with open(yaml_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    rabbit_mq = config['rabbitmq']

    # Create a new instance of the Connection object
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq['host']))
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_mq['queue'])
    json_data = json_file(file_path)
    data = json_data['files']
    for message in data:
        channel.basic_publish(exchange='',
                              routing_key='listdir',
                              body=json.dumps(message),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))
        logger.info("Sent {}".format(message))
    connection.close()


def create_db():
    global yaml_file
    with open(yaml_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    mysql = config['mysql']

    pwd = getpass.getpass()
    connection = psycopg2.connect(
        user=mysql['user'],
        password=pwd,
        host=mysql['host'],
        port=mysql['port'],
    )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

    cur = connection.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(mysql['db']))
    )
    logger.info("Database created.")


def create_table():
    try:
        global yaml_file
        with open(yaml_file, 'rt') as f:
            config = yaml.safe_load(f.read())
        mysql = config['mysql']

        pwd = getpass.getpass()
        connection = psycopg2.connect(
            user=mysql['user'],
            password=pwd,
            host=mysql['host'],
            port=mysql['port'],
            database=mysql['db'],
        )

        # Create cursor
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE files
            (ID       SERIAL  PRIMARY KEY     NOT NULL,
            PATH              varchar         NOT NULL,
            FILENAME          varchar         NOT NULL,
            SIZE              int             NOT NULL,
            SHA1              varchar         NOT NULL,
            MD5               varchar         NOT NULL); 
        """

        cursor.execute(create_table_query)
        connection.commit()
        logger.info("Table created successfully in PostgreSQL")
        return True

    except (Exception, psycopg2.Error) as error:
        logger.error("Error while connecting to PostgreSQL", error)


def list_to_db(file_path):
    try:
        global yaml_file
        with open(yaml_file, 'rt') as f:
            config = yaml.safe_load(f.read())
        mysql = config['mysql']

        pwd = getpass.getpass()
        connection = psycopg2.connect(
            user=mysql['user'],
            password=pwd,
            host=mysql['host'],
            port=mysql['port'],
        )

        cursor = connection.cursor()
        cursor.execute("select exists(SELECT datname FROM pg_catalog.pg_database WHERE datname = '{}');".format(mysql['db']))
        db_exists = cursor.fetchone()[0]
        if db_exists is False:
            logger.info("Database does not exist.")
            logger.info("Please make a database using the '-d' command")
        else:
            logger.info("Preparing your data...")
            connection = psycopg2.connect(
                user=mysql['user'],
                password=pwd,
                host=mysql['host'],
                port=mysql['port'],
                database=mysql['db'],
            )
            cursor = connection.cursor()

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

                    postgres_insert_query = """
                        INSERT INTO files
                        (PATH, FILENAME, SIZE, SHA1, MD5)
                        VALUES (%s,%s,%s,%s,%s)
                    """
                    record_to_insert = (dir_path, name, file_stat, sha1, md5)
                    cursor.execute(postgres_insert_query, record_to_insert)
                    connection.commit()
                    logger.info("Record inserted successfully into file table")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def create_all():
    logger.info("Creating database with 'files' table.")
    create_db()
    create_table()
    return True


def setup_yaml():
    """Setup logging configuration """
    global yaml_file
    default_level = logging.DEBUG
    value = os.getenv("LOG_CFG", None)

    if value:
        yaml_file = value
    if os.path.exists(yaml_file):
        with open(yaml_file, 'rt') as f:
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


def json_file(file_path):
    data_list = []
    data_dict = {"files": data_list}

    with open('output.json', 'a') as json_file:
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
                # logger.debug(data)
                data_list.append(data)
        json.dump(data_dict, json_file, indent=2)
    return data_dict


def csv_write(file_path):
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
            with open("output.csv", 'a', newline='') as output_file:
                writer = csv.writer(output_file, lineterminator='\r')
                writer.writerow(data)


def main():
    try:
        """ConfigParser"""
        config = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        config.read(path + '/config.ini')

        """Argument Parser"""
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        parser.add_argument("file_path", nargs='?', help="File path",)
        group.add_argument("-j", "--json", help="Create a json file", action="store_true")
        group.add_argument("-c", "--csv", help="Create a csv file", action="store_true")
        group.add_argument("-w", "--write", help="Write to DB", action="store_true")
        group.add_argument("-d", "--create_db", help="Create database and table", action="store_true")
        group.add_argument("-q", "--publish", help="Send to queue", action="store_true")
        args = parser.parse_args()

        if args.file_path is None and args.csv_name is None:
            """config.ini file ['section']['name]"""
            csv_write(config['DEFAULT']['file_path'])
            logger.info("CSV file created successfully..")
        elif args.csv:
            logger.info("Creating csv file...")
            csv_write(args.file_path)
            logger.info("CSV file created successfully.")
        elif args.json:
            logger.info("Creating json file...")
            json_file(args.file_path)
            logger.info("JSON file created successfully.")
        elif args.write:
            list_to_db(args.file_path)
        elif args.create_db:
            create_all()
        elif args.publish:
            logger.info("Sending files metadata to listdir queue..")
            publish_queue(args.file_path)
        else:
            logger.info("Creating csv file...")
            csv_write(args.file_path)
            logger.info("CSV file created successfully.")

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    setup_yaml()
    logger = logging.getLogger(__name__)
    main()
