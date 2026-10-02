#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de prueba para verificar que todos los módulos funcionan correctamente
Ejecutar: python test_modules.py
"""

import torch
import sys

print("="*70)
print("VERIFICACIÓN DE MÓDULOS - SENTIMENT ANALYSIS")
print("="*70)

try:
    print("\n1. Verificando config...")
    from sentiment_analysis.config import DEVICE, MAX_SEQ_LENGTH, vocab_size
    print(f"   ✓ Dispositivo detectado: {DEVICE}")
    print(f"   ✓ Max sequence length: {MAX_SEQ_LENGTH}")

    print("\n2. Verificando preprocessing...")
    from sentiment_analysis.preprocessing import clean_text, build_vocab, text_to_sequence
    test_text = "Hey @user check this! http://bit.ly/xyz #awesome"
    cleaned = clean_text(test_text)
    print(f"   ✓ Texto original: {test_text}")
    print(f"   ✓ Texto limpio: {cleaned}")

    print("\n3. Verificando construcción de vocabulario...")
    test_texts = ["hello world", "test sentence", "another example"]
    vocab = build_vocab(test_texts)
    print(f"   ✓ Vocabulario creado con {len(vocab)} palabras")
    print(f"   ✓ Tokens especiales: PAD={vocab['<PAD>']}, UNK={vocab['<UNK>']}")

    print("\n4. Verificando conversión a secuencias...")
    sequence = text_to_sequence(cleaned, vocab)
    print(f"   ✓ Secuencia generada: {sequence[:5]}... (longitud: {len(sequence)})")

    print("\n5. Verificando modelos...")
    from sentiment_analysis.models import RNNClassifier, GRUClassifier, LSTMClassifier

    test_vocab_size = 1000
    test_batch = torch.randint(0, test_vocab_size, (2, MAX_SEQ_LENGTH))

    rnn = RNNClassifier(test_vocab_size, 64, 128, 3, 1, 0.2).to(DEVICE)
    gru = GRUClassifier(test_vocab_size, 64, 128, 3, 1, 0.2).to(DEVICE)
    lstm = LSTMClassifier(test_vocab_size, 64, 128, 3, 1, 0.2).to(DEVICE)

    rnn_out = rnn(test_batch.to(DEVICE))
    gru_out = gru(test_batch.to(DEVICE))
    lstm_out = lstm(test_batch.to(DEVICE))

    print(f"   ✓ RNN output shape: {rnn_out.shape}")
    print(f"   ✓ GRU output shape: {gru_out.shape}")
    print(f"   ✓ LSTM output shape: {lstm_out.shape}")

    print("\n6. Verificando FocalLoss...")
    from sentiment_analysis.loss import FocalLoss
    class_weights = torch.tensor([1.0, 1.5, 2.0])
    focal_loss = FocalLoss(alpha=class_weights, gamma=2.0)

    test_output = torch.randn(4, 3, requires_grad=True)
    test_labels = torch.tensor([0, 1, 2, 1])
    loss_val = focal_loss(test_output, test_labels)
    print(f"   ✓ FocalLoss calculada: {loss_val:.4f}")

    print("\n7. Verificando Dataset...")
    from sentiment_analysis.dataset import TwitterDataset

    test_texts = ["hello world", "test example"]
    test_labels = [0, 1]
    dataset = TwitterDataset(test_texts, test_labels, vocab)
    print(f"   ✓ Dataset creado con {len(dataset)} ejemplos")

    sample_seq, sample_label = dataset[0]
    print(f"   ✓ Sample sequence shape: {sample_seq.shape}")
    print(f"   ✓ Sample label: {sample_label}")

    print("\n8. Verificando funciones de entrenamiento...")
    from sentiment_analysis.training import train_epoch, evaluate
    print(f"   ✓ Función train_epoch importada")
    print(f"   ✓ Función evaluate importada")

    print("\n9. Verificando utilidades...")
    from sentiment_analysis.utils import setup_plot_style, print_dataset_summary
    setup_plot_style()
    print(f"   ✓ Setup de plots configurado")

    print("\n" + "="*70)
    print("✓ TODOS LOS MÓDULOS SE VERIFICARON CORRECTAMENTE")
    print("="*70)
    print("\nPuedes ejecutar 'python main.py' para iniciar el análisis completo")
    print("="*70 + "\n")

except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

