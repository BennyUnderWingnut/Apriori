from collections import Counter, defaultdict
from itertools import dropwhile
import demjson


class APriori():
    """
    Frequent itemset miner class to implement Apriori algorithm using standard
    libraries in Python 3. Input is a database of per-row transactions of
    space-separated integers (or string representations of integers) for items.
    Writes out a text file with one row per frequent itemset, with set size,
    frequency, and constiutent items indicated in that order.
    """

    def __init__(self, data=None, out=None):

        self.data = data
        self.out = out
        self.previous = []
        self.frequent = defaultdict(Counter)

    def find_frequent(self, support, min_set_size, max_set_size):

        assert self.data is not None and self.out is not None, "data or out path is None"
        self.sigma = support
        self.min_set = min_set_size
        self.max_set = max_set_size
        self.frequent[1] = self._generate_data()
        self.associative = {}
        temp = defaultdict(Counter)

        k = 2
        # there must be at least k itemsets of size k-1 already found to
        # be frequent for there to be any frequent k-itemsets
        while len(self.frequent[k - 1]) >= k and k <= self.max_set:

            for i in range(len(self.previous)):
                # find per-transaction candidates of size k-1. groups generated
                # on previous pass, and checked against frequent itemsets now
                k_minus_1 = [
                    group for group in self.previous[i]
                    if group in self.frequent[k - 1]
                ]

                # order is cruicial: items in tuples are sorted here, while
                # ordering of tuples was established on the first pass
                cand = [
                    tuple(sorted(set(x).union(y))) for x in k_minus_1
                    for y in k_minus_1 if x < y and x[:-1] == y[:-1]
                ]

                # only those candidates need to be considered on the next pass
                self.previous[i] = cand

                # increment counts
                for group in cand:
                    self.frequent[k][group] += 1

            # drop infrequent keys
            self.frequent[k] = self._drop_infrequent(k)

            k += 1

        for key in self.frequent.keys():
            if self.min_set <= key <= self.max_set:
                for group, k in self.frequent[key].items():
                    for item_x in group:
                        other = tuple(
                            sorted([
                                item for item in group if not item == item_x
                            ]))
                        temp[item_x][other] += k / self.frequent[len(group)
                                                                 - 1][other]
        for k, v in temp.items():
            self.associative[k] = sorted(v, key=v.get, reverse=True)
        with open(self.out, "w") as f:
            f.write(demjson.encode(self.associative, strict=False))
        return

    def _drop_infrequent(self, k):
        """Remove keys from frequent items counter if their counts are below the
        support threshold. Check counts in descending order until reaching the
        first that is below the support threshold, then safely delete all such
        keys that follow."""

        for key, count in dropwhile(lambda key_ct: key_ct[1] >= self.sigma,
                                    self.frequent[k].most_common()):
            del self.frequent[k][key]

        print("Frequent {}-itemsets generated.".format(k))

        return self.frequent[k]

    def _generate_data(self):
        """Generate a list of viable transactions and counts of frequent
        singletons on the first pass. Only transactions as long as the minimum
        set size are considered, and frequent itemset keys are k-tuples of
        integers of item ids, in order to generalize for k > 1. Transactions
        themselves are not stored in memory, but rather a list of sorted lists
        of size k-1 candidates from each transaction, as only those could
        possibly generate frequent itemsets of size k.
        """

        with open(self.data, "r") as f:
            for line in f.readlines():
                # ensure there are no duplicate items in the transaction
                items = [tuple([int(item)]) for item in set(line.split())]

                # ignore transactions shorter than the min set size
                if len(items) >= self.min_set:
                    # sort to avoid generating duplicate candidate with k > 1
                    self.previous.append(sorted(items))
                    for item in items:
                        self.frequent[1][item] += 1

        self.frequent[1] = self._drop_infrequent(1)

        return self.frequent[1]

    def read_data(self, data_file):
        self.associative = demjson.decode_file(data_file)

    def get_frequent_list_of(self, wanted_items, detected_items):
        if self.associative is None:
            raise Exception('No data')
        frequent_list = defaultdict(list)
        for k in self.associative:
            if k in wanted_items:
                groups = [
                    group for group in self.associative[k] if all(
                        item in detected_items for item in group)
                ]
                frequent_list[k].append(groups)
        return frequent_list
