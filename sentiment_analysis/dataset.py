import torch
from torch.utils.data import Dataset
from preprocessing import text_to_sequence
from config import MAX_SEQ_LENGTH

# Dataset personalizado para tweets
class TwitterDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_length=MAX_SEQ_LENGTH, already_encoded=False):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_length = max_length
        self.already_encoded = already_encoded

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        if self.already_encoded:
            sequence = torch.tensor(self.texts[idx], dtype=torch.long)
        else:
            sequence = torch.tensor(
                text_to_sequence(text, self.vocab, self.max_length),
                dtype=torch.long
            )
        return sequence, label

