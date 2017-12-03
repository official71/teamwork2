import csv

class CSVData(object):
    """
    Abstract CSV data by mapping each item value in the original CSV data 
    to an integer ID, and converting each row in the CSV into a set of 
    integers.

    ...

    Attributes
    ----------
    item2id : dict{str:int}
        mapping items in the original CSV to integers
    id2item : dict{int:str}
        mapping an integer ID to an item in the original CSV data
    data : list[set(int)]
        rows in original CSV data mapped to list of a set of integers

    Methods
    -------
    item_list(id_list)
        map a list of integers to their corresponding items in original CSV
    """
    def __init__(self, csvname):
        self.item2id = {}
        self.id2item = {}
        self.data = []
        self.maxid = 0
        self.__construct(csvname)

    """construct member data from original CSV
    
    Parameters
    ----------
    csvname : str
        name of the CSV file
    """
    def __construct(self, csvname):
        with open(csvname, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            if __debug__:
                print "Constructing indices of CSV data"
                dbg_count = 0
            for row in csvreader:
                d = set()
                for item in row:
                    if not item: continue
                    # decode utf-8 for internal use
                    item = item.decode('utf-8')
                    i = self.item2id.get(item, None)
                    if i is None:
                        # item does NOT have an associated ID,
                        # assign ID to item
                        self.maxid += 1
                        self.item2id[item] = self.maxid
                        self.id2item[self.maxid] = item
                        i = self.maxid
                    # add ID into the current row 
                    d.add(i)
                if d:
                    # add an valid row into datasets
                    self.data.append(d)
                if __debug__:
                    dbg_count += 1
                    if dbg_count % 20000 == 0:
                        print "{} lines processed".format(dbg_count)
            if __debug__:
                print "All {} lines processed".format(dbg_count)

    """maps a list of integers to their corresponding items in original CSV
    
    Parameters
    ----------
    id_list : list[int]
        list of integer ID
    
    Returns
    -------
    list[str]
    """
    def item_list(self, id_list):
        # encode utf-8 for output
        return [self.id2item.get(i, None).encode('utf-8') for i in id_list]

