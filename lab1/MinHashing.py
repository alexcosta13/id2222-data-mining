import random


class MinHashing:
    def __init__(self, n):
        """
        Calculates list of a's and b's for n hash functions in the form of (a * x + b) % c
        :param n: number of hash signatures to be calculated
        """
        self.n = n
        self.a = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
        self.b = [random.randint(0, 2 ** 32 - 1) for _ in range(n)]
        self.c = 4294971673

    def compute_signature(self, shingles):
        """
        Computes a signature of length n (typically shorter than the input) by applying n hash functions
        in the form of (a * x + b) % c, and taking the minimum result for each of those functions.
        :param shingles: list of integers
        :return: list of integers
        """
        signature = []
        for i in range(self.n):
            min_hash = self.c
            for shingle in shingles:
                hash_value = (self.a[i] * shingle + self.b[i]) % self.c
                if hash_value < min_hash:
                    min_hash = hash_value
            signature.append(min_hash)
        return signature
