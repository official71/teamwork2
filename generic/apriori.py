from collections import defaultdict

def count_occurences(s, data):
    s, l = set(s), len(s)
    count = 0
    for trans in data:
        if len(s - trans) == 0:
            count += 1
    return count

def subset_pruned(s, itemsets):
    for i in xrange(len(s)):
        if not tuple(s[:i] + s[i+1:]) in itemsets:
            return True
    return False

def k_itemsets(ksets, data, min_supp, total, itemsets):
    kplus = []
    for family in ksets:
        # family is a list of itemsets with the same k-1 items 
        # except the k-th (and last) item
        candidates = []
        while family:
            # take the first itemset (root) in family, new candidates are generated 
            # using 'root' + the last element of 'other', where 'other' is each of the 
            # rest of the itemsets in family, e.g.
            # family = [ [1,2,3], [1,2,4], [1,2,5] ], where [1,2] is common among them, 
            # root = [1,2,3], we have candidates [1,2,3,4] and [1,2,3,5],
            # root = [1,2,4], we have candidates [1,2,4,5],
            # root = [1,2,5], no more candidates as it is the last one
            root = family.pop(0)
            for other in family:
                s = root + other[-1:]
                if subset_pruned(s, itemsets):
                    # candidate s is pruned because one or more of its subsets 
                    # are not among existing large itemsets
                    continue
                count = count_occurences(s, data)
                supp = float(count) / total
                if supp >= min_supp:
                    # candidate s is frequent enough, include s into itemsets
                    candidates.append(s)
                    itemsets[tuple(s)] = supp
        # print candidates
        if candidates:
            kplus.append(candidates)
    return kplus

def single_itemsets(data, min_supp, itemsets):
    sets = []
    total = 0 #denominator
    counts = defaultdict(int)
    for trans in data:
        total += 1
        for item in trans:
            counts[item] += 1

    # filter items that are less frequent
    for item, count in counts.items():
        supp = float(count) / total
        if supp >= min_supp:
            # item should be included
            sets.append([item])
            itemsets[tuple([item])] = supp

    # put the list of sorted items in a list and return
    sets.sort() 
    res = [sets] if sets else []
    return res, total


def itemsets_apriori(data, min_supp):
    itemsets = {}
    ksets, total = single_itemsets(data, min_supp, itemsets)
    while ksets:
        ksets = k_itemsets(ksets, data, min_supp, total, itemsets)
    return itemsets
