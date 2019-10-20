import random
import numpy as np

COSINE_HASH_THRESHOLD = 5

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
        return ((self.a[i] * x  + self.b[i])%self.P)%self.N

def vector_hash(arr):
    h = 2166136261
    t = 0
    for i in range(len(arr)):
        t = (h * 6777619) & 4294967295
        h = t ^ arr[i]
    return h

class Cosine_Family:
    
    def __init__(self,num_hashes,M = 4):#DO NOT INCREASE M
        self.M = M
        self.phg = Permutation_Hash_Generator(M,num_hashes)
        np.random.seed(M)
        self.arr = np.random.randint(0,2,M)
        self.arr = np.where(self.arr == 0, -1, self.arr)
        self.threshold = COSINE_HASH_THRESHOLD
    
    def hash(self,row,index):
        return self.arr[self.phg.f(row,index)]


    

class Hamming_Family:
    def __init__(self, N, num_hashes, M = 7):
        self.N = N
        np.random.seed(N)
        self.arr = [np.random.randint(0,N,M) for i in range(num_hashes)]


