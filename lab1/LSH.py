from itertools import combinations


class LSH:
    def __init__(self, b):
        """
        :param b: number of bands
        """
        self.b = b

    def find_candidates(self, signatures):
        """
        Applies the LSH algorithm to find a list of candidate pairs to be similar documents.
        :param signatures:
        :return: list of candidate pairs (tuples)
        """
        r = int(len(signatures[0]) / self.b)
        assert self.b * r == len(signatures[0]),\
            "number of buckets is not a divisor of number of rows"
        buckets = [{} for _ in range(self.b)]
        for band in range(self.b):
            for doc_id, doc in enumerate(signatures):
                doc = doc[band * r : (band + 1) * r]
                hashed = hash("".join([str(elem) for elem in doc]))
                if hashed in buckets[band]:
                    buckets[band][hashed].append(doc_id)
                else:
                    buckets[band][hashed] = [doc_id]

        candidate_pairs = []
        for b in buckets:
            for v in b.values():
                if len(v) > 1:
                    for pair in combinations(v, 2):
                        candidate_pairs.append(pair)

        return candidate_pairs
