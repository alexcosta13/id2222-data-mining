from itertools import combinations


class Apriori():

    def count_singletons(self, baskets):
        count = {}
        for basket in baskets:
            for elem in basket:
                if elem in count:
                    count[elem] += 1
                else:
                    count[elem] = 1
        return count

    def count_tuples(self, baskets, frequent_items):
        count = {}
        for basket in baskets:
            for item in frequent_items:
                if set(item).issubset(set(basket)):
                    if item in count:
                        count[item] += 1
                    else:
                        count[item] = 1
        return count

    def filter(self, count, support):
        total = sum(count.values())
        return [key for key, value in count.items() if value / total > support]

    def check_sublist(self, value, item):
        comb = []
        for i in combinations(value, len(value)-1):
            i_list = list(i)
            i_list.append(item)
            comb.append(tuple(i_list))
        return set(comb)

    def make_combinations(self, singletons, item_sets):
        updated_set = []
        for value in item_sets:
            for item in singletons:
                if item not in value:
                    value_list = list(value)
                    value_list.append(item)
                    value_list.sort()
                    if self.check_sublist(value, item).issubset(item_sets):
                        updated_set.append(tuple(value_list))

        return list(set(updated_set))

    def aprori_algorithm(self, baskets, support):
        count_items = self.count_singletons(baskets)
        frequent_items = self.filter(count_items, support)
        item_sets = [(item,) for item in frequent_items]
        acc = frequent_items.copy()

        while len(item_sets) > 0:
            combinations = self.make_combinations(frequent_items, item_sets)
            tuples_count = self.count_tuples(baskets, combinations)
            item_sets = self.filter(tuples_count, support)
            acc += item_sets
            print(len(item_sets))

        return acc

    def rules_from_set(self, item_set):
        rules = []
        for i in range(1, len(item_set)):
            left = combinations(item_set, i)
            for elem in left:
                rules.append((set(elem), set(item_set)-set(elem)))
        return rules

    def generate_association_rules(self, item_sets):
        rules = []
        for item_set in item_sets:
            if type(item_set) is tuple:
                rules += self.rules_from_set(item_set)
        return rules
