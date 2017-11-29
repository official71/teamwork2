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


def generate_pairs(itemsets, min_conf, numerator, itemset):
    # ONLY SUPPORT SINGLE ITEM IN RHS
    # calculate the confidence of LHS => RHS, using occurence counts 
    # in itemsets:
    # conf(LHS, RHS) = count(LHS U RHS) / count(LHS)
    # the numerator is the support value of itemset in itemsets, and 
    # the denominator is the support value of LHS set in itemsets, which 
    # must exist in itemsets because of the nature of large itemsets: 
    # if (a U b) is a frequent (large) itemset, then (a) must also be a 
    # large itemset
    res = []
    for i in xrange(len(itemset)):
        rhs = [itemset[i]]
        lhs = itemset[:i] + itemset[i+1:]
        denominator = itemsets.get(tuple(lhs), 0)
        if lhs and rhs and denominator:
            conf = float(numerator / denominator)
            if conf >= min_conf:
                res.append(AssociationRule(lhs, rhs, conf, numerator))
    return res

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
        # assert (in_order(itemset)), "itemset {} not in order".format(itemset)
        rules.extend(generate_pairs(itemsets, min_conf, numerator, itemset))
    rules.sort(reverse=True)
    return rules
