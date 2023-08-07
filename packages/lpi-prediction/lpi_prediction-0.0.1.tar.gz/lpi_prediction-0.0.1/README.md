# LPI-Prediction: A template library to build lncRNA-protein interaction prediction algorithms
[![Python](https://img.shields.io/pypi/pyversions/lpi_prediction.svg?style=plastic)](https://badge.fury.io/py/lpi_prediction)
[![PyPI version](https://badge.fury.io/py/lpi_prediction.svg)](https://badge.fury.io/py/lpi_prediction)

LPI-Prediction aims to be a simple and easy-to-use template library to develop lncRNA-protein interaction prediction algorithms, or any prediction algorithm in general. LPI-Prediction provides a set of abstractions to load and process data, and a set of abstractions to train, evaluate, and execute the interaction prediction algorithms. LPI-Prediction is designed to be easily extensible, and to greatly lower the cost of developing production-level lnRNA-protein interaction prediction algorithms.

## Installation
LPI-Prediction is available on PyPI, and can be installed using pip as follows:
```bash
user@host$ python3 -m pip install lpi-prediction
```
Please note that LPI-Prediction requires Python3.7 or higher.

## Examples
LPI-Prediction provides a set of examples to demonstrate how to use the library. The examples are available in the `examples` directory of the repository. The examples are:
* `knn.py`: A simple example that shows how to load and process data, and how to train and evaluate a K-Nearest Neighbors (KNN) prediction algorithm.
* `svm.py`: A simple example that shows how to load and process data, and how to train and evaluate a Support Vector Machine (SVM) prediction algorithm.
* `ensemble.py`: A simple example that shows how to load and process data, and how to train and evaluate an ensemble of prediction algorithms (KNN + SVM).

Moreover, [MIRLO](https://github.com/UDC-GAC/MIRLO) shows how to use LPI-Prediction to develop a production-level lncRNA-protein interaction prediction algorithm
that does automatic hyperparameter tuning, and uses third party applications (Rscript) to extract features from the lncRNA and protein sequences.

## License
LPI-Prediction is licensed under the MIT License. See the `LICENSE` file for more information.

## Authors
LPI-Prediction was developed by [Iñaki Amatria-Barral](https://amatria.dev/).
