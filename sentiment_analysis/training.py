import torch
import numpy as np
from config import DEVICE

# Entrenar por una época
def train_epoch(model, iterator, optimizer, criterion, device):
    model.train()
    epoch_loss = 0
    epoch_acc = 0
    for batch_idx, (text, labels) in enumerate(iterator):
        text = text.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        predictions = model(text)
        loss = criterion(predictions, labels)
        acc = (predictions.argmax(1) == labels).float().mean()
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
        epoch_acc += acc.item()
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

# Evaluar modelo
def evaluate(model, iterator, criterion, device):
    model.eval()
    epoch_loss = 0
    epoch_acc = 0
    with torch.no_grad():
        for text, labels in iterator:
            text = text.to(device)
            labels = labels.to(device)
            predictions = model(text)
            loss = criterion(predictions, labels)
            acc = (predictions.argmax(1) == labels).float().mean()
            epoch_loss += loss.item()
            epoch_acc += acc.item()
    return epoch_loss / len(iterator), epoch_acc / len(iterator)

# Entrenar modelo completo con early stopping
def train_model(model, train_iterator, val_iterator, optimizer, criterion, epochs, model_name, device, save_dir="models/"):
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    best_val_acc = 0
    for epoch in range(epochs):
        train_loss, train_acc = train_epoch(model, train_iterator, optimizer, criterion, device)
        val_loss, val_acc = evaluate(model, val_iterator, criterion, device)
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), f'{save_dir}best_{model_name}.pt')
    return history

# Obtener predicciones
def get_predictions(model, iterator, device):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for text, labels in iterator:
            text = text.to(device)
            predictions = model(text)
            preds = predictions.argmax(1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.numpy())
    return np.array(all_preds), np.array(all_labels)

# Predicción en un texto nuevo
def predict_sentiment(text, model, vocab, device, classes, clean_func, text_to_seq_func):
    model.eval()
    cleaned_text = clean_func(text)
    sequence = torch.tensor(text_to_seq_func(cleaned_text, vocab), dtype=torch.long).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(sequence)
        pred = output.argmax(1).item()
    return classes[pred]

