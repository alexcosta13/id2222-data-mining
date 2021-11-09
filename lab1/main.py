from os import listdir
import sys

from CompareSignatures import CompareSignatures
from MinHashing import MinHashing
from Shingling import Shingling
from LSH import LSH

K = 5
N = 50
N_DOCUMENTS = 50
B = 10
R = 5

if __name__ == "__main__":
    shing = Shingling(K)
    minhash = MinHashing(N)
    compare_sign = CompareSignatures()
    threshold = (1 / B) ** (1 / R)
    lsh = LSH(threshold, B, R, N_DOCUMENTS)
    files = [f for f in listdir("data")][:N_DOCUMENTS]
    sign_matrix = []

    for file in files:
        f = open("data/" + file, "r")
        doc = f.read()
        hashed_shing = shing.shingle_document(doc)
        col_doc = minhash.compute_signature(hashed_shing)
        sign_matrix.append(col_doc)
    candidate_pairs = lsh.find_candidates(sign_matrix)

    total_documents = 0
    for pair in candidate_pairs:
        i, j = pair
        if (compare_sign.compare(sign_matrix[i], sign_matrix[j])) > threshold:
            total_documents += 1
            print(f"Document {i} and Document {j} are very similar :) ")

    print(
        f"There are {total_documents} pairs of similar documents. We had {len(candidate_pairs)} candidate pairs."
    )

    sys.exit(0)
    for i in range(N_DOCUMENTS):
        for j in range(i + 1, N_DOCUMENTS):
            if (compare_sign.compare(sign_matrix[i], sign_matrix[j])) > THRESHOLD:
                print(
                    f"Document {files[i]} and Document {files[j]} are very similar :) "
                )
