import random

class Permutation_Hash_Generator:
    
    def __init__(self,N,num_hashes):
        self.N = N
        self.P = 1000000007
        # self.count = 0
        random.seed(N)
        self.a = [2 * random.randint(0,(self.P - 2) // 2) + 1 for i in range(num_hashes)]
        random.seed(N / 2)
        self.b = [random.randint(1,self.P - 1) for i in range(num_hashes)]

    def f(self,x,i):
        return 1 + ((self.a[i] * x  + self.b[i])%self.P)%self.N

def vector_hash(arr):
    h = 2166136261
    t = 0
    for i in range(len(arr)):
        t = (h * 6777619) & 4294967295
        h = t ^ arr[i]
    return h

