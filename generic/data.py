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
            for line in csvfile:
                d = set()
                for item in line.rstrip().split(','):
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

    def item_list(self, id_list):
        return [self.id2item.get(i, None) for i in id_list]

