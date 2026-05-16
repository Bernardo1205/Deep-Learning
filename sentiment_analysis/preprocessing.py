import re
from collections import Counter
from config import MIN_WORD_FREQ, MAX_SEQ_LENGTH, STOP_WORDS

# Limpiar texto: eliminar URLs, menciones, símbolos
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Construir vocabulario a partir de textos
def build_vocab(texts, min_freq=MIN_WORD_FREQ):
    word_counter = Counter()
    for text in texts:
        word_counter.update(text.split())

    vocab = {word: idx + 2 for idx, (word, count) in enumerate(
        [(w, c) for w, c in word_counter.items() if c >= min_freq]
    )}
    vocab['<PAD>'], vocab['<UNK>'] = 0, 1
    return vocab

# Convertir texto a secuencia numérica
def text_to_sequence(text, vocab, max_length=MAX_SEQ_LENGTH):
    words = text.split()
    sequence = [vocab.get(word, vocab['<UNK>']) for word in words]
    if len(sequence) < max_length:
        return sequence + [vocab['<PAD>']] * (max_length - len(sequence))
    return sequence[:max_length]

