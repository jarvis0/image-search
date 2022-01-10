import fasttext


model = fasttext.train_unsupervised(
    input='data/raw/corpus.txt',
    model='skipgram',
    lr=0.05,
    dim=200,
    ws=5,
    epoch=50,
    minCount=5,
    minn=3,
    maxn=6,
    neg=5,
    wordNgrams=1,
    loss='ns',
    bucket=2000000,
    thread=6,
    lrUpdateRate=100,
    t=0.0001,
    verbose=2,
)
model.save_model('data/bin/fasttext_200_10.bin')
