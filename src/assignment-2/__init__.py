"""
Assignment 2: CNN Image Classification with Hyperparameter Tuning

Main modules:
- models: AlexNet CNN architecture
- transforms: Image transformations and augmentations
- data: Data loading utilities
- train_utils: Training and validation functions
- evaluation: Model evaluation utilities
- optuna_tuning: Hyperparameter optimization
- constants: Configuration constants
"""

from .models import AlexNet
from .transforms import get_transform, get_inference_transform
from .data import data_loader, get_dataset, get_class_mapping
from .train_utils import train, validation, compute_accuracy
from .evaluation import run_evaluation, predict_single, batch_predict
from .optuna_tuning import objective, create_study, run_optimization, get_best_params_summary
from .constants import DATASET_DIR, NUM_CLASSES, DEFAULT_IMAGE_SIZE, DEVICE

__all__ = [
    "AlexNet",
    "get_transform",
    "get_inference_transform",
    "data_loader",
    "get_dataset",
    "get_class_mapping",
    "train",
    "validation",
    "compute_accuracy",
    "run_evaluation",
    "predict_single",
    "batch_predict",
    "objective",
    "create_study",
    "run_optimization",
    "get_best_params_summary",
    "DATASET_DIR",
    "NUM_CLASSES",
    "DEFAULT_IMAGE_SIZE",
    "DEVICE",
]

