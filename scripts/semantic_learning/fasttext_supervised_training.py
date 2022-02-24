import os

import fasttext

import matplotlib.pyplot as plt

import numpy as np


dim = 100
epoch = 7
loss_f = 'hs'
model = fasttext.train_supervised(
    input='data/corpus_train.txt',
    # lr=0.1,
    # dim=dim,
    ws=5,
    # epoch=epoch,
    minCount=5,
    minn=0,
    maxn=0,
    neg=5,
    # wordNgrams=1,
    # loss=loss_f,
    bucket=2000000,
    thread=6,
    lrUpdateRate=100,
    t=0.0001,
    label='__label__',
    verbose=2,
    autotuneValidationFile='data/corpus_valid.txt',
    autotunePredictions=3,
    autotuneDuration=28800,
)
training_name = 'fasttext_supervised'
training_path = 'scripts/semantic_learning/trainings/' + training_name + '/'
os.makedirs(training_path, exist_ok=True)
model.save_model(training_path + 'supervised_model.bin')

log_path = 'scripts/semantic_learning/temp/'
with open(log_path + 'training.log') as fp:
    loss = [float(line.split()[7]) for line in fp.readlines() if line.startswith('Progress:')]
plt.figure(figsize=(16, 4))
plt.plot(loss)
ticks = np.linspace(0, len(loss) - 1, epoch, dtype=int)
plt.xticks(ticks, range(epoch))
plt.grid()
plt.savefig(training_path + 'progress.png')
plt.close()
