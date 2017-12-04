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

### (b) Data mapping

* In the original CSV data, each row contains information of a single violation during inspection, as well as the restaurant associated to it. If the restaurant violated multiple terms in one inspection there will be one row for each violation it made. The most important processing to the original data is therefore joining it by `CAMIS`(restaurant ID) and the inspection date, so that each row represents the result of one inspection rather than one violation.

* A selection of columns in the original CSV are then mapped to new data for better representation:

|Column Name|Description|Mapping Approach|
|---|---|---|
|DBA|Name of the restaurant|Add prefix "DBA"|
|BORO|Borough where the restaurant locates|Add prefix "BORO"|
|STREET|Name of the street where the restaurant locates|Add prefix "STREET"|
|CUISINE DESCRIPTION|Describes the cuisine of the restaurant|Add prefix "CUISINE"|
|INSPECTION DATE|Date of the inspection (MM/DD/YYYY)|Mapped into quarters using the month, e.g. "May": "Q2", "July": "Q3"|
|ACTION|Action taken in each inspection, e.g. "Cited", "Closed"|Add prefix "ACTION"|
|INSPECTION TYPE|Type of the inspection|Abstract information into smaller categories such as "Initial Inspection" and "Re-inspection"|
|SCORE|Total score of an inspection||
|GRADE|Grade assigned to the restaurant of an inspection, according to the [DOHMH guide](http://www1.nyc.gov/assets/doh/downloads/pdf/rii/how-we-score-grade.pdf), "Restaurants with a score between 0 and 13 points earn an A, those with 14 to 27 points receive a B and those with 28 or more a C"|When grade is missing for an inspection, use the score to determine the grade|
|CRITICAL FLAG|Whether violation is critical or not, determined by the Violation Code||
|VIOLATION CODE|Code of the violation defined by [DOHMH](http://www1.nyc.gov/assets/doh/downloads/pdf/rii/blue-book.pdf)|Combined with Critical Code to form an instance of violation, e.g. VIOLATION_08A_NON_CRITICAL; In addition, the number of critical/non-critical violations of each inspection are counted and categorized as 0, 1, 2 and 3+|

Columns with redundant or over-specific information are discarded for simplicity.

* The mapped data are dumped into `INTEGRATED-DATASET.csv`, reducing the former 396,000 rows of violation data into about 137,000 rows of inspection data.

### (c) Reason of choice

* The dataset is among the [most popular ones](https://data.cityofnewyork.us/browse?provenance=official&sortBy=most_accessed&utf8=✓) in NYC Open Data.
* The columns are well-defined and structured, with relatively less missing fields. Even when there is data missing we can derive the missing fields using the rules specified by DOHMH.
* As much as we'd like our food to be delicious, we care about how clean it is. The dataset allows us to discover what's behind the "Sanitary Inspection Grade A" sign posted on the restaurant window.

## Detailed design

* All items in the original CSV data are treated as Unicode strings, and mapped to a unique integer ID. Each row of the original CSV is converted to a set of integers and saved in class `CSVData`. Further processing assumes integer items.
* Function `itemsets_apriori()` then takes the converted data sets as input, and returns the large itemsets, which is a dictionary with keys being itemsets and values being the corresponding support values. The function implements the algorithm as stated in Figure 1 of [Rakesh's paper](http://www.cs.columbia.edu/%7Egravano/Qual/Papers/agrawal94.pdf). For each candidate itemset, the whole data is scanned to obtain its support value for thresholding.
* Function `association_rules()` generates association rules out of the large itemsets. For an itemset of k items, there are k possible rules obtained by putting one item to the RHS (right hand side) and all the rest k-1 items to the LHS (left hand side). Confidence value of a rule `LHS => RHS` is computed by dividing the support value of `LHS + RHS` with that of LHS alone, which are stored in the dictionary returned by `itemsets_apriori()`. If the confidence is above threshold, construct a `AssociationRule` instance to store the rule. The function finally returns the association rules as a list of such instances.

## Sample run

* For a compelling sample run, run `python main.py INTEGRATED-DATASET.csv 0.05 0.6` in Bash, where the minimum support and confidence are 5% and 60% respectively.
* Some rules of interest:
    * Almost every Grade B is assigned during a re-inspection (unannounced visit if the initial inspection failed to grade an A). There is a good chance (78%) that a re-inspection could result in a Grade A.

    ``` 
    [ GRADE_B ] => [ RE-INSPECTION ] (Conf: 99.97%, Supp: 5.33%)
    [ RE-INSPECTION ] => [ GRADE_A ] (Conf: 77.59%, Supp: 24.97%)
    ```

    * A Restaurant that violated 04L is also likely (85%) to violate 08A, and if this is the initial inspection then there is a high probability (80%) that it will get a Grade C (the unconditional probability of getting Grade C is 35%). According to the [violation codes](http://www1.nyc.gov/assets/doh/downloads/pdf/rii/blue-book.pdf), 04L stands for critical violation of *"Evidence of mice or live mice present in facility's food and/or non-food areas"*, and 08A for non-critical violation of *"Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist"*

    ```
    [ VIOLATION_04L_CRITICAL ] => [ VIOLATION_08A_NON_CRITICAL ] (Conf: 84.52%, Supp: 16.93%)
    [ INITIAL_INSPECTION , VIOLATION_04L_CRITICAL ] => [ GRADE_C ] (Conf: 79.53%, Supp: 10.45%)
    ```

    * Initial inspections tend to be more strict: 
        * With 1 critical violation, a restaurant has an overall probability of 83% to have Grade A, however if it is the initial inspection, the probability decreases to 76%.
        * With 3 or more critical violations, there is an overall 81% chance it will get Grade C, while for initial inspections the chance is as high as 96%.
    
    ```
    [ NR_CRITICAL_VIOLATIONS_1 ] => [ GRADE_A ] (Conf: 82.89%, Supp: 35.48%)
    [ INITIAL_INSPECTION , NR_CRITICAL_VIOLATIONS_1 ] => [ GRADE_A ] (Conf: 75.53%, Supp: 18.93%)

    [ NR_CRITICAL_VIOLATIONS_3+ ] => [ GRADE_C ] (Conf: 80.65%, Supp: 14.94%)
    [ INITIAL_INSPECTION , NR_CRITICAL_VIOLATIONS_3+ ] => [ GRADE_C ] (Conf: 95.58%, Supp: 13.81%)
    ```

    * Inspections made in the first quarter of year (January, February and March) are more likely to result in Grade A than others.

    ```
    [ INSPEC_TIME_Q1 ] => [ GRADE_A ] (Conf: 61.37%, Supp: 14.92%)
    ```

    * Among popular cuisines, restaurants serving American foods are more likely to earn a Grade A.

    ```
    [ CUISINE_(American) ] => [ GRADE_A ] (Conf: 61.13%, Supp: 13.95%)
    ```
