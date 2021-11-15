class CompareSignatures:
    def compare(self, sign1, sign2):
        equal = 0
        for elem1, elem2 in zip(sign1, sign2):
            if elem1 == elem2:
                equal += 1
        return equal / len(sign1)
