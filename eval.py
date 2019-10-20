from query import query_all_documents
import pandas as pd

def calc_precision(results,df,categories_to_consider):
    average_precision = 0
    total_docs = 0
    for filename,sources in results.items():
        category = df.loc[df['File'] == filename,'Category'].iloc[0]
        if category not in categories_to_consider:
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


def calc_recall(results, df, categories_to_consider):
    average_recall = 0
    total_docs = 0
    for filename, sources in results.items():
        category = df.loc[df['File'] == filename, 'Category'].iloc[0]
        if category not in categories_to_consider:
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


def evaluate_corpus(distance_type, categories_to_consider):
    
    with open('corpus-final09.csv') as f:
        data = pd.read_csv(f)

    results = query_all_documents('corpus-20090418', 'shingles.pickle', distance_type)
    precision = calc_precision(results, data, categories_to_consider)
    recall = calc_recall(results, data, categories_to_consider)
    f = f_value(precision,recall)
    print('********** ' + distance_type + '************')
    print('precision : ',precision)
    print('recall : ',recall)
    print('f value : ',f)
    print()


def evaluate_for_measures(measures=['Jaccard', 'Cosine', 'Hamming'], categories_to_consider = ['light', 'cut']):
    for measure in measures:
        evaluate_corpus(measure,categories_to_consider)
        


if __name__ == '__main__':
    evaluate_for_measures()
