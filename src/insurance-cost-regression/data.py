
import pandas as pd
import seaborn as sns
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

def load_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Covert categorical columns to numeric using one-hot encoding , drop first col to prevent multicollinearity
    return pd.get_dummies(df, columns=["sex", "smoker", "region"], drop_first=True, dtype=int)


def plot_correlation(df: pd.DataFrame):
    corr = df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")


def prepare_data(csv_path: str) :
    dataset = load_dataset(csv_path)

    y = dataset["charges"]
    X = dataset.drop("charges", axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        shuffle=True
    )

    # Split para optimización , train vs val
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train,
        test_size=0.2,  # In our case validation
        random_state=42,
        shuffle=True
    )

    # Standardize the features using StandardScaler from the train Data
    scaler_x = StandardScaler()
    X_train = scaler_x.fit_transform(X_train)
    X_test = scaler_x.transform(X_test)
    X_val = scaler_x.transform(X_val)

    scaler_y = StandardScaler()
    # .fit_transform returns a 2D array, so we reshape y_train to have one column and as many rows as needed. After scaling, we flatten the array back to 1D since our target variable is a single value per sample.
    y_train = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).flatten()
    y_test = scaler_y.transform(y_test.values.reshape(-1, 1)).flatten()
    y_val = scaler_y.transform(y_val.values.reshape(-1, 1)).flatten()

    # Convert to tensors Dataset so we can parse to the DataLoader
    X_train = torch.tensor(X_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    X_val = torch.tensor(X_val, dtype=torch.float32)

    y_train = torch.tensor(y_train, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32)
    y_val = torch.tensor(y_val, dtype=torch.float32)

    # Once the train/test splits are converted to PyTorch tensors,wrap them in TensorDataset so each sample is returned as (features, target).
    train_td = TensorDataset(X_train, y_train)
    test_td = TensorDataset(X_test, y_test)
    val_td = TensorDataset(X_val, y_val)

    # DataLoader groups samples into mini-batches.
    # Example with batch_size=64:
    #   X batch shape -> [64, 8]
    #   y batch shape -> [64]
    # The model will output [64, 1] (one value per sample, 64 samples in the batch).
    train_loader = DataLoader(train_td, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_td, batch_size=64, shuffle=False)
    val_loader = DataLoader(val_td, batch_size=64, shuffle=False)

    return train_loader,  val_loader, test_loader ,scaler_x, scaler_y



