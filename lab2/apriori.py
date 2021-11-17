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

    def make_combinations(self, frequent_items, item_sets):
        updated_set = []
        for value in item_sets:
            for item in frequent_items:
                if item not in value:
                    value_list = list(value)
                    value_list.append(item)
                    value_list.sort()
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
