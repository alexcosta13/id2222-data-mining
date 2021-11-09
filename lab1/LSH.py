from itertools import combinations


class LSH:
    def __init__(self, sim_threshold, b, r, n_buckets):
        self.sim_threshold = sim_threshold
        self.b = b
        self.r = r
        self.n_buckets = n_buckets

    def find_candidates(self, signatures):
        assert self.b * self.r == len(signatures), "b * r != n"
        buckets = [[[] for _ in range(self.n_buckets)] for _ in range(self.b)]
        for band in range(self.b):
            for doc_id, doc in enumerate(signatures):
                doc = doc[band*self.r:(band+1)*self.r]
                hashed = hash("".join([str(elem) for elem in doc])) % self.n_buckets
                buckets[band][hashed].append(doc_id)

        candidate_pairs = []
        for i in buckets:
            for j in i:
                if len(j) > 1:
                    for pair in combinations(j, 2):
                        candidate_pairs.append(pair)

        return candidate_pairs
