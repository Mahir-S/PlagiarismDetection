import os
from generate_shingles import generate_shingles
from hash_utils import Permutation_Hash_Generator
import pickle
shingle_dict = dict()

def generate_map(pickle_filename):
    global shingle_dict
    with open(pickle_filename, 'rb') as handle:
        b = pickle.load(handle)
    i = 0
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

def minhash_all_documents(directory,pickle_filename,num_hashes):
    generate_map(pickle_filename)

    for filename in os.listdir(directory):
        filepath = directory + '/' + filename
        minhash_document(filepath,num_hashes)        


def hash_all_documnents(directory,pickle_filename,distance_type,num_hashes):
    if distance_type == 'Jaccard':
        minhash_all_documents(directory,pickle_filename,num_hashes)


hash_all_documnents('source', 'shingles.pickle', 'Jaccard', 10)
