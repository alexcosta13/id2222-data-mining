

class CompareSet:
    def jaccard_similarity(self, shingle1, shingle2):
        return len(set(shingle1) & set(shingle2)) / len(set(shingle1) | set(shingle2))
