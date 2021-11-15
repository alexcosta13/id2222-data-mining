class CompareSet:
    def jaccard_similarity(self, shingle1, shingle2):
        """
        Returns the Jaccard similarity of two sets, defined as the size of the
        intersection divided by the size of the union of these sets.
        :param shingle1: input set
        :param shingle2: input set
        :return: float between 0 and 1
        """
        return len(set(shingle1) & set(shingle2)) / len(set(shingle1) | set(shingle2))
