# Bloque de Transfer Learning extracto del notebook proporcionado
# Solo funciones (sin clases). Comentarios en español con #.

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
import os

# Detectar dispositivo
def get_device():
    # Devuelve torch.device('cuda') si está disponible, si no 'mps' o 'cpu'
    if torch.cuda.is_available():
        return torch.device('cuda')
    elif torch.backends.mps.is_available():
        return torch.device('mps')
    else:
        return torch.device('cpu')

# Intento de extraer el modelo base desde un objeto que venga de torch.load
def _extract_base_model(obj):
    # Si ya es un nn.Module lo devolvemos
    if isinstance(obj, nn.Module):
        return obj
    # Si es un diccionario buscaremos claves comunes que puedan contener un módulo
    if isinstance(obj, dict):
        for key in ("model", "base_model", "net", "module"):
            candidate = obj.get(key)
            if isinstance(candidate, nn.Module):
                return candidate
    # No encontramos un nn.Module en el checkpoint
    return None

# Dada una arquitectura, intentamos quitar la "cabeza" final y conservar las capas de extracción
def _unwrap_feature_layers(base_model):
    children = list(base_model.children())

    # Algunos modelos vienen envueltos en un único Sequential
    if len(children) == 1 and isinstance(children[0], nn.Sequential):
        children = list(children[0].children())

    # Si hay varias partes, quitamos la última (asumimos que es la cabeza)
    if len(children) > 1:
        return children[:-1]
    return children

# Construye un "mock" como fallback si no hay checkpoint válido
def _build_mock_base(input_size):
    # Devuelve un nn.Sequential simple que actúa como extractor de características
    return nn.Sequential(
        nn.Linear(input_size, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 8),
        nn.ReLU()
    )

# Carga el archivo base (intenta obtener un nn.Module). Si no es posible, devuelve un mock
def load_base_model(path, device, input_size):
    # Devuelve: base_model (nn.Module), base_available (bool)
    try:
        checkpoint = torch.load(path, map_location=device)
        base_model = _extract_base_model(checkpoint)
        if base_model is None:
            # No encontramos un nn.Module dentro del checkpoint
            raise TypeError(
                "model.pt no contiene un nn.Module serializado. Si es solo state_dict(), hace falta la arquitectura original para cargarlo."
            )
        base_model = base_model.to(device)
        base_model.eval()
        return base_model, True
    except (FileNotFoundError, TypeError, AttributeError, KeyError) as e:
        # Mensaje informativo y fallback a mock
        print(f"model.pt no pudo cargarse como modelo completo: {e}")
        print("Usando un modelo simulado como base model.")
        mock = _build_mock_base(input_size).to(device)
        mock.eval()
        return mock, False

# Prepara los componentes del modelo de transfer learning sin usar clases
def prepare_transfer_components(base_model, input_size, device, dropout_p=0.2):
    # Extraer capas reutilizables
    layers = _unwrap_feature_layers(base_model)
    # Construimos un Sequential con las capas de extracción
    feature_extractor = nn.Sequential(*layers)
    feature_extractor.to(device)

    # Congelar parámetros de la base
    for param in feature_extractor.parameters():
        param.requires_grad = False

    # Detectar si la base espera entrada 2D (batch, features) o 4D (images)
    feature_extractor.eval()
    with torch.no_grad():
        dummy = torch.zeros(1, input_size).to(device)
        is_cnn_base = False
        try:
            out = feature_extractor(dummy)
        except Exception:
            # Intentamos reshape que el notebook usó: (1,1,1,input_size)
            try:
                dummy4 = dummy.view(1, 1, 1, input_size)
                out = feature_extractor(dummy4)
                is_cnn_base = True
            except Exception:
                # Como último recurso, intentamos pasar dummy como (1,input_size,1)
                try:
                    dummy3 = dummy.view(1, input_size, 1)
                    out = feature_extractor(dummy3)
                except Exception as e:
                    # Si todo falla, lanzamos para que sea evidente
                    raise RuntimeError("No se pudo determinar la forma de entrada esperada por el extractor de características: " + str(e))

    feat_dim = out.view(1, -1).shape[1]
    print(f"Feature extractor output dimension: {feat_dim}")

    # Construir la nueva cabeza regresora
    regressor = nn.Sequential(
        nn.Linear(feat_dim, 64),
        nn.ReLU(),
        nn.Dropout(p=dropout_p),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 1)
    ).to(device)

    return feature_extractor, regressor, is_cnn_base, feat_dim

# Contadores de parámetros
def count_parameters(feature_extractor, regressor):
    total = sum(p.numel() for p in list(feature_extractor.parameters()) + list(regressor.parameters()))
    frozen = sum(p.numel() for p in feature_extractor.parameters() if not p.requires_grad)
    trainable = total - frozen
    return total, frozen, trainable

# Funciones de entrenamiento que trabajan con los componentes

