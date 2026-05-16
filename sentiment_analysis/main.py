import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import precision_score, recall_score, f1_score
from torch.utils.data import DataLoader
from imblearn.over_sampling import SMOTE
import optuna
import warnings

warnings.filterwarnings('ignore')

# Importar módulos propios
from config import (
    DEVICE, MIN_WORD_FREQ, MAX_SEQ_LENGTH, EMBEDDING_DIM, HIDDEN_DIM,
    NUM_LAYERS, DROPOUT, LEARNING_RATE, BATCH_SIZE, EPOCHS,
    N_TRIALS, OPTUNA_EPOCHS, FOCAL_LOSS_GAMMA, DATASET_PATH, OPTUNA_DB_PATH
)
from preprocessing import clean_text, build_vocab, text_to_sequence
from models import RNNClassifier, GRUClassifier, LSTMClassifier
from loss import FocalLoss
from training import train_epoch, evaluate, train_model, get_predictions, predict_sentiment
from dataset import TwitterDataset

# ════════════════════════════════════════════════════════════════════════════════
# 1. Cargar y preparar datos
# ════════════════════════════════════════════════════════════════════════════════
print("Cargando dataset...")
df = pd.read_csv("dataset/Tweets.csv")

# Filtrar valores nulos
df = df[df['airline_sentiment'].notna()].copy()
df = df[df['text'].notna()].copy()

# Codificar etiquetas
le = LabelEncoder()
df['sentiment_encoded'] = le.fit_transform(df['airline_sentiment'])
classes = le.classes_
num_classes = len(classes)

# Limpiar textos
df['text_cleaned'] = df['text'].apply(clean_text)

# Construir vocabulario
vocab = build_vocab(df['text_cleaned'], min_freq=MIN_WORD_FREQ)
vocab_size = len(vocab)

print(f"Total de tweets: {len(df)}")
print(f"Clases: {df['airline_sentiment'].value_counts().to_dict()}")
print(f"Tamaño del vocabulario: {vocab_size}")

# ════════════════════════════════════════════════════════════════════════════════
# 2. Dividir datos
# ════════════════════════════════════════════════════════════════════════════════
X_train, X_temp, y_train, y_temp = train_test_split(
    df['text_cleaned'].values,
    df['sentiment_encoded'].values,
    test_size=0.3,
    random_state=42,
    stratify=df['sentiment_encoded'].values
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.5,
    random_state=42,
    stratify=y_temp
)

# Convertir a secuencias
X_train_seq = np.array([text_to_sequence(t, vocab) for t in X_train])

# SMOTE para balanceo
sm = SMOTE(random_state=42)
X_train_seq, y_train = sm.fit_resample(X_train_seq, y_train)

# Crear datasets
train_dataset = TwitterDataset(X_train_seq, y_train, vocab, already_encoded=True)
val_dataset = TwitterDataset(X_val, y_val, vocab)
test_dataset = TwitterDataset(X_test, y_test, vocab)

print(f"\nDatos de entrenamiento después de SMOTE: {len(train_dataset)}")
print(f"Datos de validación: {len(val_dataset)}")
print(f"Datos de test: {len(test_dataset)}")

# ════════════════════════════════════════════════════════════════════════════════
# 3. Calcular pesos de clases
# ════════════════════════════════════════════════════════════════════════════════
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights = torch.tensor(class_weights, dtype=torch.float32).to(DEVICE)

criterion = FocalLoss(alpha=class_weights, gamma=FOCAL_LOSS_GAMMA)
print(f"Pesos de clases: {dict(zip(classes, class_weights.cpu().numpy()))}")

