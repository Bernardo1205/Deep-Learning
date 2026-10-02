# Deep Learning Portfolio

Practical deep-learning projects developed with Python and PyTorch. The repository covers regression, computer vision, and natural-language processing, with training pipelines, hyperparameter optimization, evaluation code, and experiment notebooks.

## Projects

### Insurance Cost Neural Network

`src/insurance-cost-NN`

Neural-network regression for predicting insurance costs from structured data. The project includes preprocessing, model training, validation, Optuna-based hyperparameter tuning, and model evaluation.

### Image Classification

`src/image-classification`

Computer-vision experiments for classifying astronomical images. It includes a CNN training pipeline, data augmentation and transformations, Optuna optimization, evaluation utilities, and a separate transfer-learning workflow.

### Sentiment Analysis with RNNs

`src/sentiment-analysis-multimodel`

Text classification for tweet sentiment using and comparing vanilla RNN, GRU, and LSTM architectures. The project includes text cleaning, vocabulary construction, sequence encoding, focal loss, training, and evaluation.

### Single-Model Tweet Sentiment Analysis

`src/tweet-sentiment-analysis-single-model`

An LSTM-based sentiment-analysis workflow applied to historical Twitter data, including dataset exploration, experiment tracking, and a trained model notebook.

## Repository Structure

```text
src/
├── insurance-cost-NN/
├── image-classification/
├── sentiment-analysis-multimodel/
└── tweet-sentiment-analysis-single-model/
```

Each project keeps its implementation, datasets, notebooks, and documentation together. Trained model checkpoints, Optuna databases, experiment logs, and Python cache files are local artifacts and are excluded from version control.

## Setup

This project requires Python 3.10 or newer. From the repository root, install the dependencies with:

```bash
pip install -e .
```

Alternatively, if you use `uv`:

```bash
uv sync
```

## Running the Projects

Because the training scripts use project-relative dataset paths, run each script from its project directory. For example:

```bash
cd src/insurance-cost-NN
python main.py
```

The CNN and sentiment-analysis projects also provide notebooks for exploring the data, training models, and reviewing results.

## Technologies

- Python 3.10+
- PyTorch and TorchVision
- NumPy and Pandas
- Scikit-learn
- Matplotlib
- Optuna
- Jupyter
