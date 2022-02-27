<h1 align="center">
  <a href="https://github.com/jarvis0/image-search">
    <!-- Please provide path to your logo here -->
    <img src="docs/images/logo.png" alt="Logo" width="100" height="100">
  </a>
</h1>

<div align="center">
  Image Search
  <br />
  <a href="#about"><strong>Explore the demos »</strong></a>
  <br />
  <a href="https://github.com/jarvis0/image-search/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/jarvis0/image-search/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  ·
  <a href="https://github.com/jarvis0/image-search/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>
<div align="center">

[![Project license](https://img.shields.io/badge/license-all%20rights%20reserved-lightgrey)](LICENSE)
[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-orange)](https://github.com/jarvis0/image-search/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
[![code by jarvis0](https://img.shields.io/badge/%3C%2F%3E%20by-jarvis0-lightblue)](https://github.com/jarvis0)
![python](https://img.shields.io/badge/python-3.8-blue)
![lint](https://img.shields.io/badge/lint-passing-brightgreen)
![mypy](https://img.shields.io/badge/mypy-passing-brightgreen)
</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Solution overview](#solution-overview)
  - [Use case 1 — caption autocompletion](#use-case-1--caption-autocompletion)
  - [Use case 2 — term autocompletion](#use-case-2--term-autocompletion)
  - [Use case 3 — term autocorrection](#use-case-3--term-autocorrection)
  - [Use case 4 — term prediction](#use-case-4--term-prediction)
- [Roadmap](#roadmap)
- [Support](#support)
- [Project assistance](#project-assistance)
- [Contributing](#contributing)
- [Authors & contributors](#authors--contributors)
- [Acknowledgements](#acknowledgements)

</details>

---

## About

This project is a software application for searching and displaying images from a dataset of ~2M images gathered on the Internet. The images can be searched through an input text that specifies a caption or a description of the desired images. For a faster and more effective retrieval, the user is intelligently assisted while typing.

The application can be employed in two ways. One is through a [Command-Line Interface (CLI)](https://en.wikipedia.org/wiki/Command-line_interface), the other through a [Flask WebApp](https://github.com/pallets/flask) accessible from common browsers. As soon as the user types, several typing suggestions are generated and proposed as we report in the following use cases:
1. <b><i>(caption autocompletion)</i></b> a list of complete image captions that are compatible with the text inserted so far;
2. <b><i>(term autocompletion)</i></b> a term completion compatible with the current term being inserted and the previous typed terms;
3. <b><i>(term autocorrection)</i></b> a term correction of the last inserted term if applicable;
4. <b><i>(term prediction)</i></b> a prediction of the next term.

The idea for this project originated from a Google competition about [Automatic Image Captioning](https://ai.google.com/research/ConceptualCaptions/home). Automatic image captioning is the task of automatically producing a english natural-language description for an image. Even though the purpose of the competition is different from that of this project, Google published a dataset consisting of ~2M images annotated with captions. The dataset is indeed used for this project for searching through the available captions as a text retrieval task. Each caption can then be mapped to a URL where the image can be downloaded and shown to the user.
<br>
A data analysis notebook can be found [here](notebooks/data_analysis.ipynb).

<details>
<summary>Demos</summary>
<img src="docs/images/screenshot.png" title="Login Page" width="100%">
</details>

## Getting Started

### Prerequisites
This application relies on [fastText](https://github.com/facebookresearch/fastText). It builds on modern Mac OS and Linux distributions. Since it uses some C++11 features, it requires a compiler with good C++11 support. These include:
- (g++-4.7.2 or newer) or (clang-3.3 or newer)

The compilation is carried out using a Makefile, so you will need to have a working make. If you want to use cmake you need at least version 2.8.9. For further information, refer [here](https://github.com/facebookresearch/fastText).

The code has been developed using Python v3.8.11 and Anaconda v4.10.1. We cannot guarantee proper functioning for lower versions.

### Installation

We encourage you to create a fresh Anaconda environment for the installation.
```sh
git clone https://github.com/jarvis0/image-search.git
cd image-search
pip install .
```

At this point, you will need to download the database containing the image captions and their corresponding URLs. You can find the file at this [link](https://storage.cloud.google.com/conceptual-captions-v1-1-labels/Image_Labels_Subset_Train_GCC-Labels-training.tsv?_ga=2.234395421.-20118413.1607637118), provided that you are logged in with a valid Google account. Once the file is downloaded you will have to run the following command:
```sh
python scripts/data_preprocessing.py --sample_fraction <value in the interval (0, 1]>
```
By default this command assumes the downloaded file to be under the folder `data` and to be named as `raw.tsv`. You can specify a different input path and file name by using the `--input_file` argument. The output of this command will be a file named `captions_{sample_fraction}.tsv` under the `data` folder. The number of selected captions will depend on the `--sample_fraction` argument. If you specify `--sample_fraction=1`, then all the captions from the original dataset will be considered. This file will contain only three columns:
- caption UID (`id`);
- caption text (`caption`);
- image URL (`url`).

You can skip the data download and preprocessing steps if you can provide your own TSV dataset of captions having the same columns as specified.

Also, you will need to train a semantic word embeddings model. But first, we need to prepare the training data using the following command:

```sh
python semantic_learning/unsupervised_preprocessing.py
```
By default this command assumes the file to be preprocessed for training to be under the folder `data` and to be named as `raw.tsv`. You can specify a different input path and file name by using the `--input_file` argument. The output of this command will be a training file named `corpus_unsupervised.txt` under the `data` folder.

At this point, you can run the training by executing the following instruction:
```sh
python semantic_learning/unsupervised_training.py
```
By default this command assumes the preprocessed input file to be under the folder `data` and to be named as `corpus_unsupervised.txt`. You can specify a different train path and file name by using the `--train_file` argument. The output of this command will be a binary file containing the trained model named `semantic_model.bin` under the `binaries` folder.

## Usage

To initialize the search indices and components, you will have to run the following:
```sh
python -m image_search.app_init --input_file <file_path>
```
Where `<file_path>` is `data/captions_{sample_fraction}.tsv` as specified in the installation instructions. This command can take from a few seconds to some minutes, according to the size of the input file. However, it is important to highlight that this process is memory-intensive and therefore can require a lot of memory that grows roughly in a linear way with respect to the input dataset size. To give you some reference points:
- ~200k captions require <2 GB;
- ~1M captions require <6GB;
- ~2M captions require <14 GB.

Please, consider that this step will be run only once for a given dataset and will make the usage of the actual application very fast.

At this point, you can launch the application either through a [CLI](https://en.wikipedia.org/wiki/Command-line_interface) or a [Flask WebApp](https://github.com/pallets/flask) in these ways:
```sh
python -m image_search.app_cli
```
or
```sh
python -m image_search.app_web
```

## Solution overview

The key idea of making text search fast at runtime is to use an [Inverted Index](https://en.wikipedia.org/wiki/Inverted_index) as a core data structure. In fact, the initialization of the application is aimed at building such an inverted index that is a mapping from each unique term in the dataset to the list of captions where those terms appear. This way, the search for all the captions containing a given input term is $\mathcal{O}(1)$ instead of linear in the number of captions. From the inverted index, we filter out the top 1% of most frequent words intersected with a list of English [stop words](https://en.wikipedia.org/wiki/Stop_word). Stop words removal not only reduces the size of the inverted index but will also make the search much faster because very frequent and, therefore, irrelevant words are ruled out.

### Use case 1 — caption autocompletion

We rely on [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) ranking function that is state-of-the-art in modern search engines. It estimates the relevance of a document with respect to a given search input. The key idea of such ranking function is to rely on a [vector space](https://en.wikipedia.org/wiki/Vector_space_model) representation of text. That is, to have an algebraic model for representing text as vectors of term identifiers. Each dimension of the vector model corresponds to a separate term. If a term (i.e., a word in our case) occurs in a document (i.e., a caption in our case), its value in the vector is non-zero. There are several ways to characterize the values in the vector model, one of this is indeed Okapi BM25 and it is grounded in the [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) weighting schema. It is a numerical statistic that is intended to reflect how important a term is to a document in a collection. The TF-IDF value increases proportionally to the number of times a term appears in the document and is offset by the number of documents in the collection that contain the term, which helps to adjust for the fact that some terms appear more frequently in general.
<br>
TF-IDF schema comes with several limitations. We address two of them since, in our opinion, are the most relevant for this project:
1. search terms must precisely match document terms;
2. documents with similar context but different term vocabulary are not associated.

To overcome these issues, we employ an input text expansion strategy. Query expansion is addressed on two sides:
1. for each input term, we identify strings that match the input term approximately;
2. for each input term, we identify strings that are neighbors of the input term in a semantic latent space.

The first solution is carried out by employing the [Gestalt Pattern Matching](https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching) algorithm. It is a string-matching algorithm that exploits the longest common substrings for determining a similarity score (between zero and one) of two strings. Python comes with a standard library named [difflib](https://docs.python.org/3/library/difflib.html) for computing such similarity score. The authors claim that this score does not reflect minimal edit sequences, but does tend to yield scores that "look right" to people. Therefore, for the query expansion, we will consider pairs of strings whose similarity score is above a certain threshold. The threshold is set arbitrarily high to avoid the increase of false-positive matches while still increasing some sort of string matching flexibility.

The second solution considers the usage of [semantic word embeddings](https://en.wikipedia.org/wiki/Word_embedding). The key idea is to build a representation of words in the form of a real-valued vector that encodes the meaning of the word such that the words that are closer in the vector space are expected to be similar in meaning. In linguistics, word embeddings were discussed in the research area of distributional semantics. It aims to quantify and categorize semantic similarities between linguistic items based on their distributional properties in large samples of language data. The underlying idea is that "a word is characterized by the company it keeps. Therefore, many of the available models are able to express the semantic relationships of words by means of a co-occurrence schema of the words.
<br>
To this purpose, we rely on [fastText](https://github.com/facebookresearch/fastText) from Facebook AI Research that allows training an unsupervised model of the text. The corresponding research paper is available [here](https://arxiv.org/pdf/1607.01759.pdf). A thoughtful overview of word embeddings models can be found [here](https://medium.com/@kashyapkathrani/all-about-embeddings-829c8ff0bf5b).
<br>
We conducted several experiments involving different hyperparameter configurations and then manually evaluated some sample similarities between pairs of words (e.g., [here](notebooks/unsupervised_models_check.ipynb)). After some trials, we selected the following hyperparameter configuration (for all the others, we kept the default values):
- `dim=100`: we experimented that enlarging the model size favored overfitting;
- `epoch=7`: the default number of epochs (5) was insufficient as the loss plot did not converge;
- `minn=0` and `maxn=0`: since we already deal with misspelled words, it is redundant to model character n-grams;
- `wordNgrams=1`: captions have on average ~10 words, hence it would be overwhelming considering, for instance, word bi-grams;
- `loss='hs'`: this loss ([hierarchical softmax](https://www.iro.umontreal.ca/~lisa/pointeurs/hierarchical-nnlm-aistats05.pdf)) is an approximation of the softmax loss that is more efficient at a negligible accuracy cost for our purpose.

The original dataset from the Google competition came with classification labels. Hence, we gave supervised learning a try. As expected, the results are worse than those of the unsupervised learning [here](notebooks/supervised_models_check.ipynb). The main reason for this is that unsupervised learning is expected to work well for a large pool of downstream tasks. On the other hand, if we train a supervised model for a specific task, i.e., classification, we cannot expect better performances if the downstream task is not classification.

### Use case 2 — term autocompletion

We first check if the term that is currently being inserted (i.e., before a space button is pressed) is a known term. If not, we look for similar terms in our vocabulary by using the [Gestalt Pattern Matching](https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching) algorithm. Differently from use case 1, the search for similar terms is carried out by comparing the term being inserted and all the vocabulary terms after cutting them off at the length of the input term plus one. The reason is that the term being inserted is assumed to be incomplete and cannot be directly compared to entire vocabulary terms.
<br>
This step will generate several candidates that need to be ranked based on their chance of occurence. Therefore, we check if there is a history of two terms, one term or no term prior to the last inserted term. According to the cases, we employ either a conditional frequency distribution model of word tri-grams or bi-grams, or a TF-IDF uni-gram model. Finally, based on the ranked suggestions, we provide the best term completion suggestion.

### Use case 3 — term autocorrection

We first check if the last inserted term (i.e., after a space button is pressed) is a known term. If not, we look for similar terms in our vocabulary by using the [Gestalt Pattern Matching](https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching) algorithm.
<br>
This step will generate several candidates that need to be ranked based on their chance of occurence. Therefore, we check if there is a history of two terms, one term or no term prior to the last inserted term. According to the cases, we employ either a conditional frequency distribution model of word tri-grams or bi-grams, or a TF-IDF uni-gram model. Finally, based on the ranked suggestions, we provide the best term correction suggestion.

### Use case 4 — term prediction

We consider the last inserted term (i.e., after a space button is pressed) and evaluate the chance of occurence of next term candidates. Therefore, we check if there is a history of one or two terms. According to the cases, we employ either a conditional frequency distribution model of word tri-grams or bi-grams. Finally, based on the ranked suggestions, we provide the best term prediction suggestion.

## Roadmap

See the [open issues](https://github.com/jarvis0/image-search/issues) for a list of proposed features (and known issues).

- [Top Feature Requests](https://github.com/jarvis0/image-search/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/jarvis0/image-search/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/jarvis0/image-search/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

## Support

Reach out to the maintainer at one of the following places:

- [GitHub issues](https://github.com/jarvis0/image-search/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)
- Contact options listed on [this GitHub profile](https://github.com/jarvis0)
- [LinkedIn](https://www.linkedin.com/in/giuseppe-mascellaro-applied-scientist/)

## Project assistance

If you want to say **thank you** or/and support active development of Image Search:

- Add a [GitHub Star](https://github.com/jarvis0/image-search) to the project.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your personal blog.

## Contributing

Please read [our contribution guidelines](docs/CONTRIBUTING.md), and thank you for being involved!

## Authors & contributors

The original setup of this repository is by [Giuseppe Mascellaro](https://github.com/jarvis0).

For a full list of all authors and contributors, see [the contributors page](https://github.com/jarvis0/image-search/contributors).

## Acknowledgements

numpy - see [LICENSE.txt](https://github.com/numpy/numpy/blob/main/LICENSE.txt)

pandas - see [LICENSE.txt](https://github.com/pandas-dev/pandas/blob/main/LICENSE)

matplotlib - see [LICENSE](https://github.com/matplotlib/matplotlib/blob/main/LICENSE/LICENSE)

nltk - see [LICENSE.txt](https://github.com/nltk/nltk/blob/develop/LICENSE.txt)

scikit-learn - see [COPYING](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING)

fastText - see [LICENSE](https://github.com/facebookresearch/fastText/blob/main/LICENSE)

flask - see [LICENSE.rst](https://github.com/pallets/flask/blob/main/LICENSE.rst)

aiohttp - see [LICENSE.txt](https://github.com/aio-libs/aiohttp/blob/master/LICENSE.txt)

pillow - see [LICENSE](https://github.com/python-pillow/Pillow/blob/main/LICENSE)

getch - see [pypi](https://pypi.org/project/getch/)

blessings - see [LICENSE](https://github.com/erikrose/blessings/blob/master/LICENSE)

amazing-github-template - see [LICENSE](https://github.com/dec0dOS/amazing-github-template/blob/main/LICENSE)

Gifski - see [LICENSE](https://github.com/sindresorhus/Gifski/blob/main/license)
