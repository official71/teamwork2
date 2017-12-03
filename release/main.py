#!/usr/bin/env python

import argparse
import os.path
from data import *
from apriori import itemsets_apriori
from rules import association_rules


"""main function
Parameters
----------
csvname : str
    name of the CSV file containing integrated data
min_supp : float
    minimum support value
min_conf : float
    minimum confidence value
"""
def main(csvname, min_supp, min_conf):
    # validate inputs
    if not csvname or not os.path.isfile(csvname):
        raise ValueError("[ERROR] Invalid CSV file: {}".format(csvname))
    if not 0 <= min_supp <= 1:
        raise ValueError("[ERROR] Invalid support value: {}".format(min_supp))
    if not 0 <= min_conf <= 1:
        raise ValueError("[ERROR] Invalid confidence value: {}".format(min_conf))

    if __debug__:
        print "====== ASSOCIATION RULES (DEBUG MODE) ======"
    else:
        print "====== ASSOCIATION RULES ======"
    print "Input CSV file ----- {}".format(csvname)
    print "Minimum Support ---- {}".format(min_supp)
    print "Minimum Confidence - {}".format(min_conf)

    # save and index CSV data
    print "\nParsing CSV data..."
    csvdata = CSVData(csvname)
    data = csvdata.data

    # compute rules and dump output to file
    outname = "output.txt"
    with open(outname, "w") as outfile:
        # generate large itemsets using the Apriori algorithm
        print "\nGenerating large itemsets using Apriori algorithm..."
        itemsets = itemsets_apriori(data, min_supp)
        # print and dump to file the large(frequent) itemsets
        outfile.write("==Frequent itemsets (min_supp=%.2f%%)\n" % (min_supp * 100))
        for itemset, supp in sorted(itemsets.items(), key=lambda x:x[1], reverse=True):
            line = "[ %s ], %.2f%%\n" % (
                " , ".join([str(item) for item in csvdata.item_list(itemset)]), 
                supp * 100)
            outfile.write(line)
        print "Found %d larger itemsets." % (len(itemsets))

        # generate association rules
        print "\nGenerating association rules..."
        rules = association_rules(itemsets, min_conf)
        # print and dump to file the association rules
        outfile.write("\n\n==High-confidence association rules (min_conf=%.2f%%)\n" % (min_conf * 100))
        for rule in sorted(rules, key=lambda x:x.attr[2], reverse=True):
            lhs, rhs, conf, supp = rule.attr
            line = "[ %s ] => [ %s ] (Conf: %.2f%%, Supp: %.2f%%)\n" % (
                " , ".join(csvdata.item_list(lhs)), 
                " , ".join(csvdata.item_list(rhs)),
                conf * 100, supp * 100)
            outfile.write(line)
        print "Found %d association rules." % (len(rules))
        print "Refer to %s for detailed outputs. Exiting..." % (outname)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Mining using Apriori algorithm')
    parser.add_argument('csvname', type=str, help='name of the CSV file that contains data')
    parser.add_argument('min_supp', type=float, help='minimal support value (range 0 to 1)')
    parser.add_argument('min_conf', type=float, help='minimal confidence value (range 0 to 1)')

    args = vars(parser.parse_args())
    main(**args)
