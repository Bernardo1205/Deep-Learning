import torch
from data import prepare_data
from model import InsuranceNN
from train_utils import predict



def run_evaluation(model_path: str = "model.pt", csv_path: str = "dataset/insurance.csv", n_examples: int = 10):
    device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
    train_loader, val_loader, test_loader, scaler_x, scaler_y = prepare_data(csv_path=csv_path)

    checkpoint = torch.load(model_path)
    best = checkpoint["best_params"]

    model = InsuranceNN(best["h1"], best["h2"], best["h3"]).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])


    y_pred, y_true = predict(model,test_loader, device,scaler_y)

    for i in range(n_examples):
        print(f"Real: ${y_true[i]:.2f} | Pred: ${y_pred[i]:.2f}")


if __name__ == "__main__":
    run_evaluation()

