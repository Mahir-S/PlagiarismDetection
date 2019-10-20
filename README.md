# PlagiarismDetection
Plagiarism Detection with Locality Sensitive Hashing

# DATASET USED
https://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html

A set of five short answer questions (A-E) on a variety of topics that might be included in the Computer Science curriculum were created by the authors. For each of these questions a set of answers were obtained using a variety of approaches, some of which simulate cases in which the answer is plagiarised and others that simulate the case in which the answer is not plagiarised
Four levels of plagiarism are represented in the corpus:
1. Near copy
1. Light revision
1. Heavy revision
1. Non-plagiarism

# DISTANCE MEASURES USED
1. JACCARD
1. COSINE
1. HAMMING

# Instructions to Run
1. python generate_shingles.py
1. python hash_documents.py
1. python eval.py

## Brief Description of Files
1. generate_shingles.py : Goes through the corpus,generates shingles and stores it in a set and pickles it for subsequent use
1. hash_utils.py : Contains utility classes for each of the distance families and a separate standalone function for hashing a vector using universal hashing technique
1. hash_documents.py : Contains functions for creating a signature of a document and dividing it into bands and hashing each band.Processes all source documents in corpus and stores their hashes in pickle for each distance measure
1. query.py : Contains functions to find documents similar to query documents
1. eval.py : Queries all query documents,and evaluates average precision and recall from the results for each distance measure


