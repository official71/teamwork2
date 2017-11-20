class AssociationRule(object):
    def __init__(self, lhs, rhs, conf, supp):
        self.__lhs = lhs
        self.__rhs = rhs
        self.__conf = conf
        self.__supp = supp

    def __cmp__(self, other):
        r = cmp(self.__conf, other.__conf)
        if r == 0:
            r = cmp(self.__supp, other.__supp)
        return r

    def __str__(self):
        return "[{}] => [{}] (Conf: {}%, Supp: {}%)".format(
            ",".join([str(item) for item in self.__lhs]), 
            ",".join([str(item) for item in self.__rhs]),
            int(self.__conf * 100), int(self.__supp * 100))

    @property
    def attr(self):
        return (self.__lhs, self.__rhs, self.__conf, self.__supp)


def generate_pairs(rules, itemsets, min_conf, numerator, lhs, rhs, itemset, i):
    if i == len(itemset):
        # all items in itemset have been assigned to either side,
        # calculate the confidence of LHS => RHS, using occurence counts 
        # in itemsets:
        # conf(LHS, RHS) = count(LHS U RHS) / count(LHS)
        # the numerator is the support value of itemset in itemsets, and 
        # the denominator is the support value of LHS set in itemsets, which 
        # must exist in itemsets because of the nature of large itemsets: 
        # if (a U b) is a frequent (large) itemset, then (a) must also be a 
        # large itemset
        denominator = itemsets.get(tuple(lhs), 0)
        assert (not lhs or denominator > 0), "lhs {} does not exist in itemsets".format(lhs)
        if lhs and rhs and denominator:
            conf = float(numerator / denominator)
            if conf >= min_conf:
                rules.append(AssociationRule(lhs, rhs, conf, numerator))
    else:
        # continue generating lhs and rhs
        generate_pairs(rules, itemsets, min_conf, numerator, lhs+[itemset[i]], rhs, itemset, i+1)
        generate_pairs(rules, itemsets, min_conf, numerator, lhs, rhs+[itemset[i]], itemset, i+1)

def in_order(s):
    order = 0
    for i in xrange(1, len(s)):
        if order == 0:
            order = cmp(s[i], s[i-1])
        else:
            t = cmp(s[i], s[i-1])
            if t != 0 and t != order:
                return False
    return True

# assume items in each itemset are sorted
def association_rules(itemsets, min_conf):
    min_conf = float(min_conf)
    rules = []
    for itemset, numerator in itemsets.items():
        if len(itemset) <= 1: continue
        # for an itemset containing multiple items, partition it into two 
        # itemsets (LHS and RHS) and calculate the confidence of (LHS => RHS), 
        # for example:
        # itemset = (1,2,3), rules of LHS => RHS are: (1) => (2, 3), 
        # (2, 3) => (1), (1, 2) => (3), (3) => (1, 2), (1, 3) => (2), 
        # (2) => (1, 3)
        # notice that a => b and b => a are not the same; there are 
        # 2^k - 2 pairs for an itemset of k items
        assert (in_order(itemset)), "itemset {} not in order".format(itemset)
        generate_pairs(rules, itemsets, min_conf, numerator, [], [], itemset, 0)
    rules.sort(reverse=True)
    return rules