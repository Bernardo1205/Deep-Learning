import torch
import warnings

warnings.filterwarnings('ignore')

# Dispositivo
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Constantes de procesamiento de texto
MIN_WORD_FREQ = 2
MAX_SEQ_LENGTH = 30

# Hiperparámetros de entrenamiento (después de Optuna)
EMBEDDING_DIM = 64
HIDDEN_DIM = 256
NUM_LAYERS = 1
DROPOUT = 0.2537625356455452
LEARNING_RATE = 0.004695367048662512
BATCH_SIZE = 128
EPOCHS = 10

# Hiperparámetros de Optuna
N_TRIALS = 20
OPTUNA_EPOCHS = 8

# Focal Loss
FOCAL_LOSS_GAMMA = 2.0

# Stopwords inglés (excluyendo negaciones)
STOP_WORDS = {
    "the", "a", "an", "to", "and", "is", "in", "it", "of", "for", "on", "at", "as", "be",
    "this", "that", "with", "was", "are", "i", "my", "me", "we", "you", "he", "she",
    "they", "our", "your", "have", "had", "has", "not", "but", "so", "or", "if", "can",
    "do", "did", "no", "up", "by", "just", "from", "its", "im", "get", "got", "will",
    "about", "all", "been", "were", "there", "their", "than", "s", "t", "amp", "rt",
    "would", "could", "should", "out", "us", "am", "now", "when", "what", "how",
    "more", "also", "any", "one", "like", "time", "much", "then", "very", "some", "him"
}

# Negaciones que se mantienen (no se eliminan)
NEGATIONS = {
    'not', 'no', 'nor', 'never', 'none', 'neither', 'cannot', 'isn', 'aren',
    'wasnt', 'werent', 'hasn', 'haven', 'hadnt', 'doesn', 'don', 'didn', 'won',
    'wouldn', 'shan', 'shouldn', 'couldn', 'mustn'
}

STOP_WORDS = STOP_WORDS - NEGATIONS

# Rutas
DATASET_PATH = "dataset/Tweets.csv"
MODELS_SAVE_PATH = "models/"
OPTUNA_DB_PATH = "sqlite:///optuna_study.db"

