import functools
import optuna
import torch
from torch import nn
from model import InsuranceNN
from train_utils import validation, train


def objective(trial, train_loader, val_loader, device, epochs: int):
    h1 = trial.suggest_int("h1", 16, 128)
    h2 = trial.suggest_int("h2", 16, 128)
    h3 = trial.suggest_int("h3", 16, 128)
    lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)

    model = InsuranceNN(h1=h1, h2=h2, h3=h3).to(device)

    # Adam normalizes Gradients so it moves fixed direction while using
    # momentum to help to coverage to a minimum faster and more stable.
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    for _ in range(epochs):
        train(model, train_loader, optimizer, loss_fn, device)

    return validation(model, val_loader, loss_fn, device)


def run_optuna(train_loader, val_loader, device, n_trials: int = 30, epochs: int = 50):
    objective_with_data = functools.partial(
        objective,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        epochs=epochs,
    )
    study = optuna.create_study(direction="minimize")
    study.optimize(objective_with_data, n_trials=n_trials)
    return study

