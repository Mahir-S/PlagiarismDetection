import os
from generate_shingles import generate_shingles
from hash_utils import Permutation_Hash_Generator,vector_hash
import pickle
shingle_dict = dict()
NUM_HASHES = 200
BAND_SIZE = 5

def generate_map(pickle_filename):
    global shingle_dict
    with open(pickle_filename, 'rb') as handle:
        b = pickle.load(handle)
    i = 0
    b = sorted(b)
    for item in b:
        shingle_dict[item] = i
        i += 1


def minhash_document(filepath,num_hashes):
    shingles = set()
    with open(filepath, 'rb') as inp:
            for text in inp:
                text = str(text)
                document_shingles = generate_shingles(text)
                
                for shingle in document_shingles:
                    shingles.add(shingle)
    
    N = len(shingle_dict)
    hasher = Permutation_Hash_Generator(N,num_hashes)
    ans = [N  +  1 for i in range(num_hashes)]
    for shingle in shingles:
        if shingle not in shingle_dict:
            continue
        row = shingle_dict[shingle]
        for i in range(num_hashes):
            ans[i] = min(ans[i],hasher.f(row,i))
    return ans

def minhash_all_documents(directory,pickle_filename,num_hashes):
    generate_map(pickle_filename)
    minhash_buckets = [dict() for i in range((num_hashes + BAND_SIZE - 1) // BAND_SIZE)]
    for filename in os.listdir(directory):
        filepath = directory + '/' + filename
        minhash = minhash_document(filepath,num_hashes)        
        for i in range((num_hashes + BAND_SIZE - 1) // BAND_SIZE):
            arr = minhash[i * BAND_SIZE:(i + 1) * BAND_SIZE]
            hash_value = vector_hash(arr)
            if hash_value not in minhash_buckets[i]:
                minhash_buckets[i][hash_value] = [filename]
            else : 
                minhash_buckets[i][hash_value].append(filename)
    
    with open('minhash_buckets.pickle', 'wb') as handle:
        pickle.dump(minhash_buckets, handle)

def hash_all_documnents(directory,pickle_filename,distance_type,num_hashes):
    if distance_type == 'Jaccard':
        minhash_all_documents(directory,pickle_filename,num_hashes)




hash_all_documnents('source', 'shingles.pickle', 'Jaccard', NUM_HASHES)
