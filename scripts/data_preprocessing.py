import argparse
from os.path import join

import pandas as pd


RANDOM_STATE = 42


def preprocess_data(input_file: str, output_path: str, sample_fraction: float):
    df = pd.read_csv(
        input_file,
        sep='\t',
        names=['caption', 'url', 'labels', 'MIDs', 'confidence_score'],
    )
    df['id'] = range(len(df))
    df = df.set_index('id')[['caption', 'url']]

    sampled_df = df.sample(frac=sample_fraction, random_state=RANDOM_STATE)
    sampled_df.to_csv(join(output_path, f'captions_{sample_fraction}.tsv'), sep='\t')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='data/raw.tsv')
    parser.add_argument('--output_path', type=str, default='data')
    parser.add_argument('--sample_fraction', type=float, default=0.1)

    args = parser.parse_args()
    preprocess_data(args.input_file, args.output_path, args.sample_fraction)
