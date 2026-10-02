"""
Utility functions for model saving, loading, and checkpointing
"""
import torch
from models import AlexNet
from constants import NUM_CLASSES , DEVICE


def save_checkpoint(model, best_params, checkpoint_path="model.pt"):
    """
    Save model and hyperparameters to a checkpoint.

    Args:
        model: PyTorch model
        best_params: Dict with best hyperparameters
        checkpoint_path: Path to save checkpoint
    """
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "best_params": best_params,
    }

    torch.save(checkpoint, checkpoint_path)
    print(f"Checkpoint saved to {checkpoint_path}")


def load_checkpoint(checkpoint_path):
    """
    Load model and hyperparameters from a checkpoint.

    Args:
        checkpoint_path: Path to checkpoint file
        device: Device to load model on (if None, uses cpu)

    Returns:
        tuple: (model, best_params)
    """

    checkpoint = torch.load(checkpoint_path, map_location=DEVICE)

    # Recreate model
    model = AlexNet(num_classes=NUM_CLASSES)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(DEVICE)

    best_params = checkpoint["best_params"]

    return model, best_params


def print_model_summary(model):
    """
    Print model architecture summary.

    Args:
        model: PyTorch model
    """
    print("MODEL ARCHITECTURE")

    print(model)

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    print(f"\nTotal parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    print(f"{'='*60}\n")

