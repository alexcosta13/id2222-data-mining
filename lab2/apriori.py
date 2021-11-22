import itertools


class Apriori:
    def count_singletons(self, baskets):
        """
        Count all the elements in the baskets
        :param baskets: list of all elements
        :return: dictionary of the count (elem: count of the element)
        """
        count = {}
        for basket in baskets:
            for elem in basket:
                if elem in count:
                    count[elem] += 1
                else:
                    count[elem] = 1
        return count

    def make_combinations(self, item_sets, frequent_items):
        """
        Make combinations by concatenating every item in item_sets with all frequent items.
        :param item_sets: list of all items
        :param frequent_items: Singletons of frequent items
        :return: all list of possible combinations
        """
        candidates = {}
        for item in item_sets:
            for single_item in frequent_items:
                if single_item not in item:
                    candidate = tuple(sorted(item + (single_item,)))
                    candidates[candidate] = 0
        return candidates

    def count_tuples(self, baskets, combinations):
        """
        Count in how many baskets does each tuple appear.
        :param baskets: list of all elements
        :param combinations: a possible tuple
        :return: dictionary with the tuple as a key and the count as a value
        """
        count = combinations.copy()
        candidates_length = len(list(combinations.keys())[0])
        for basket in baskets:
            basket_combinations = itertools.combinations(basket, candidates_length)
            for combination in basket_combinations:
                if combination in count:
                    count[combination] += 1
        return count

    def filter(self, count, support):
        """
        Filter all the elements that are bellow the support
        :param count: dictionary that contains the count of all elements
        :param support: number of baskets that contain a given itemset
        :return: dictionary with key and count of all filtered elements
        """

        return {key: value for key, value in count.items() if value >= support}

    def aprori_algorithm(self, baskets, support):
        """
        Performs a priori algorithm
        :param baskets: list of all elements
        :param support: fraction of baskets that contain a given itemset
        :return: all frequent itemsets
        """
        n_baskets = len(baskets)
        count_items = self.count_singletons(baskets)
        support = int(support*n_baskets)
        acc_count = self.filter(count_items, support)
        frequent_items = acc_count.keys()
        item_sets = [(item,) for item in frequent_items]
        acc_count = {(key,): value for key, value in acc_count.items()}

        while len(item_sets) > 0:
            combinations = self.make_combinations(item_sets, frequent_items)
            tuples_count = self.count_tuples(baskets, combinations)
            count = self.filter(tuples_count, support)
            item_sets = count.keys()
            acc_count.update(count)

        return acc_count

    def generate_association_rules(self, count, confidence):
        """
        Generate association rules
        :param count: count of all the frequent tuples
        :param confidence: fraction of number of baskets that appear
        I and j out of the number of baskets that appears j
        :return: associations
        """
        associations = {}
        frequent_set = count.keys()
        for itemset in frequent_set:
            if len(itemset) > 1:
                candidates = itertools.permutations(itemset)
                for rule in candidates:
                    for i in range(len(itemset) - 1, 0, -1):
                        num_idx = tuple(sorted(list(rule)))
                        den_idx = tuple(sorted(list(rule[:i])))
                        i_idx = tuple(sorted(list(rule[i:])))
                        conf = count[num_idx] / count[den_idx]
                        if conf > confidence:
                            key = f"{', '. join(list(map(str, den_idx)))} ==> {', '. join(list(map(str, i_idx)))}"
                            associations[key] = conf
                        else:
                            break

        return associations
