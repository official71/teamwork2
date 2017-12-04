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

### (a) NYC Open Data

[DOHMH New York City Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j). This dataset provides restaurant inspections, violations, grades and adjudication information.

### (b) Data mapping procedure

    1. In the original CSV data, each row contains information of a single violation during inspection and the restaurant that did the violation. If the restaurant violated multiple terms in one inspection there will be one row for each violation it made. The most important processing to the original data is therefore joining it by `CAMIS`(restaurant ID) and the inspection date so that each row represents the result of one inspection rather than one violation.

    1. A selection of columns in the original data are then mapped to new formats for better representations:

    |Column Name|Description|Mapping|
    |---|---|---|
    |DBA|Name of the restaurant|Add prefix "DBA"|
    |BORO|Borough where the restaurant locates|Add prefix "BORO"|
    |STREET|Name of the street where the restaurant locates|Add prefix "STREET"|
    |CUISINE DESCRIPTION|Describes the cuisine of the restaurant|Add prefix "CUISINE"|
    |INSPECTION DATE|Date of the inspection (MM/DD/YYYY)|Mapped into quarters using the month, e.g. "May": "Q2", "Sep": "Q3"|
    |ACTION|Action taken in each inspection, e.g. "Cited", "Closed"|Add prefix "ACTION"|
    |INSPECTION TYPE|Type of the inspection|Abstract information into smaller categories such as "Initial Inspection" and "Re-inspection"|
    |VIOLATION CODE|Code of the violation defined by [DOHMH](http://www1.nyc.gov/assets/doh/downloads/pdf/rii/blue-book.pdf)||
    |CRITICAL FLAG|Whether violation is critical or not, determined by the Violation Code|Combined with Violation Code to form an instance of violation|
    |SCORE|Total score of an inspection||
    |GRADE|Grade assigned to the restaurant of an inspection, according to the [DOHMH guide](http://www1.nyc.gov/assets/doh/downloads/pdf/rii/how-we-score-grade.pdf), "Restaurants with a score between 0 and 13 points earn an A, those with 14 to 27 points receive a B and those with 28 or more a C"|When grade is missing for an inspection, use the score to determine the grade|

    Columns with redundant or over-specific information are discarded for simplicity.

    1. The mapped data are dumped into `INTEGRATED-DATASET.csv`, reducing the former 396,000 rows of violation data into 137,462 rows of inspection data.

### (c) Reason of choice

* The dataset is among the [most popular ones](https://data.cityofnewyork.us/browse?provenance=official&sortBy=most_accessed&utf8=✓) in NYC Open Data.
* The columns are well-defined and structured, with relatively less missing fields. Even when there is data missing we can derive the missing fields using the rules specified by DOHMH.
* As much as we'd like our food to be delicious, we care about how clean it is. The dataset allows us to discover what's behind the "Sanitary Inspection Grade A" sign posted on the window.

## Detailed design

## Sample run

