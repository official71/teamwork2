class AssociationRule(object):
    """
    Association rules: likelihood of RHS items given the LHS items.

    ...

    Attributes
    ----------
    lhs : list[int]
        left-hand-side itemset
    rhs : list[int]
        right-hand-side itemset
    conf : float
        confidence value of the rule, probability of rhs given lhs
    supp : float
        support value of the rule, fraction of transactions that 
        contain all items in both lhs and rhs
    """
    def __init__(self, lhs, rhs, conf, supp):
        self.__lhs = lhs
        self.__rhs = rhs
        self.__conf = conf
        self.__supp = supp

    def __cmp__(self, other):
        r = cmp(len(self.__rhs), len(other.__rhs))
        if r == 0:
            r = cmp(len(self.__lhs), len(other.__lhs))
        if r == 0:
            r = -cmp(self.__conf, other.__conf)
        if r == 0:
            r = -cmp(self.__supp, other.__supp)
        return r

    def __str__(self):
        return "[{}] => [{}] (Conf: {}%, Supp: {}%)".format(
            ",".join([str(item) for item in self.__lhs]), 
            ",".join([str(item) for item in self.__rhs]),
            int(self.__conf * 100), int(self.__supp * 100))

    @property
    def attr(self):
        return (self.__lhs, self.__rhs, self.__conf, self.__supp)

"""generate rules out of one itemset (support only single item in RHS)

Parameters
----------
itemsets : dict{tuple(int):float}
    key-value pairs of itemsets and their support value
min_conf : float
    minimum confidence value that the generated rules must have
numerator : float
    the numerator in computing the confidence of the input itemset, i.e. 
    the support value of itemset in itemsets
itemset : tuple(int)
    the itemset where rules are generated from

Returns
-------
list[AssociationRule]
    list of association rules generated
"""
def generate_rules(itemsets, min_conf, numerator, itemset):
    # calculate the confidence of LHS => RHS, using support values stored  
    # in itemsets:
    # conf(LHS, RHS) = supp(LHS U RHS) / supp(LHS)
    # the numerator is the support value of itemset in itemsets, and 
    # the denominator is the support value of LHS set in itemsets, which 
    # must exist in itemsets because of the nature of large itemsets: 
    # if (a U b) is a frequent (large) itemset, then (a) must also be a 
    # large itemset
    res = []
    for i in xrange(len(itemset)):
        rhs = [itemset[i]]
        # perhaps we should discard the rule if the support of RHS is too 
        # high, e.g. if the RHS item has support value 0.9, any rule that 
        # leads to the item will likely to have a very high confidence, 
        # and it somehow makes the rule useless
        p = itemsets.get(tuple(rhs), 0)
        if p > min_conf:
            continue

        lhs = itemset[:i] + itemset[i+1:]
        denominator = itemsets.get(tuple(lhs), 0)
        if lhs and rhs and denominator:
            conf = float(numerator / denominator)
            if conf >= min_conf:
                res.append(AssociationRule(lhs, rhs, conf, numerator))
    return res

"""generate all association rules (support only single item in RHS)

Parameters
----------
itemsets : dict{tuple(int):float}
    key-value pairs of itemsets and their support value
min_conf : float
    minimum confidence value that the generated rules must have

Returns
-------
list[AssociationRule]
"""
def association_rules(itemsets, min_conf):
    min_conf = float(min_conf)
    rules = []
    for itemset, numerator in itemsets.items():
        if len(itemset) <= 1: continue
        rules.extend(generate_rules(itemsets, min_conf, numerator, itemset))
    # rules.sort()
    return rules
