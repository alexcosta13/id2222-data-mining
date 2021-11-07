from os import listdir

from CompareSignatures import CompareSignatures
from MinHashing import MinHashing
from Shingling import Shingling

N_DOCUMENTS = 50
THRESHOLD = 0.8

if __name__ == "__main__":
    shing = Shingling(5)
    minhash = MinHashing(150)
    compare_sign = CompareSignatures()
    print(len([f for f in listdir("data")]))
    files = [f for f in listdir("data")][:N_DOCUMENTS]
    sign_matrix = []

    for file in files:
        f = open("data/" + file, "r")
        doc = f.read()
        hashed_shing = shing.shingle_document(doc)
        col_doc = minhash.compute_signature(hashed_shing)
        sign_matrix.append(col_doc)

    for i in range(N_DOCUMENTS):
        for j in range(i+1, N_DOCUMENTS):
            if (compare_sign.compare(sign_matrix[i], sign_matrix[j])) > THRESHOLD:
                print(f"Document {files[i]} and Document {files[j]} are very similar :) ")
