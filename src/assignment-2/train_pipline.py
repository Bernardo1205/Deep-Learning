from xgboost.callback import EarlyStopping

from optuna_tuning import run_optimization
from constants import EPOCHS , DATASET_DIR , NUM_CLASSES , DEVICE
from models import AlexNet
from data import data_loader
from transforms import get_transform
from train_utils import train, validation, compute_accuracy
from evaluation import run_evaluation
from utils import save_checkpoint, print_model_summary
import torch

def main():

    study = run_optimization()

    best_params = study.best_params

    # Extract best hyperparameters
    batch_size = best_params["batch_size"]
    lr = best_params["lr"]
    optimizer_name = best_params["optimizer"]
    momentum = best_params["momentum"]
    weight_decay = best_params["weight_decay"]

    # Create DataLoaders with best transformations
    transform = get_transform(best_params)

    train_loader = data_loader(
        DATASET_DIR / "training",
        batch_size=batch_size,
        transform=transform
    )

    val_loader = data_loader(
        DATASET_DIR / "validation",
        batch_size=batch_size,
        transform=transform
    )

    # Create model
    model = AlexNet(num_classes=NUM_CLASSES)
    print_model_summary(model)
    model.to(DEVICE)

    # Create optimizer
    if optimizer_name == "Adam":
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=lr,
            weight_decay=weight_decay
        )

    else:
        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=lr,
            momentum=momentum,
            weight_decay=weight_decay
        )

    # Loss function
    loss_fn = torch.nn.CrossEntropyLoss()
    early_stopping = False

    #Training Process
    for epoch in range(EPOCHS):
        # Train
        train(model, train_loader, optimizer, loss_fn, DEVICE)

        # Validate
        val_loss = validation(model, val_loader, loss_fn, DEVICE)

        # Compute accuracy
        train_acc = compute_accuracy(model, train_loader, DEVICE)
        val_acc = compute_accuracy(model, val_loader, DEVICE)

        print(f"Epoch {epoch+1}/{EPOCHS} - Train Loss: {val_loss:.6f}, Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")
        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            early_stopping = True
            # Save best model
            save_checkpoint(model, best_params, checkpoint_path="model.pt")

    print(f"\nTraining completed!")

    if not early_stopping:
        save_checkpoint(model, best_params, checkpoint_path="model.pt")



    # Load test dataset
    inference_transform = get_transform(best_params)
    test_loader = data_loader(DATASET_DIR / "test",
                              transform=inference_transform ,
                              batch_size=batch_size)

    test_acc = compute_accuracy(model, test_loader, DEVICE)
    print(f"Test Accuracy: {test_acc:.4f}")

    # Show random evaluations
    print(f"Random test predictions:")
    run_evaluation("model.pt", num_examples=5, device=DEVICE)


if __name__ == "__main__":
    main()