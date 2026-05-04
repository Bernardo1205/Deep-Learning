"""
Optuna hyperparameter tuning utilities
"""

import torch
from torch import nn
from torchvision import transforms
from data import data_loader
from models import AlexNet
from train_utils import train, validation
from constants import DATASET_DIR , EPOCHS , DEVICE , STORAGE_DIR
import optuna

def objective(trial):
    loss_fn = nn.CrossEntropyLoss()
    model = AlexNet()

    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64, 128, 256])

    # Hyperparameters to image transformation
    #Image size
    image_size = trial.suggest_categorical("image_size", [224 , 299])

    # Rotation degrees
    rot_degrees = trial.suggest_int("rot_degrees", 0, 360)

    #Probability to flip horizontally
    h_flip = trial.suggest_int("h_flip", 0, 1)

    #Brightness ( 1.0 is the original )
    brightness = trial.suggest_int("brightness", 0.8, 1.2)

    #Randndom crop ( how much are we willing to crop the image randomly )
    crop_scale = trial.suggest_int("crop_scale", 0.7, 1)

    #Find the best normalization transformation
    norm_strategy = trial.suggest_categorical("norm_strategy", ["imagenet", "custom", "simple"])

    if norm_strategy == "imagenet":
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
    elif norm_strategy == "custom":
        # Optuna search for you mean values and std for our data
        m = trial.suggest_float("m_custom", 0.0, 1.0)
        s = trial.suggest_float("s_custom", 0.1, 0.5)
        mean, std = [m, m, m], [s, s, s]
    else: # "simple" [0, 1]
        mean, std = [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]

    transform = transforms.Compose([
        transforms.RandomRotation(degrees=rot_degrees),
        transforms.RandomResizedCrop(size=(image_size,image_size),scale=(crop_scale,crop_scale,1)),
        transforms.RandomHorizontalFlip(p=h_flip),
        transforms.ColorJitter(brightness=brightness),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

    train_loder = data_loader(DATASET_DIR / "training", batch_size=batch_size, transform=transform)
    validation_loader = data_loader(DATASET_DIR / "validation", batch_size=batch_size, transform=transform)

    #Generate the best Optimizer
    #Suggest best lr
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)

    #Get optimizer name
    optimizer = trial.suggest_categorical("optimizer", ["Adam", "SGD"])

    momentum = trial.suggest_float("momentum", 0.8, 1)

    #Penalizes large weights , prevents overfitting
    weight_decay = trial.suggest_float("weight_decay", 1e-5, 1e-1, log=True)

    if optimizer == "Adam":
        scaling = trial.suggest_float("scaling", 0.9, 1)
        optimizer = torch.optim.Adam(
            params= model.parameters(),
            betas=(momentum,scaling),
            lr=lr,
            weight_decay=weight_decay,
        )
    else:
        optimizer = torch.optim.SGD(
            params=model.parameters(),
            momentum= momentum,
            lr=lr,
            weight_decay=weight_decay)

    for _ in range(EPOCHS):
        train(model, train_loder, optimizer, loss_fn, DEVICE)

    return validation(model,validation_loader,loss_fn, DEVICE)

def run_optimization():
    study = optuna.create_study(
        study_name="study7",
        storage=STORAGE_DIR,
        direction="maximize",
        load_if_exists=True
    )
    study.optimize(objective, n_trials=100)

    return study