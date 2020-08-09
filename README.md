<!-- Add banner here -->

# RecKit

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ZhongchuanSun/reckit?include_prereleases)
![PyPI](https://img.shields.io/pypi/v/reckit)
![Travis (.com)](https://img.shields.io/travis/com/ZhongchuanSun/reckit?label=Travis%20CI&logo=Travis)
![AppVeyor](https://img.shields.io/appveyor/build/ZhongchuanSun/reckit?label=AppVeyor&logo=AppVeyor)

<!-- Describe your project in brief -->
RecKit is a collection of recommender utility codes.

# Feature

- Parse arguments from command line and ini-style files
- Diverse data preprocessing
- Fast negative sampling
- Fast model evaluating
- Convenient records logging
- Flexible batch data iterator

# Installation

## Installation from binary

Binary installers are available at the [Python package index](https://pypi.org/project/reckit/)

```sh
# PyPI
pip install reckit
```

## Build from sources

To install reckit from source you need Cython:

```sh
pip install cython
```

In the reckit directory, execute:

```sh
python setup.py bdist_wheel
```

Then, you can find a `*.whl` file in `./dist/`, and install it:

```sh
pip install ./dist/*.whl
```

# Usage

You can find examples in [NeuRec](https://github.com/wubinzzu/NeuRec/tree/v3.x).
