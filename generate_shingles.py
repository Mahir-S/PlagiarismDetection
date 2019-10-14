import os
import nltk
from text_prepocess_utils import preprocess_text
import pickle

K = 6 #K shingles


def get_hash_value(text):
    #TODO  hash the text and return it
    return text



def generate_shingles(text):
    
    terms = preprocess_text(text)
    shingles = set()
    for word in terms:
        #TODO Get Hashes of each ngram and add that to set instead of the word itself
        if len(word) < K:
            if len(word) > 3:
                shingles.add(word)
        else:
            for i in range(len(word) - K + 1):
                shingles.add(word[i : i + K])
    return shingles

def generate_all_shingles(directory_name):
    shingles = set()
    for filename in os.listdir(directory_name):
        file_path = directory_name + '/' + filename
        with open(file_path,'r') as inp:
            for text in inp:
                document_shingles = generate_shingles(text)
                for shingle in document_shingles:
                    shingles.add(shingle)
    print(len(shingles))
    with open('shingles.pickle','wb') as handle:
        pickle.dump(shingles,handle)


if __name__ == '__main__':
    generate_all_shingles('source')


