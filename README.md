# lisdir-with-hashes
#### Version 1.1

lisdir-with-hashes is a python module that can list the files, sha1 and md5 in a csv file of a recursive directory path. It also compresses the output csv file into a zip file


### Machine Problem

* Add 2 new columns to the output: md5 and sha1
* The data under these columns should include the respective hashes of the file
* The output file should be zipped
* If the user set the output filename to be out.txt, it should now output out.txt.zip


## New Features: 
* Columns for MD5 and SHA1
* Output file is zipped.



### Built With
* Python v3.7
* <b>IDE</b> - Jetbrains PyCharm Community Edition 2019


### Running the program
```

python main.py <PATH> <csv_name>

```
