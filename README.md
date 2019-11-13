# lisdir write-to-queue

### Machine Problem

* Create a new argument where it will give the functionality of sending the the file metadata (the row in the CSV in a previous Machine Problem) in JSON format to a queue
* The hostname, the name of the queue and the credentials (if needed) should be read from a configuration file
* The module reads from a queue and logs the message to STDOUT and uses the INFO severity (using the logging library)
* The module runs continuously in an infinite loop waiting for messages
    * Hint: The module should "sleep" for a certain amount of seconds (configurable in the config file) if it got not messages in the queue (i.e. the queue is empty)
    
### Configuration
#### Database and RabbitMQ
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
##### Send file metadata to queue
```
python listdir.py <PATH> -q
```

##### Receive file metadata from queue
```
python listdir.py <PATH> -r
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
