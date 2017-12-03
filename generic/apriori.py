from collections import defaultdict

"""count the number of occurrences (support) of given itemset

Parameters
----------
candidate : list[int]
    candidate itemset
data : list[set(int)]
    list of transactions

Returns
-------
int
"""
def count_occurences(candidate, data):
    if not candidate: return 0
    candidate, l = set(candidate), len(candidate)
    count = 0
    for transaction in data:
        if len(candidate - transaction) == 0:
            # number of items that are in the candidate itemset but missing 
            # in the transaction is 0 => the transaction "support" this itemset
            count += 1
    return count

"""prune unlikely itemset
Reference: 2.1.1 of Rakesh's paper - the "prune-step"
Returns True (pruned) if any of the (k-1)-subsets of the k-itemset is NOT 
a large itemset

Parameters
----------
candidate : list[int]
    candidate itemset
itemsets : dict{tuple(int):float}
    known large itemsets

Returns
-------
boolean
    True if pruned; False if not pruned
"""
def subset_pruned(candidate, itemsets):
    for i in xrange(len(candidate)):
        if not tuple(candidate[:i] + candidate[i+1:]) in itemsets:
            return True
    return False

"""Apriori candidate generation function of (k+1)-itemsets given k-itemsets
Reference: 2.1.1 of Rakesh's paper - the "apriori-gen" function

Parameters
----------
ksets : list[list[list[int]]]
    the k-itemsets from previous iteration, containing all the "families" 
    of itemsets with k number of items. A family of itemsets consist of the 
    same set of items except for the last one, e.g.
    [
    [[1,2,3],[1,2,4],[1,2,7]],
    [[2,5,6],[2,5,7]]
    ]
data : list[set(int)]
    list of transactions, each transaction is a set of integer items
min_supp: float
    minimum support value for an itemset to be "large"
total : int
    total number of transactions, used for computing support values
itemsets: dict{tuple(int):float}
    containing final results: large itemsets and their support values

Returns
-------
kplus : list[list[list[int]]]
    (k+1)-itemsets generated
"""
def apriori_gen_k_itemsets(ksets, data, min_supp, total, itemsets):
    if __debug__:
        # some work is needed to know how many items the sets currently contain
        if not ksets or not ksets[0]:
            dbg_n = 0
        else:
            dbg_n = len(ksets[0][0]) + 1
        print "Generating frequent {}-item itemsets".format(dbg_n)
        dbg_count = 0
    kplus = [] # the (k+1)-itemsets
    for family in ksets:
        # family is a list of itemsets with the same k-1 items 
        # except the k-th (and last) item
        while family:
            candidates = []
            # take the first itemset (root) in family, new candidates are generated 
            # using 'root' + the last element of 'other', where 'other' is each of the 
            # rest of the itemsets in family, e.g.
            # family = [ [1,2,3], [1,2,4], [1,2,5] ], where [1,2] is common among them, 
            # root = [1,2,3], we have candidates [1,2,3,4] and [1,2,3,5],
            # root = [1,2,4], we have candidates [1,2,4,5],
            # root = [1,2,5], no more candidates as it is the last one
            root = family.pop(0)
            for other in family:
                candidate = root + other[-1:]
                if subset_pruned(candidate, itemsets):
                    # candidate is pruned because one or more of its subsets 
                    # are not among existing large itemsets
                    continue
                count = count_occurences(candidate, data)
                supp = float(count) / total
                if supp >= min_supp:
                    # candidate is frequent enough, include it into itemsets
                    candidates.append(candidate)
                    itemsets[tuple(candidate)] = supp
            # print candidates
            if candidates:
                kplus.append(candidates)
                if __debug__:
                    # print "{} new candidates found".format(len(candidates))
                    dbg_count += len(candidates)
    if __debug__:
        print "{}-item itemsets extracted: {}".format(dbg_n, dbg_count)
    return kplus

"""Apriori candidate generation function of single-item itemsets
Reference: Chapter 2.1.1 of Rakesh's paper - the "apriori-gen" function

Parameters
----------
data : list[set(int)]
    list of transactions, each transaction is a set of integer items
min_supp: float
    minimum support value for an itemset to be "large"
itemsets: dict{tuple(int):float}
    containing final results: large itemsets and their support values

Returns
-------
res : list[list[list[int]]]
    all k-itemsets, k is the size of itemsets in the current iteration, 
    in this case k = 1
total : int
    total number of transactions
"""
def apriori_gen_single_itemsets(data, min_supp, itemsets):
    if __debug__:
        print "Generating frequent 1-item itemsets"
    candidates = []
    total = 0 #denominator
    counts = defaultdict(int)
    for trans in data:
        total += 1
        for item in trans:
            counts[item] += 1
    if __debug__:
        print "Total number of transactions: {}".format(total)

    # filter items that are less frequent
    for item, count in counts.items():
        supp = float(count) / total
        if supp >= min_supp:
            # item should be included
            candidates.append([item])
            itemsets[tuple([item])] = supp

    # if 1-itemsets are sorted, the algorithm ensures that all itemsets 
    # generated in following iterations are all sorted internally
    candidates.sort() 
    res = [candidates] if candidates else []
    if __debug__:
        print "1-item itemsets extracted: {}".format(len(candidates))
    return res, total

"""generate large(frequent) itemsets using Apriori algorithm
Reference: Fast Algorithms for Mining Association Rules by Rakesh et al.
(http://www.cs.columbia.edu/%7Egravano/Qual/Papers/agrawal94.pdf)

Parameters
----------
data : list[set(int)]
    list of transactions, each transaction is a set of integer items
min_supp: float
    minimum support value for an itemset to be "large"

Returns
-------
itemsets : dict{tuple(int):float}
    key-value pairs of large itemsets (tuple of integers) and their support 
    value in the data
"""
def itemsets_apriori(data, min_supp):
    itemsets = {}
    ksets, total = apriori_gen_single_itemsets(data, min_supp, itemsets)
    while ksets:
        ksets = apriori_gen_k_itemsets(ksets, data, min_supp, total, itemsets)
    return itemsets
