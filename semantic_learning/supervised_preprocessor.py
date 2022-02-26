import argparse
import re
from os.path import join

import pandas as pd


MAX_LABELS = 1
TRAIN_FRACTION = 0.7
VALID_FRACTION = 1 - TRAIN_FRACTION
REGEX = r'[a-z]+'
OUTPUT_FILE_NAME = 'corpus_supervised.txt'
OUTPUT_FILE_NAME_TRAIN = 'corpus_train.txt'
OUTPUT_FILE_NAME_VALID = 'corpus_valid.txt'


def tokenize_supervised(sample):
    labels = ' '.join(['__label__' + '-'.join(label.split(' ')) for label in sample['labels'].split(',')[: MAX_LABELS]]) + ' '
    caption = ' '.join(re.findall(REGEX, sample['caption']))
    return labels + caption + '\n'


def preprocess_supervised_data(input_file: str, output_path: str, train_valid_split: bool):
    df = pd.read_csv(
        input_file,
        sep='\t',
        names=['caption', 'url', 'labels', 'MIDs', 'confidence_score'],
    )[['caption', 'labels']]
    corpus_df = df.dropna()
    corpus_df['tokenized_corpus'] = corpus_df.apply(tokenize_supervised, axis=1)
    corpus = corpus_df['tokenized_corpus'].tolist()
    print(len(corpus), corpus[0])
    if not train_valid_split:
        with open(join(output_path, OUTPUT_FILE_NAME), 'w', encoding='utf-8') as fp:
            for sentence in corpus:
                fp.write(sentence)
    else:
        with open(join(output_path, OUTPUT_FILE_NAME_TRAIN), 'w', encoding='utf-8') as fp:
            for sentence in corpus[: int(len(corpus) * TRAIN_FRACTION)]:
                fp.write(sentence)
        with open(join(output_path, OUTPUT_FILE_NAME_VALID), 'w', encoding='utf-8') as fp:
            for sentence in corpus[-int(len(corpus) * VALID_FRACTION):]:
                fp.write(sentence)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='data/raw.tsv')
    parser.add_argument('--output_path', type=str, default='data')
    parser.add_argument('--train_valid_split', action='store_true', default=True)

    args = parser.parse_args()
    preprocess_supervised_data(args.input_file, args.output_path, args.train_valid_split)
