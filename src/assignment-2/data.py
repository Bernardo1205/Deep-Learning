"""
Data loading and preprocessing utilities
"""
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from constants import DATASET_DIR


def data_loader(data_path, batch_size, transform):
    """
    Create a DataLoader from an ImageFolder dataset.
    
    Args:
        data_path: Path to dataset directory with class subdirectories
        batch_size: Number of samples per batch
        transform: torchvision.transforms.Compose object for preprocessing
    
    Returns:
        torch.utils.data.DataLoader with shuffled data
    """
    
    # Load dataset using ImageFolder
    # ImageFolder automatically creates class labels from subdirectory names
    dataset = ImageFolder(DATASET_DIR / data_path, transform=transform)
    
    # Create DataLoader
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )
    return dataloader



