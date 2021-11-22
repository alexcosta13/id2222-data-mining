from itertools import combinations, permutations
from tqdm import tqdm
import time


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

    def count_tuples_fast(self, baskets, frequent_items):
        item_length = len(frequent_items[0])
        count = {}
        for basket in tqdm(baskets):
            basket_combinations = combinations(basket, item_length)
            for c in basket_combinations:
                if c in frequent_items:
                    if c in count:
                        count[c] += 1
                    else:
                        count[c] = 1
        return count

    def generate_candidates(self, items, singletons):
        candidates = {}
        for item in items:
            for singleton in singletons:
                if singleton not in item:
                    candidate = tuple(sorted(item + (singleton, )))
                    if candidate not in candidates:
                        candidates[candidate] = 0
        return candidates

    def count_candidates(self, baskets, candidates):
        count = candidates.copy()
        candidates_length = len(list(candidates.keys())[0])
        for basket in baskets:
            basket_variations = combinations(basket, candidates_length)
            for combination in basket_variations:
                if combination in count:
                    count[combination] += 1
        return count

    def filter(self, count, support):
        return {key: value for key, value in count.items() if value >= support}

    def check_sublist(self, value, item):
        comb = []
        for i in combinations(value, len(value)-1):
            i_list = list(i)
            i_list.append(item)
            comb.append(tuple(i_list))
        return set(comb)

    def make_combinations(self, singletons, item_sets):
        updated_set = []
        for value in tqdm(item_sets):
            for singleton in singletons:
                if singleton not in value:
                    value_list = list(value)
                    value_list.append(singleton)
                    value_list.sort()
                    if self.check_sublist(value, singleton).issubset(item_sets):
                        updated_set.append(tuple(value_list))

        return list(set(updated_set))

    def aprori_algorithm(self, baskets, support):
        count_items = self.count_singletons(baskets)
        acc_count = self.filter(count_items, support)
        frequent_items = acc_count.keys()
        item_sets = [(item,) for item in frequent_items]
        acc_count = {(key, ): value for key, value in acc_count.items()}

        while len(item_sets) > 0:
            #combinations = self.make_combinations(frequent_items, item_sets)
            #tuples_count = self.count_tuples_fast(baskets, combinations)
            candidates = self.generate_candidates(item_sets, frequent_items)
            tuples_count = self.count_candidates(baskets, candidates)
            count = self.filter(tuples_count, support)
            item_sets = count.keys()
            acc_count.update(count)

        return acc_count

    def generate_association_rules(self, count, confidence):
        associations = {}
        frequent_set = count.keys()
        for itemset in frequent_set:
            if len(itemset) > 1:
                candidates = permutations(itemset)
                for rule in candidates:
                    for i in range(len(itemset)-1, 0, -1):
                        num_idx = tuple(sorted(list(rule)))
                        den_idx = tuple(sorted(list(rule[:i])))
                        i_idx = tuple(sorted(list(rule[i:])))
                        conf = count[num_idx] / count[den_idx]
                        if conf > confidence:
                            key = f"{', '. join(list(map(str, i_idx)))} --> {', '. join(list(map(str, den_idx)))}"
                            associations[key] = conf
                        else:
                            break

        return associations

