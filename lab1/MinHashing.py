import random

class MinHashing:
    def __init__(self, n):
        self.n = n
        self.a = [random.randint(0, n ** n) for _ in range(n)]
        self.b = [random.randint(0, n ** n) for _ in range(n)]
        # TODO c has to be prime?
        self.c = 2**32

    def compute_signature(self, shingles):
        signature = []
        for i in range(self.n):
            hashed = []
            for shingle in shingles:
                hashed.append((self.a[i] * shingle + self.b[i]) % self.c)
            signature.append(min(hashed))
        return signature