#!/usr/bin/env python

import argparse
import os.path
from data import *
from apriori import itemsets_apriori

def main(csvname, min_supp, min_conf):
    # validate inputs
    if not csvname or not os.path.isfile(csvname):
        raise ValueError("[ERROR] Invalid CSV file: {}".format(csvname))
    if not 0 <= min_supp <= 1:
        raise ValueError("[ERROR] Invalid support value: {}".format(min_supp))
    if not 0 <= min_conf <= 1:
        raise ValueError("[ERROR] Invalid confidence value: {}".format(min_conf))

    # save and index CSV data
    csvdata = CSVData(csvname)
    data = csvdata.data

    # generate large itemsets using the Apriori algorithm
    itemsets = itemsets_apriori(data, min_supp)
    # print large itemsets
    for itemset, count in sorted(itemsets.items(), key=lambda x:x[1], reverse=True):
        print "items: {}\tcount: {}".format(
            ",".join([str(item) for item in csvdata.item_list(itemset)]),
            count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Mining using Apriori algorithm')
    parser.add_argument('csvname', type=str, help='name of the CSV file that contains data')
    parser.add_argument('min_supp', type=float, help='minimal support percentage')
    parser.add_argument('min_conf', type=float, help='minimal confidence percentage')

    args = vars(parser.parse_args())
    main(**args)
