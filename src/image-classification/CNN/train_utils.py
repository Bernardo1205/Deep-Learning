"""
Training and validation utilities
"""
import torch


def train(model, train_loader, optimizer, loss_fn, device):
    """
    Train the model for one epoch.

    Args:
        model: PyTorch model to train
        train_loader: DataLoader with training data
        optimizer: Optimizer (e.g., Adam, SGD)
        loss_fn: Loss function
        device: Device to run on (cuda or cpu)
    """
    model.train()

    for data, target in train_loader:
        # Move data to the specified device (GPU or CPU)
        data, target = data.to(device), target.to(device)

        # Zero the gradients from the previous iteration
        # This prevents gradients from accumulating across batches
        optimizer.zero_grad()

        # Forward pass: model output has shape [batch_size, num_classes]
        # target has shape [batch_size]
        prediction = model(data)

        # Compute the loss (CrossEntropyLoss for classification)
        loss = loss_fn(prediction, target)

        # Backward pass: compute gradients
        loss.backward()

        # Update weights using computed gradients
        optimizer.step()


def validation(model, val_loader, loss_fn, device):
    """
    Evaluate model performance on validation set.

    Args:
        model: PyTorch model to evaluate
        val_loader: DataLoader with validation data
        loss_fn: Loss function
        device: Device to run on (cuda or cpu)

    Returns:
        float: Average validation loss
    """
    model.eval()
    total_loss = 0.0

    with torch.no_grad():
        for data, target in val_loader:
            # Move data to device
            data, target = data.to(device), target.to(device)

            # Forward pass
            prediction = model(data)

            # Compute loss
            loss = loss_fn(prediction, target)
            total_loss += loss.item()

    # Return average loss across all batches
    avg_loss = total_loss / len(val_loader)
    return avg_loss


def compute_accuracy(model, data_loader, device):
    """
    Compute classification accuracy on a dataset.

    Args:
        model: PyTorch model to evaluate
        data_loader: DataLoader with data
        device: Device to run on (cuda or cpu)

    Returns:
        float: Accuracy (0.0 to 1.0)
    """
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)

            # Forward pass
            output = model(data)

            # Get predictions
            predictions = torch.argmax(output, dim=1)

            # Count correct predictions
            correct += (predictions == target).sum().item()
            total += target.size(0)

    accuracy = correct / total if total > 0 else 0.0
    return accuracy

