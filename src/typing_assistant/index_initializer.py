import time

import pandas as pd

from .indexing import Collection, ImagesHandler, InvertedIndex, Lexicon


if __name__ == '__main__':
    df = pd.read_csv('data/captions_0.1.tsv', sep='\t', index_col='id')
    corpus = df['caption'].to_dict()
    print('number of sentences:', len(corpus))
    tic = time.time()
    collection = Collection()
    collection.build_collection(corpus)
    print('build collection', time.time() - tic)
    tic = time.time()
    inv_index = InvertedIndex(collection)
    inv_index.index_collection()
    print('build index', time.time() - tic)
    tic = time.time()
    lexicon = Lexicon()
    lexicon.build_lexicon(collection, inv_index)
    print('build lexicon', time.time() - tic)
    tic = time.time()
    images_url = df['url'].to_dict()
    images_handler = ImagesHandler()
    images_handler.set_images_url(images_url)
    print('set images url', time.time() - tic)

    print('lexicon entries', len(lexicon.get_words_lexicon()))
    tic = time.time()
    collection.dump()
    print('dump collection', time.time() - tic)
    tic = time.time()
    lexicon.dump()
    print('dump lexicon', time.time() - tic)
    tic = time.time()
    images_handler.dump()
    print('dump images', time.time() - tic)
