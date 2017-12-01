import csv

class CSVData(object):
    def __init__(self, csvname):
        self.item2id = {}
        self.id2item = {}
        self.data = [] # data, list of sets, where each set is a transaction
        self.maxid = 0
        self.__construct(csvname)
        # print self.item2id
        # print self.id2item
        # print self.data
        # print self.maxid

    def __construct(self, csvname):
        with open(csvname, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            if __debug__:
                print "Constructing indices of CSV data"
                dbg_count = 0
            for line in csvreader:
                d = set()
                for item in line:
                    if not item: continue
                    item = item.decode('utf-8')
                    i = self.item2id.get(item, None)
                    if i is None:
                        # item does NOT have an associated ID,
                        # assign ID to item
                        self.maxid += 1
                        self.item2id[item] = self.maxid
                        self.id2item[self.maxid] = item
                        i = self.maxid
                    # add ID into the current set (transaction)
                    d.add(i)
                if d:
                    # add an valid transaction into datasets
                    self.data.append(d)
                if __debug__:
                    dbg_count += 1
                    if dbg_count % 20000 == 0:
                        print "{} lines processed".format(dbg_count)
            if __debug__:
                print "All {} lines processed".format(dbg_count)

    def item_list(self, id_list):
        return [self.id2item.get(i, None).encode('utf-8') for i in id_list]

