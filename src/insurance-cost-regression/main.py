from pathlib import Path
import torch
from torch import nn
from data import prepare_data
from model import InsuranceNN
from train_utils import validation, train
from tune import run_optuna



def run_training_pipeline(
    csv_path: str = "dataset/insurance.csv",
    model_path: str = "model.pt",
    n_trials: int = 30,
    epochs: int = 50
):
    device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
    print(f"Using {device} device")

    train_loader, val_loader, test_loader, scaler_x, scaler_y = prepare_data(csv_path=csv_path)
    study = run_optuna(
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        n_trials=n_trials,
        epochs=epochs
    )

    print("Best hyperparameters:", study.best_params)

    best = study.best_params
    model = InsuranceNN(best["h1"], best["h2"], best["h3"]).to(device)

    # Adam normalizes Gradients so it moves fixed direction while using
    # momentum to help to coverage to a minimum faster and more stable.
    optimizer = torch.optim.Adam(model.parameters(), lr=best["lr"])
    loss_fn = nn.MSELoss()

    for epoch in range(epochs):
        train(model, train_loader, optimizer, loss_fn, device)
        test_loss = validation(model, test_loader, loss_fn, device)
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {test_loss:.4f}")

    out_path = Path(model_path)

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "best_params": best
        },
        out_path,
    )

    print(f"Saved model {out_path}")
    return str(out_path)


if __name__ == "__main__":
    run_training_pipeline()

