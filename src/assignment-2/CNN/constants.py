"""
Constants and configuration for the CNN project
"""
from pathlib import Path

# Dataset configuration
DATASET_DIR = Path("CNN/dataset")
NUM_CLASSES = 12

# Training configuration
EPOCHS = 50
DEFAULT_N_TRIALS = 100

STORAGE_DIR = "db/optuna_study4.db"
# Device
DEVICE = "cuda" if __import__("torch").cuda.is_available() else "cpu"

