import os
from generate_shingles import generate_shingles
from hash_utils import Permutation_Hash_Generator,vector_hash,Cosine_Family,Hamming_Family
import pickle

NUM_HASHES = 200
BAND_SIZE = 5
COSINE_BAND_SIZE = 5
HAMMING_BAND_SIZE = 3

shingle_dict = dict()
reverse_shingle_dict = dict()

def generate_map(pickle_filename):
    global shingle_dict
    global reverse_shingle_dict

    if len(shingle_dict) > 0:
        return

    with open(pickle_filename, 'rb') as handle:
        b = pickle.load(handle)
    i = 0
    b = sorted(b)
    for item in b:
        shingle_dict[item] = i
        reverse_shingle_dict[i] = item
        i += 1

def get_shingle_set(filepath):
    shingles = set()
    with open(filepath, 'rb') as inp:
            for text in inp:
                text = str(text)
                document_shingles = generate_shingles(text)
                for shingle in document_shingles:
                    shingles.add(shingle)
    return shingles

def minhash_document(filepath,num_hashes):
    shingles = get_shingle_set(filepath)
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

def cosine_hash_single_document(filepath,num_hashes):
    shingles = get_shingle_set(filepath)
    cosine_hasher = Cosine_Family(num_hashes)
    ans = [0 for i in range(num_hashes)]
    for shingle in shingles:
        if shingle not in shingle_dict:
            continue
        row = shingle_dict[shingle]
        for i in range(num_hashes):
            ans[i] += cosine_hasher.hash(row,i)
    
    for i in range(num_hashes):
        if ans[i] > 0:
            ans[i] = 1
        else : 
            ans[i] = 0
    # print(filepath,ans)
    return ans

def cosine_hash_all_documents(directory,pickle_filename,num_hashes):
    generate_map(pickle_filename)
    cosinehash_buckets = [dict() for i in range((num_hashes + COSINE_BAND_SIZE - 1) // COSINE_BAND_SIZE)]
    
    for filename in os.listdir(directory):
        filepath = directory + '/' + filename
        cosine_hash = cosine_hash_single_document(filepath,num_hashes)
        
        for i in range((num_hashes + COSINE_BAND_SIZE - 1) // COSINE_BAND_SIZE):
            
            arr = cosine_hash[i * COSINE_BAND_SIZE:(i + 1) * COSINE_BAND_SIZE]
            hash_value = vector_hash(arr)
            
            if hash_value not in cosinehash_buckets[i]:
                cosinehash_buckets[i][hash_value]=[filename]
            else:
                cosinehash_buckets[i][hash_value].append(filename)
    
    with open('cosinehash_buckets.pickle', 'wb') as handle:
        pickle.dump(cosinehash_buckets, handle)


def hamming_hash_single_document(filepath, num_hashes):
    shingles = get_shingle_set(filepath)
    hamming_hasher = Hamming_Family(len(shingle_dict),num_hashes)
    
    ans = [0 for i in range(num_hashes)]
    for i,hash_arr in enumerate(hamming_hasher.arr):
        for index,element in enumerate(hash_arr):
            corres_shingle = reverse_shingle_dict[element]
            if corres_shingle in shingles:
                ans[i] += (1 << index)
    # print(filepath,ans)
    return ans

def hamming_hash_all_documents(directory, pickle_filename, num_hashes):
    generate_map(pickle_filename)
    hamminghash_buckets = [dict() for i in range((num_hashes + HAMMING_BAND_SIZE - 1) // HAMMING_BAND_SIZE)]

    for filename in os.listdir(directory):
        filepath = directory + '/' + filename
        hamming_hash = hamming_hash_single_document(filepath, num_hashes)

        for i in range((num_hashes + HAMMING_BAND_SIZE - 1) // HAMMING_BAND_SIZE):

            arr = hamming_hash[i * HAMMING_BAND_SIZE:(i + 1) * HAMMING_BAND_SIZE]
            hash_value = vector_hash(arr)
            if hash_value not in hamminghash_buckets[i]:
                hamminghash_buckets[i][hash_value] = [filename]
            else:
                hamminghash_buckets[i][hash_value].append(filename)

    with open('hamminghash_buckets.pickle', 'wb') as handle:
        pickle.dump(hamminghash_buckets, handle)

def hash_all_documnents(directory,pickle_filename,distance_type,num_hashes):
    if distance_type == 'Jaccard':
        minhash_all_documents(directory,pickle_filename,num_hashes)

    if distance_type == 'Cosine':
        cosine_hash_all_documents(directory,pickle_filename,num_hashes)

    if distance_type == 'Hamming':
        hamming_hash_all_documents(directory,pickle_filename,num_hashes)

if __name__ == '__main__':
    hash_all_documnents('source','shingles.pickle','Jaccard',NUM_HASHES)
    hash_all_documnents('source', 'shingles.pickle', 'Hamming', NUM_HASHES)
    hash_all_documnents('source','shingles.pickle','Cosine',NUM_HASHES)

