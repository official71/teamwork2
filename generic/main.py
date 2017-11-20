#!/usr/bin/env python

import argparse
import os.path
from data import *
from apriori import itemsets_apriori
from rules import association_rules

def main(csvname, min_supp, min_conf):
    # validate inputs
    if not csvname or not os.path.isfile(csvname):
        raise ValueError("[ERROR] Invalid CSV file: {}".format(csvname))
    if not 0 <= min_supp <= 1:
        raise ValueError("[ERROR] Invalid support value: {}".format(min_supp))
    if not 0 <= min_conf <= 1:
        raise ValueError("[ERROR] Invalid confidence value: {}".format(min_conf))

    if __debug__:
        print "====== ASSOCIATION RULES (DEBUG MODE)======"
    else:
        print "====== ASSOCIATION RULES ======"
    print "Input CSV file ----- {}".format(csvname)
    print "Minimum Support ---- {}".format(min_supp)
    print "Minimum Confidence - {}".format(min_conf)

    # save and index CSV data
    print "\nParsing CSV data..."
    csvdata = CSVData(csvname)
    data = csvdata.data

    # generate large itemsets using the Apriori algorithm
    print "\nGenerating large itemsets using Apriori algorithm..."
    itemsets = itemsets_apriori(data, min_supp)
    # print large itemsets
    print "\n==Frequent itemsets (min_supp={}%)".format(int(min_supp * 100))
    i = 0
    for itemset, supp in sorted(itemsets.items(), key=lambda x:x[1], reverse=True):
        if i >= 100: break
        i += 1
        print "[{}], {}%".format(
            ",".join([str(item) for item in csvdata.item_list(itemset)]),
            int(supp * 100))
    if i < len(itemsets):
        print "... and more ..."

    # generate association rules
    print "\nGenerating association rules..."
    rules = association_rules(itemsets, min_conf)
    # print association rules
    print "\n==High-confidence association rules (min_conf={}%)".format(int(min_conf * 100))
    i = 0
    for rule in rules:
        if i >= 100: break
        i += 1
        lhs, rhs, conf, supp = rule.attr
        print "[{}] => [{}] (Conf: {}%, Supp: {}%)".format(
            ",".join([str(item) for item in csvdata.item_list(lhs)]), 
            ",".join([str(item) for item in csvdata.item_list(rhs)]),
            int(conf * 100), int(supp * 100))
    if i < len(rules):
        print "... and more ..."




# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Mining using Apriori algorithm')
    parser.add_argument('csvname', type=str, help='name of the CSV file that contains data')
    parser.add_argument('min_supp', type=float, help='minimal support percentage')
    parser.add_argument('min_conf', type=float, help='minimal confidence percentage')

    args = vars(parser.parse_args())
    main(**args)
