from query import query_all_documents
import pandas as pd

def calc_precision(results,df):
    average_precision = 0
    total_docs = 0
    for filename,sources in results.items():
        category = df.loc[df['File'] == filename,'Category'].iloc[0]
        if category != 'light' and category != 'cut':
            continue
        total = len(sources)
        if total == 0:
            continue
        value = 0
        for source_document in sources:
            text = source_document
            doc_name = text.split('.')[0][-1]
            query_name = filename.split('.')[0][-1]
            if doc_name == query_name:
                value += 1
        
        average_precision += value / total
        total_docs += 1
    average_precision /= total_docs
    return average_precision

def calc_recall(results, df):
    average_recall = 0
    total_docs = 0
    for filename, sources in results.items():
        category = df.loc[df['File'] == filename, 'Category'].iloc[0]
        if category != 'light' and category != 'cut':
            continue
        
        value = 0
        for source_document in sources:
            text = source_document
            doc_name = text.split('.')[0][-1]
            query_name = filename.split('.')[0][-1]
            if doc_name == query_name:
                value += 1

        average_recall += value
        total_docs += 1
    average_recall /= total_docs
    return average_recall

def f_value(precision,recall):
    return (2 * precision * recall) / (precision + recall)

def evaluate_corpus(distance_type):
    
    with open('corpus-final09.csv') as f:
        data = pd.read_csv(f)

    results = query_all_documents('corpus-20090418', 'shingles.pickle', distance_type)
    precision = calc_precision(results,data)
    recall = calc_recall(results,data)
    f = f_value(precision,recall)
    print(precision,recall,f)

evaluate_corpus('Euclid')
