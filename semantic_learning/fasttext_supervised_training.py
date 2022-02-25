import os

import fasttext

import matplotlib.pyplot as plt

import numpy as np


dim = 100
epoch = 10
loss_f = 'hs'
lr = 0.2
n_grams = 1
model = fasttext.train_supervised(
    input='data/corpus_train.txt',
    lr=lr,
    dim=dim,
    ws=5,
    epoch=epoch,
    minCount=5,
    minn=0,
    maxn=0,
    neg=5,
    wordNgrams=n_grams,
    loss=loss_f,
    bucket=2000000,
    thread=6,
    lrUpdateRate=100,
    t=0.0001,
    label='__label__',
    verbose=2,
)
training_name = f'fasttext_dim-{dim}_epoch-{epoch}_loss-{loss_f}_lr-{lr}_ngrams-{n_grams}'
training_path = 'scripts/semantic_learning/trainings/supervised/' + training_name + '/'
os.makedirs(training_path, exist_ok=True)
_, precision, recall = model.test('data/corpus_valid.txt', k=1)
f1_score = 2 * (recall * precision) / (recall + precision)
model.save_model(training_path + 'supervised_model.bin')

log_path = 'scripts/semantic_learning/temp/'
with open(log_path + 'training.log') as fp:
    loss = [float(line.split()[7]) for line in fp.readlines() if line.startswith('Progress:')]
plt.figure(figsize=(16, 4))
plt.title(f'f1_score = {f1_score}, precision = {precision}, recall = {recall}')
plt.plot(loss)
ticks = np.linspace(0, len(loss) - 1, epoch, dtype=int)
plt.xticks(ticks, range(epoch))
plt.grid()
plt.savefig(training_path + 'progress.png')
plt.close()
