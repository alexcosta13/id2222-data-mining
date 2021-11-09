import random


class MinHashing:
    def __init__(self, n):
        self.n = n
        self.a = [random.randint(0, n ** n) for _ in range(n)]
        self.b = [random.randint(0, n ** n) for _ in range(n)]
        self.c = 4294971673

    def compute_signature(self, shingles):
        signature = []
        for i in range(self.n):
            min_hash = self.c
            for shingle in shingles:
                hash_value = (self.a[i] * shingle + self.b[i]) % self.c
                if hash_value < min_hash:
                    min_hash = hash_value
            signature.append(min_hash)
        return signature
