import torch


def train(model, train_loader, optimizer, loss_fn, device):
    model.train()
    for data, target in train_loader:
        # Send the data to the device in our case GPU
        data, target = data.to(device), target.to(device)

        # Zero out the gradients from the previous iteration to prevent accumulation .If we don't do this, gradients would add up across batches leading to incorrect weight updates
        optimizer.zero_grad()

        # model(data) returns [batch_size, 1].
        # targets are [batch_size], so we remove only the last dimension to match shapes for MSELoss: [batch_size, 1] -> [batch_size] we apply the squeeze function.
        prediction = model(data).squeeze()

       # Compute the loss (Mean Squared Error) between predictions and actual targets
        loss = loss_fn(prediction, target)

        # Backward pass: compute gradients of the loss with respect to all model parameters .This calculates partial derivative of the loss and wights for every weight in the network
        loss.backward()

        # Update the model parameters using the computed gradients and the learning rate.
        # New weight = old weight - learning_rate × gradient
        optimizer.step()


def validation(model, val_loader, loss_fn, device) -> float:
    model.eval()
    total = 0.0
    with torch.no_grad():
        for data, target in val_loader:
            data, target = data.to(device), target.to(device)
            prediction = model(data).squeeze()
            total += loss_fn(prediction, target).item()
    return total / len(val_loader)


def predict(model, test_loader, device , scaler_y):
    model.eval()
    preds = []
    reals = []

    # torch.no_grand() deactivates the calculations of gradients
    with torch.no_grad():
        # We use test dataset to see how our model performs
        for x_batch, y_batch in test_loader:
            # Move the input batch to the specified device (GPU or CPU)
            x_batch = x_batch.to(device)

            # Forward pass through the model and squeeze to remove the last dimension [batch_size, 1] -> [batch_size], then move to CPU for storage
            y_hat = model(x_batch).squeeze()

            # Append the model predictions for this batch to the list
            preds.append(y_hat)

            # Append the actual target values for this batch to the list
            reals.append(y_batch)

    # Concatenate all prediction tensors from all batches into a single tensor total_samples and do the same for the true target values.
    y_pred = torch.cat(preds)
    y_true = torch.cat(reals)

    # Here we denormalise the target variables by using the inverse of our Scalar Transformer trained by using the Test set
    # We use .reshape(-1,1) because inverse_transform needs a 2D array then we add this new Dimension by applying .reshape(-1,1) and once it is inversed we remove it by doing .flatten()
    y_pred_original = scaler_y.inverse_transform(y_pred.numpy().reshape(-1, 1)).flatten()
    y_true_original = scaler_y.inverse_transform(y_true.numpy().reshape(-1, 1)).flatten()

    return y_pred_original, y_true_original

