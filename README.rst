list-dir
------------------
lisdir-with-hashes is a python module that

* can list the files, sha1 and md5 in a csv file of a recursive directory path.
* It also compresses the output csv file into a zip file.
* Date and time is included in the filename


To use (listdir), simply do::

    >>> import listdir
    >>> listdir.csv_write(r"<PATH>", r"<filename>")


You can also run the function directly.
This command will still support the arguments for the value of the input directory and output file::

    >>> pip install .
    >>> listdir


