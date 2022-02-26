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
  <br />
  <a href="https://github.com/jarvis0/image-search/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/jarvis0/image-search/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/jarvis0/image-search/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br />

[![Project license](https://img.shields.io/github/license/jarvis0/image-search.svg?style=flat-square)](LICENSE)

[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/jarvis0/image-search/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
[![code with love by jarvis0](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-jarvis0-ff1414.svg?style=flat-square)](https://github.com/jarvis0)

</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Support](#support)
- [Project assistance](#project-assistance)
- [Contributing](#contributing)
- [Authors & contributors](#authors--contributors)
- [Acknowledgements](#acknowledgements)

</details>

---

## About

This project is a software application for searching and displaying images from a database of ~20M images gathered on the Internet. The images can be searched through an input text that specifies a caption or a description of the desired images. For a faster retrieval, the user is intelligently assisted while typing.

The application can be accessed in two ways. One is a Command Line Interface (CLI) application, the other is a Web application accessible from common browsers. As soon as the user types, several typing suggestions are generated and proposed:
- a list of complete image captions that are compatible with the text inserted so far;
- a term completion compatible with the current term being inserted;
- a term correction if applicable;
- a prediciton of the next term.

<details>
<summary>Demos</summary>
<br>
|                               Home Page                               |                               Login Page                               |
| :-------------------------------------------------------------------: | :--------------------------------------------------------------------: |
| <img src="docs/images/screenshot.png" title="Home Page" width="100%"> | <img src="docs/images/screenshot.png" title="Login Page" width="100%"> |

</details>

## Getting Started

### Prerequisites
This application relies on fastText. `fastText` builds on modern Mac OS and Linux distributions. Since it uses some C++11 features, it requires a compiler with good C++11 support. These include:
- (g++-4.7.2 or newer) or (clang-3.3 or newer)

Compilation is carried out using a Makefile, so you will need to have a working make. If you want to use cmake you need at least version 2.8.9. For further information, refer [here](https://github.com/facebookresearch/fastText/tree/master).

The code has been developed using Python v3.8.11. Therefore, you will need at least Python v3.8.11 and Anaconda v4.10.1.

All the other requirements are included in the application setup.

### Installation
We use a makefile and some scripts to simplify the installation procedure.
```
$ git clone https://github.com/jarvis0/image-search.git
$ cd image-search
$ make conda
$ make requirements
$ make install
```
At this point you will need to download the database containing the image descriptions and their corresponding URLs. You can find the file at this [link](https://storage.cloud.google.com/conceptual-captions-v1-1-labels/Image_Labels_Subset_Train_GCC-Labels-training.tsv?_ga=2.234395421.-20118413.1607637118), provided that you are logged in using a valid Google account. Once the file is downloaded, we suggest to move it under the folder `data` and to rename it to `raw.tsv`.



## Usage

> **[?]**
> How does one go about using it?
> Provide various use cases and code examples here.

## Roadmap

See the [open issues](https://github.com/jarvis0/image-search/issues) for a list of proposed features (and known issues).

- [Top Feature Requests](https://github.com/jarvis0/image-search/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/jarvis0/image-search/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/jarvis0/image-search/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

## Support

> **[?]**
> Provide additional ways to contact the project maintainer/maintainers.

Reach out to the maintainer at one of the following places:

- [GitHub issues](https://github.com/jarvis0/image-search/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)
- Contact options listed on [this GitHub profile](https://github.com/jarvis0)

## Project assistance

If you want to say **thank you** or/and support active development of Image Search:

- Add a [GitHub Star](https://github.com/jarvis0/image-search) to the project.
- Tweet about the Image Search.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your personal blog.

Together, we can make Image Search **better**!

## Contributing



Please read [our contribution guidelines](docs/CONTRIBUTING.md), and thank you for being involved!

## Authors & contributors

The original setup of this repository is by [Giuseppe Mascellaro](https://github.com/jarvis0).

For a full list of all authors and contributors, see [the contributors page](https://github.com/jarvis0/image-search/contributors).



## Acknowledgements

> **[?]**
> If your work was funded by any organization or institution, acknowledge their support here.
> In addition, if your work relies on other software libraries, or was inspired by looking at other work, it is appropriate to acknowledge this intellectual debt too.
