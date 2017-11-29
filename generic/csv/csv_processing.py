#!/usr/bin/env python
import argparse
import csv
from collections import defaultdict
import importlib

class CSVColumn(object):
    def __init__(self, title, index):
        self.title = title
        self.index = index
        self.value_counter = defaultdict(int)
        self.nr_rows = 0
        self.rename_module = None
        self.rename_fun = None

    def add_one(self, value):
        self.value_counter[value] += 1
        self.nr_rows += 1
    
    def show_info(self):
        print "Column #{}:".format(self.index)
        print "Title: {}".format(self.title)
        print "Rows: {}".format(self.nr_rows)
        nr_enum = len(self.value_counter)
        print "Enumerations: {} unqiue values".format(nr_enum)
        if nr_enum > float(self.nr_rows) * 0.01:
            print "Too many unique values"
        imax = raw_input("Show all values(Y/N)? or input specific number to show: ")
        if imax.lower() in ('y', 'yes'):
            imax = len(self.value_counter)
        elif imax.lower() in ('n', 'no', ''):
            imax = 0
        else:
            try:
                imax = int(imax)
            except:
                imax = 0

        for value, count in sorted(self.value_counter.items(), key=lambda x:x[1], reverse=True)[:imax]:
            print "[{}], {} ({}%)".format(value, count, format(100*float(count)/self.nr_rows, '.1f'))


    def rename(self, rename_module):
        self.rename_module = rename_module
        fun = "_".join([w.lower() for w in self.title.split()])
        if not fun:
            return
        try:
            self.rename_fun = getattr(rename_module, fun)
        except Exception as e:
            print "Error loading function {}.{}: {}".format(rename_module, fun, e)


# main function
def main(csvname, module):
    print "Processing CSV file: {}".format(csvname)
    rename_module = None
    if module:
        try:
            rename_module = importlib.import_module(module)
        except Exception as e:
            print "Error loading module {}: {}".format(module, e)
            return
    try:
        f = open(csvname, 'r')
    except Exception as e:
        print "Error opening file: {}".format(e)

    print "Parsing CSV file..."
    columns = []
    reader = csv.reader(f, delimiter=',', quotechar='\"')
    line = next(reader)
    for i, title in enumerate(line):
        columns.append(CSVColumn(title, i))
    for line in reader:
        for i, value in enumerate(line):
            columns[i].add_one(value)
    f.close()

    print "\nStatistics of CSV file:"
    print "Columns: {}".format(len(columns))
    print "Rows: {}".format(columns[0].nr_rows)

    print "\nRe-formatting columns"
    reformatted = []
    for col in columns:
        print "\n" + "=" * 36
        col.show_info()
        
        yes = raw_input("\nAre you keeping this column(Y/N)? ")
        yes = yes.lower() in ('y', 'yes')
        if not yes:
            print "Skipping this column..."
            continue
        reformatted.append(col)

        yes = raw_input("Keeping this column, are you renaming the values(Y/N)? ")
        yes = yes.lower() in ('y', 'yes')
        if not yes:
            print "Keeping the column values as they were..."
            continue
        elif not rename_module:
            print "Cannot rename columns because no module has been specified"
        else:
            print "Renaming the values..."
            col.rename(rename_module)

    print "\nWriting the re-formatted CSV"
    with open(csvname + '.reformat', 'w') as wf:
        writer = csv.writer(wf, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        with open(csvname, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='\"')
            next(reader)
            for line in reader:
                values = []
                for col in reformatted:
                    if col.rename_fun:
                        values.append(col.rename_fun(line[col.index]))
                    else:
                        values.append(line[col.index])
                writer.writerow([v for v in values if v])


# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process original CSV file for Data Mining')
    parser.add_argument('csvname', type=str, help='name of the CSV file that contains data')
    parser.add_argument('--module', type=str, help='module of renaming functions')

    args = vars(parser.parse_args())
    main(**args)
