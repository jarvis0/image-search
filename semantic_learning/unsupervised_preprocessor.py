import argparse
import re
from os.path import join

import pandas as pd


REGEX = r'[a-z]+'
OUTPUT_FILE_NAME = 'corpus_unsupervised.txt'


def tokenize_unsupervised(sample):
    caption = ' '.join(re.findall(REGEX, sample['caption']))
    return caption + '\n'


def preprocess_unsupervised_data(input_file: str, output_path: str):
    df = pd.read_csv(
        input_file,
        sep='\t',
        names=['caption', 'url', 'labels', 'MIDs', 'confidence_score'],
    )[['caption']]
    corpus_df = df.dropna()
    corpus_df['tokenized_corpus'] = corpus_df.apply(tokenize_unsupervised, axis=1)
    corpus = corpus_df['tokenized_corpus'].tolist()
    print(len(corpus), corpus[0])
    with open(join(output_path, OUTPUT_FILE_NAME), 'w', encoding='utf-8') as fp:
        for sentence in corpus:
            fp.write(sentence)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='data/raw.tsv')
    parser.add_argument('--output_path', type=str, default='data')

    args = parser.parse_args()
    preprocess_unsupervised_data(args.input_file, args.output_path)
