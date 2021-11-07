

class Shingling:
    def __init__(self,k):
        self.k = k

    def shingle_document(self,document):
        shingle = []
        for i in range(len(document)-self.k):
            shingle.append(document[i:i+self.k])
        shingle = list(set(shingle))
        print(len(shingle))

if __name__=="__main__":
    f = open("data/2537newsML.txt", "r")
    document = f.read()
    shing = Shingling(5)
    shing.shingle_document(document)