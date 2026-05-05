# 2. Configuración inicial
device = get_device()
model_path = "model.pt"
head_save_path = "transfer_learning_head.pt"

# 3. Cargar el modelo base
base_model, base_available = load_base_model(model_path, device, input_size=4096)

if base_available:
    print("Modelo base cargado desde model.pt")
else:
    print("Usando modelo simulado como base (model.pt no válido)")

# 4. Preparar componentes de Transfer Learning
feature_extractor, regressor, is_cnn_base, feat_dim = prepare_transfer_components(
    base_model=base_model,
    input_size=4096,
    device=device,
    dropout_p=0.2
)

print(f"Extractor de características preparado (congelado)")
print(f"Cabeza regresora creada (entrada: {feat_dim} features)")

# 5. Mostrar resumen de parámetros
print_transfer_summary(feature_extractor, regressor)

# 6. Entrenar solo la cabeza (Transfer Learning)
history = train_model_components(
    feature_extractor=feature_extractor,
    regressor=regressor,
    train_loader=train_loader,
    val_loader=test_loader,
    device=device,
    input_size=4096,
    epochs=100,
    lr=1e-3,
    label="Transfer Learning Model (from scratch base)"
)

# 7. Evaluar en test set
preds_tl, reals_tl = get_predictions_components(
    feature_extractor=feature_extractor,
    regressor=regressor,
    loader=test_loader,
    device=device,
    input_size=4096,
    scaler_y=None
)

# 8. Guardar la cabeza entrenada
save_transfer_head(regressor, head_save_path)
print(f"\n✓ Cabeza de Transfer Learning guardada en: {head_save_path}")

# 9. Comparación rápida: Predicciones vs Reales
print(" Resultados de transfer learning:")
print(f"Predicciones generadas: {len(preds_tl)}")
print(f"Error promedio (MSE): {np.mean((preds_tl - reals_tl)**2):.4f}")
print(f"Rango de predicciones: [{preds_tl.min():.4f}, {preds_tl.max():.4f}]")
print(f"Rango de valores reales: [{reals_tl.min():.4f}, {reals_tl.max():.4f}]")

# 10. Visualizar histórico de entrenamiento
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.plot(history["train_loss"], label="Train Loss", marker='o')
ax.plot(history["val_loss"], label="Val Loss", marker='s')
ax.set_xlabel("Epoch")
ax.set_ylabel("MSE Loss")
ax.set_title("Transfer Learning: Training History")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 11. Gráfico de predicciones vs reales
fig2, ax2 = plt.subplots(1, 1, figsize=(10, 6))
ax2.scatter(reals_tl, preds_tl, alpha=0.5, s=30)
# Línea perfecta (y=x)
min_val = min(reals_tl.min(), preds_tl.min())
max_val = max(reals_tl.max(), preds_tl.max())
ax2.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label="Perfect prediction")
ax2.set_xlabel("Actual values")
ax2.set_ylabel("Predicted values")
ax2.set_title("Transfer Learning: Predictions vs Actual")
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("Transfer Learning completed ")

