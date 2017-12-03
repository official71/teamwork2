# Association Rules

## Group UNI

## List of files

* __data.py__: maps original CSV data items into integers
* __apriori.py__: implements the Apriori algorithm to find large itemsets
* __rules.py__: generates association rules from given itemsets
* __main.py__: contains main function

## Prerequisites and usage

* Platform: Google Cloud VM, Ubuntu 14.04
* Python package: __argparse__ for argument parsing, install by running `sudo pip install argparse` in Bash
* Main function help information:

```
$ python main.py -h
usage: main.py [-h] csvname min_supp min_conf

Data Mining using Apriori algorithm

positional arguments:
  csvname     name of the CSV file that contains data
  min_supp    minimal support value (range 0 to 1)
  min_conf    minimal confidence value (range 0 to 1)

optional arguments:
  -h, --help  show this help message and exit
```

## Data specifications

1. NYC Open Data

1. Data mapping procedure

    1. p1

    2. p2

1. Reason of choice

## Detailed design

## Sample run

