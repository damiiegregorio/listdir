# lisdir write-to-db

### Machine Problem

* Create a new argument where it will give the functionality of writing to a PostgreSQL DB instead of writing to a file
* The password should be passed as command line arguments. Note the secure way of passing passwords as command line arguments
* The hostname and username should be in the config
* Use a local installation of PostgreSQL during development


### Configuration
#### Change database name config.yaml
```
mysql:
    host: <host>
    user: <username>
    db: <database_name>
    port: <port>
```


### Running the program
#### Create database
```
python listdir.py <PATH> -d
```

#### Create a table
```
python listdir.py <PATH> -t
```

#### Write files to database
```
python listdir.py <PATH> -d
```

### Built With
* Python v3.7
* <b>IDE</b> - Jetbrains PyCharm Community Edition 2019