# ════════════════════════════════════════════════════════════════════════════════
# 4. Optuna: Búsqueda de hiperparámetros
# ════════════════════════════════════════════════════════════════════════════════
def objective(trial):
    arch = trial.suggest_categorical("architecture", ["RNN", "GRU", "LSTM"])
    emb_dim = trial.suggest_categorical("embedding_dim", [64, 128, 256])
    hid_dim = trial.suggest_categorical("hidden_dim", [64, 128, 256])
    n_layers = trial.suggest_int("num_layers", 1, 3)
    dropout = trial.suggest_float("dropout", 0.1, 0.5)
    lr = trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True)
    bs = trial.suggest_categorical("batch_size", [64, 128])

    cls_map = {"RNN": RNNClassifier, "GRU": GRUClassifier, "LSTM": LSTMClassifier}
    model = cls_map[arch](vocab_size, emb_dim, hid_dim, num_classes, n_layers, dropout).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=lr)

    train_loader = DataLoader(train_dataset, batch_size=bs, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=bs, shuffle=False)

    best_val_acc = 0.0
    for epoch in range(OPTUNA_EPOCHS):
        train_epoch(model, train_loader, optimizer, criterion, DEVICE)
        _, val_acc = evaluate(model, val_loader, criterion, DEVICE)
        best_val_acc = max(best_val_acc, val_acc)
        trial.report(val_acc, epoch)
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return best_val_acc

# Ejecutar Optuna
print("\n" + "="*80)
print("Iniciando búsqueda de hiperparámetros con Optuna...")
print("="*80)

study = optuna.create_study(
    direction="maximize",
    storage=OPTUNA_DB_PATH,
    study_name="sentiment",
    load_if_exists=True,
    pruner=optuna.pruners.MedianPruner()
)
study.optimize(objective, n_trials=N_TRIALS, show_progress_bar=True)

best_trial = study.best_trial
print(f"\nMejor val_accuracy: {best_trial.value}")
print(f"Mejores hiperparámetros: {best_trial.params}")

# ════════════════════════════════════════════════════════════════════════════════
# 5. Entrenar modelos con mejores hiperparámetros
# ════════════════════════════════════════════════════════════════════════════════
best_params = best_trial.params

# DataLoaders finales
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

results = {}
models = {}

print("\n" + "="*80)
print("Entrenando modelos con mejores hiperparámetros...")
print("="*80)

# RNN
print("\nEntrenando RNN...")
model_rnn = RNNClassifier(vocab_size, best_params['embedding_dim'], best_params['hidden_dim'],
                          num_classes, best_params['num_layers'], best_params['dropout']).to(DEVICE)
optimizer_rnn = optim.Adam(model_rnn.parameters(), lr=best_params['learning_rate'])
history_rnn = train_model(model_rnn, train_loader, val_loader, optimizer_rnn, criterion, EPOCHS, 'RNN', DEVICE)
results['RNN'] = history_rnn
models['RNN'] = model_rnn

# GRU
print("Entrenando GRU...")
model_gru = GRUClassifier(vocab_size, best_params['embedding_dim'], best_params['hidden_dim'],
                          num_classes, best_params['num_layers'], best_params['dropout']).to(DEVICE)
optimizer_gru = optim.Adam(model_gru.parameters(), lr=best_params['learning_rate'])
history_gru = train_model(model_gru, train_loader, val_loader, optimizer_gru, criterion, EPOCHS, 'GRU', DEVICE)
results['GRU'] = history_gru
models['GRU'] = model_gru

# LSTM
print("Entrenando LSTM...")
model_lstm = LSTMClassifier(vocab_size, best_params['embedding_dim'], best_params['hidden_dim'],
                            num_classes, best_params['num_layers'], best_params['dropout']).to(DEVICE)
optimizer_lstm = optim.Adam(model_lstm.parameters(), lr=best_params['learning_rate'])
history_lstm = train_model(model_lstm, train_loader, val_loader, optimizer_lstm, criterion, EPOCHS, 'LSTM', DEVICE)
results['LSTM'] = history_lstm
models['LSTM'] = model_lstm

# ════════════════════════════════════════════════════════════════════════════════
# 6. Evaluación en test
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("Evaluando modelos en conjunto de test...")
print("="*80)

test_results = {}

