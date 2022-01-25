import time
from os.path import join

from .indexing import load_collection, load_images_handler, load_lexicon


def load_init(root: str):
    tic = time.time()
    collection = load_collection(join(root, 'binaries/collection.pkl'))
    print('load collection', time.time() - tic)
    tic = time.time()
    lexicon = load_lexicon(join(root, 'binaries/lexicon.pkl'))
    print('load lexicon', time.time() - tic)
    print('lexicon entries', len(lexicon.get_words_lexicon()))
    tic = time.time()
    images_handler = load_images_handler(join(root, 'binaries/images_handler.pkl'))
    print('load images handler', time.time() - tic)
    return collection, lexicon, images_handler
