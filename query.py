import os
from generate_shingles import generate_shingles
from hash_utils import Permutation_Hash_Generator, vector_hash,COSINE_HASH_THRESHOLD
from hash_documents import minhash_document,cosine_hash_single_document,shingle_dict,generate_map,euclid_hash_single_document
from hash_documents import BAND_SIZE,COSINE_BAND_SIZE,NUM_HASHES,EUCLID_BAND_SIZE
import pickle

def query_all_documents_minhash(directory,shingle_pickle_filename,minhash_buckets_filename,num_hashes):
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


def query_all_documents_cosinehash(directory, shingle_pickle_filename, cosinehash_buckets_filename, num_hashes):
    generate_map(shingle_pickle_filename)
    with open(cosinehash_buckets_filename, 'rb') as handle:
        cosinehash_buckets = pickle.load(handle)

    for filename in os.listdir(directory):
        filepath = directory + '/' + filename
        cosinehash = cosine_hash_single_document(filepath, num_hashes)
        possible_sources = dict()

        for i in range((num_hashes + COSINE_BAND_SIZE - 1) // COSINE_BAND_SIZE):
            arr = cosinehash[i * COSINE_BAND_SIZE:(i + 1) * COSINE_BAND_SIZE]
            hash_value = vector_hash(arr)

            if hash_value in cosinehash_buckets[i]:
                for source_document in cosinehash_buckets[i][hash_value]:
                    if source_document not in possible_sources:
                        possible_sources[source_document] = 1
                    else :
                        possible_sources[source_document] += 1
        ans = []
        if len(possible_sources) != 0:
            for source_document,frequency in possible_sources.items():
                if frequency > COSINE_HASH_THRESHOLD: #change if threshold becomes dynamic
                    ans.append(source_document)
        if(len(ans) != 0):
            print(filename, sorted(ans))


def query_all_documents_euclidhash(directory, shingle_pickle_filename, euclidhash_buckets_filename, num_hashes):
    generate_map(shingle_pickle_filename)

    with open(euclidhash_buckets_filename, 'rb') as handle:
        euclidhash_buckets = pickle.load(handle)

    for filename in os.listdir(directory):
        
        filepath = directory + '/' + filename
        euclidhash = euclid_hash_single_document(filepath, num_hashes)
        possible_sources = set()
        
        for i in range((num_hashes + EUCLID_BAND_SIZE - 1) // EUCLID_BAND_SIZE):
    
            arr = euclidhash[i * EUCLID_BAND_SIZE:(i + 1) * EUCLID_BAND_SIZE]
            hash_value = vector_hash(arr)
    
            if hash_value in minhash_buckets[i]:
                for source_document in minhash_buckets[i][hash_value]:
                    possible_sources.add(source_document)
        
        if len(possible_sources) != 0:
            print(filename, sorted(possible_sources))

def query_all_documents(directory,shingle_pickle_filename,num_hashes,distance_type):
    
    if distance_type == 'Jaccard':
        query_all_documents_minhash(directory,shingle_pickle_filename,'minhash_buckets.pickle',num_hashes)
    
    if distance_type == 'Cosine':
        query_all_documents_cosinehash(directory,shingle_pickle_filename,'cosinehash_buckets.pickle',num_hashes)
    
    if distance_type == 'Euclidean':
        pass



query_all_documents('corpus-20090418', 'shingles.pickle',NUM_HASHES,'Cosine')
