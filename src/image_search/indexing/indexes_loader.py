import time
from typing import Tuple

from . import (Collection, ImagesHandler, Lexicon, load_collection,
               load_images_handler, load_lexicon)


def load_indexes(root: str) -> Tuple[Collection, Lexicon, ImagesHandler]:
    tic = time.time()
    collection = load_collection(root)
    print('load collection', time.time() - tic)
    tic = time.time()
    lexicon = load_lexicon(root)
    print('load lexicon', time.time() - tic)
    print('lexicon entries', len(lexicon.terms_lexicon))
    tic = time.time()
    images_handler = load_images_handler(root)
    print('load images handler', time.time() - tic)
    return collection, lexicon, images_handler
