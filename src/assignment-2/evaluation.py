import random
import torch
from torchvision.datasets import ImageFolder
from models import AlexNet
from transforms import get_transform
from constants import DATASET_DIR, NUM_CLASSES


def run_evaluation(model_path, num_examples=5, device=None):
    """
    Evaluate model on random test examples.

    Loads a trained model and displays predictions vs actual labels
    for random samples from the test set.

    Args:
        model_path: Path to saved model checkpoint (e.g., "model.pt")
        num_examples: Number of examples to evaluate
        device: Device to run on (if None, uses cuda if available)
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load checkpoint
    checkpoint = torch.load(model_path, map_location="cpu")

    # Recreate model
    model = AlexNet(num_classes=NUM_CLASSES)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    transform = get_transform(checkpoint["best_params"])
    test_dataset = ImageFolder(DATASET_DIR / "test", transform=transform)
    indices = random.sample(range(len(test_dataset)), num_examples)

    with torch.no_grad():
        for idx in indices:
            # Get image and true label
            original_img, label = test_dataset[idx]

            # Add batch dimension and move to device
            original_img = original_img.unsqueeze(0).to(device)

            # Forward pass
            output = model(original_img)

            # Get probabilities
            probabilities = torch.softmax(output, dim=1)

            # Get predicted class
            prediction = torch.argmax(probabilities, dim=1).item()

            print(f"Prediction: {prediction}| Actual:{label}")

