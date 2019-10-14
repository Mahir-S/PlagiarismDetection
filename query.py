import os
from generate_shingles import generate_shingles
from hash_utils import Permutation_Hash_Generator, vector_hash
from hash_documents import minhash_document,BAND_SIZE,NUM_HASHES,shingle_dict,generate_map
import pickle

def query_all_documents(directory,shingle_pickle_filename,minhash_buckets_filename,num_hashes):
    generate_map(shingle_pickle_filename)
    with open(minhash_buckets_filename, 'rb') as handle:
        minhash_buckets = pickle.load(handle)

    for filename in os.listdir(directory):
        filepath = directory + '/' + filename
        minhash = minhash_document(filepath, num_hashes)
        possible_sources = set()
        for i in range((num_hashes + BAND_SIZE - 1) // BAND_SIZE):
            arr = minhash[i * BAND_SIZE:(i + 1) * BAND_SIZE]
            hash_value = vector_hash(arr)
            if hash_value in minhash_buckets[i]:
                for source_document in minhash_buckets[i][hash_value]:
                    possible_sources.add(source_document)
        if len(possible_sources) != 0:
            print(filename, sorted(possible_sources))


query_all_documents('corpus-20090418', 'shingles.pickle','minhash_buckets.pickle',NUM_HASHES)