for model_name, model in models.items():
    model.load_state_dict(torch.load(f'models/best_{model_name}.pt'))
    preds, labels = get_predictions(model, test_loader, DEVICE)

    accuracy = (preds == labels).mean()
    precision = precision_score(labels, preds, average='weighted')
    recall = recall_score(labels, preds, average='weighted')
    f1 = f1_score(labels, preds, average='weighted')

    test_results[model_name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

    print(f"\n{model_name}:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")

# ════════════════════════════════════════════════════════════════════════════════
# 7. Visualizaciones
# ════════════════════════════════════════════════════════════════════════════════
print("\nGenerando gráficas de resultados...")

# Gráfico de pérdida
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for idx, (model_name, history) in enumerate(results.items()):
    ax = axes[idx]
    ax.plot(history['train_loss'], label='train loss', marker='o')
    ax.plot(history['val_loss'], label='val loss', marker='s')
    ax.set_title(f'{model_name} - Loss')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.legend()
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico de precisión
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for idx, (model_name, history) in enumerate(results.items()):
    ax = axes[idx]
    ax.plot(history['train_acc'], label='train acc', marker='o')
    ax.plot(history['val_acc'], label='val acc', marker='s')
    ax.set_title(f'{model_name} - Accuracy')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    ax.legend()
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Comparación de métricas
fig, ax = plt.subplots(figsize=(10, 6))
metrics = list(test_results[list(test_results.keys())[0]].keys())
x = np.arange(len(metrics))
width = 0.25

for idx, (model_name, scores) in enumerate(test_results.items()):
    values = [scores[metric] for metric in metrics]
    ax.bar(x + idx * width, values, width, label=model_name)

ax.set_xlabel('Métricas')
ax.set_ylabel('Puntuación')
ax.set_title('Comparación de Modelos en Test')
ax.set_xticks(x + width)
ax.set_xticklabels(metrics)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

# ════════════════════════════════════════════════════════════════════════════════
# 8. Conclusiones
# ════════════════════════════════════════════════════════════════════════════════
best_model_name = max(test_results.items(), key=lambda x: x[1]['accuracy'])

print("\n" + "="*80)
print("RESUMEN Y CONCLUSIONES")
print("="*80)
resumen = (
    f"\n# Se probaron tres arquitecturas de redes neuronales recurrentes:\n"
    f"  - RNN: Simple pero olvida contexto largo\n"
    f"  - GRU: Punto medio entre velocidad y capacidad\n"
    f"  - LSTM: Más lenta pero recuerda mejor frases largas\n\n"
    f"# Mejor modelo: {best_model_name[0]}\n"
    f"# Accuracy: {best_model_name[1]['accuracy']:.4f}\n"
    f"# F1-Score: {best_model_name[1]['f1']:.4f}\n\n"
    f"# Los gráficos muestran cómo cada red aprendió durante el entrenamiento\n"
    f"# Logramos predecir sentimientos en textos nuevos con buena precisión"
)
print(resumen)

# ════════════════════════════════════════════════════════════════════════════════
# 9. Pruebas con textos nuevos
# ════════════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("Probando el mejor modelo con textos nuevos...")
print("="*80)

best_model = models[best_model_name[0]]
best_model.load_state_dict(torch.load(f'models/best_{best_model_name[0]}.pt'))

test_tweets = [
    "Great flight! Very happy with the service",
    "The flight was cancelled, terrible experience",
    "Normal flight, nothing special",
    "Neutral experience",
    "Horrible flight",
    "Not so great experience",
    "Amazing airline, best experience ever"
]

print(f"\nModelo utilizado: {best_model_name[0]}\n")
for tweet in test_tweets:
    sentiment = predict_sentiment(tweet, best_model, vocab, DEVICE, classes, clean_text, text_to_sequence)
    print(f"  Tweet: '{tweet}'")
    print(f"  Sentimiento: {sentiment}\n")

print("Programa completado. Los modelos se han guardado en la carpeta 'models/'")

