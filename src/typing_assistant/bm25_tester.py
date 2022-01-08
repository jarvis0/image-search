import re
import time

import pandas as pd

from rank_bm25 import BM25Okapi


if __name__ == '__main__':
    corpus = pd.read_csv('data/raw/all_captions.tsv', sep='\t', index_col='id')['caption'].to_list()
    print('number of sentences:', len(corpus))
    tic = time.time()
    tokenized_corpus = [tuple(re.findall(r'\w+', doc)) for doc in corpus]
    print('tokenize corpus', time.time() - tic)
    tic = time.time()
    bm25 = BM25Okapi(tokenized_corpus)
    print('index', time.time() - tic)
    n = 10
    tic = time.time()
    for _ in range(n):
        query = 'running football player player in field across football'
        tokenized_query = list(re.findall(r'\w+', query))
        scores = bm25.get_scores(tokenized_query)
        corpus_scores = list(zip(corpus, scores))
        result = sorted(corpus_scores, key=lambda x: x[1], reverse=True)[: 5]
    print('query', (time.time() - tic) / n)
    for sentence, score in result:
        print(score, sentence)