def train_epoch_components(feature_extractor, regressor, loader, optimizer, loss_fn, device, is_cnn_base, input_size):
    # feature_extractor está en modo eval y congelado
    regressor.train()
    total_loss = 0.0
    for X_batch, y_batch in loader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)

        # Ajustar forma si la base es CNN
        if is_cnn_base:
            X_in = X_batch.view(X_batch.size(0), 1, 1, input_size)
        else:
            X_in = X_batch

        with torch.no_grad():
            feats = feature_extractor(X_in)
        feats = feats.view(feats.size(0), -1)

        optimizer.zero_grad()
        preds = regressor(feats).view(-1)
        loss = loss_fn(preds, y_batch.view(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

@torch.no_grad()
def evaluate_components(feature_extractor, regressor, loader, loss_fn, device, is_cnn_base, input_size):
    regressor.eval()
    total_loss = 0.0
    for X_batch, y_batch in loader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)
        if is_cnn_base:
            X_in = X_batch.view(X_batch.size(0), 1, 1, input_size)
        else:
            X_in = X_batch
        feats = feature_extractor(X_in)
        feats = feats.view(feats.size(0), -1)
        preds = regressor(feats).view(-1)
        total_loss += loss_fn(preds, y_batch.view(-1)).item()
    return total_loss / len(loader)

# Entrenamiento completo con early stopping para los componentes
def train_model_components(feature_extractor, regressor, train_loader, val_loader,
                           device, input_size, epochs=100, lr=1e-3, label="Transfer Model"):
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, regressor.parameters()), lr=lr, weight_decay=1e-4)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10)

    history = {"train_loss": [], "val_loss": []}

    best_val_loss = float('inf')
    best_state = None
    patience = 20
    patience_cnt = 0

    # Detectar si la base es CNN (ya debería estar definido por quien preparó los componentes)
    # Para mayor robustez, intentamos deducirlo: comprobamos si feature_extractor acepta (1,input_size)
    with torch.no_grad():
        try:
            _ = feature_extractor(torch.zeros(1, input_size).to(device))
            is_cnn_base = False
        except Exception:
            try:
                _ = feature_extractor(torch.zeros(1, 1, 1, input_size).to(device))
                is_cnn_base = True
            except Exception:
                is_cnn_base = False

    print(f"\n{'='*55}")
    print(f"  Training: {label}")
    print(f"{'='*55}\n")

    for epoch in range(1, epochs + 1):
        tr_loss = train_epoch_components(feature_extractor, regressor, train_loader, optimizer, loss_fn, device, is_cnn_base, input_size)
        val_loss = evaluate_components(feature_extractor, regressor, val_loader, loss_fn, device, is_cnn_base, input_size)
        scheduler.step(val_loss)

        history["train_loss"].append(tr_loss)
        history["val_loss"].append(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.clone() for k, v in regressor.state_dict().items()}
            patience_cnt = 0
        else:
            patience_cnt += 1

        if epoch % 10 == 0:
            print(f"  Epoch {epoch:3d}/{epochs}  │  Train MSE: {tr_loss:.4f}  │  Val MSE: {val_loss:.4f}")

        if patience_cnt >= patience:
            print(f"\n  Early stopping at epoch {epoch} (best val: {best_val_loss:.4f})")
            break

    # Restaurar mejor estado en la cabeza regresora
    if best_state is not None:
        regressor.load_state_dict(best_state)
    print(f"\n  Best val MSE: {best_val_loss:.4f}")
    return history

# Predicciones y des-normalización si es necesario (la normalización la debe manejar quien use estas funciones)
@torch.no_grad()
def get_predictions_components(feature_extractor, regressor, loader, device, input_size, scaler_y=None):
    feature_extractor.eval()
    regressor.eval()
    preds_list = []
    reals_list = []
    with torch.no_grad():
        for X_batch, y_batch in loader:
            X_batch = X_batch.to(device)
            if feature_extractor is None:
                raise RuntimeError("feature_extractor no puede ser None")
            # Detección simple de forma de entrada
            try:
                feats = feature_extractor(X_batch)
            except Exception:
                feats = feature_extractor(X_batch.view(X_batch.size(0), 1, 1, input_size))
            feats = feats.view(feats.size(0), -1)
            out = regressor(feats).view(-1).cpu()
            preds_list.append(out)
            reals_list.append(y_batch.view(-1))

    preds = torch.cat(preds_list).numpy()
    reals = torch.cat(reals_list).numpy()
    if scaler_y is not None:
        # Escalar de nuevo a la escala original
        try:
            preds = scaler_y.inverse_transform(preds.reshape(-1, 1)).flatten()
            reals = scaler_y.inverse_transform(reals.reshape(-1, 1)).flatten()
        except Exception:
            pass
    return preds, reals

# Funciones de guardado/recuperación mínimas para la cabeza
def save_transfer_head(regressor, path):
    # Guarda solo los pesos de la cabeza regresora
    torch.save(regressor.state_dict(), path)

def load_transfer_head(regressor, path, device):
    state = torch.load(path, map_location=device)
    regressor.load_state_dict(state)
    regressor.to(device)
    return regressor

# Función utilitaria para mostrar resumen
def print_transfer_summary(feature_extractor, regressor):
    total, frozen, trainable = count_parameters(feature_extractor, regressor)
    print("Transfer Model parameter summary:")
    print(f"  Total params    : {total:,}")
    print(f"  Frozen (base)   : {frozen:,}")
    print(f"  Trainable (head): {trainable:,}")


# Ejemplo mínimo de contrato (no se ejecuta automáticamente)
# - Se espera que el usuario provea DataLoaders que retornen (features_tensor, target_tensor)
# - Input_size debe coincidir con la dimensión de features en cada batch
# - scaler_y es opcional y se usa solo para des-normalizar predicciones

# Fin del bloque de transferencia

