# lisdir write-to-queue

### Machine Problem

* Create a new argument where it will give the functionality of sending the the file metadata (the row in the CSV in a previous Machine Problem) in JSON format to a queue
* The hostname, the name of the queue and the credentials (if needed) should be read from a configuration file


### Configuration
#### Change database name config.yaml
```
mysql:
    host: <host>
    user: <username>
    db: <database_name>
    port: <port>

rabbit_mq:
    host: <host>
    queue: <queue>

```


### Running the program
```
python listdir.py <PATH> -q
```


##### Creating a database
```
python listdir.py <PATH> -d
```

##### Write files to database
```
python listdir.py <PATH> -w
```

### Built With
* Python v3.7
* <b>IDE</b> - Jetbrains PyCharm Community Edition 2019