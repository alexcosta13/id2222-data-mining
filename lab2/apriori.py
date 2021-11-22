import itertools


class Apriori:
    def count_singletons(self, baskets):
        count = {}
        for basket in baskets:
            for elem in basket:
                if elem in count:
                    count[elem] += 1
                else:
                    count[elem] = 1
        return count

    def make_combinations(self, item_sets, frequent_items):
        candidates = {}
        for item in item_sets:
            for single_item in frequent_items:
                if single_item not in item:
                    candidate = tuple(sorted(item + (single_item,)))
                    candidates[candidate] = 0
        return candidates

    def count_tuples(self, baskets, combinations):
        count = combinations.copy()
        candidates_length = len(list(combinations.keys())[0])
        for basket in baskets:
            basket_combinations = itertools.combinations(basket, candidates_length)
            for combination in basket_combinations:
                if combination in count:
                    count[combination] += 1
        return count

    def filter(self, count, support):
        return {key: value for key, value in count.items() if value >= support}

    def aprori_algorithm(self, baskets, support):
        count_items = self.count_singletons(baskets)
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
