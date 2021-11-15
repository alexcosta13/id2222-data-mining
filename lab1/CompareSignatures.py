class CompareSignatures:
    def compare(self, sign1, sign2):
        """
        Element-wise comparison of two list of the same size
        :param sign1: input list
        :param sign2: input list
        :return: fraction of equal elements
        """
        equal = 0
        for elem1, elem2 in zip(sign1, sign2):
            if elem1 == elem2:
                equal += 1
        return equal / len(sign1)
