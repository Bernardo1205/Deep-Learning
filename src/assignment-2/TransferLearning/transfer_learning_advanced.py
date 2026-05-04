import torch
import torch.nn as nn
import pandas as pd



#Load our model
base_model = torch.load('../CNN/models/model.pt')

# 2. Freeze the weights (The "Transfer" part)
for param in base_model.parameters():
    param.requires_grad = False


# 3. Create the Adaptor Model
class InsuranceTransferModel(nn.Module):
    def __init__(self, base_model):
        super(InsuranceTransferModel, self).__init__()
        # Remove the last classification layer of the CNN
        self.feature_extractor = nn.Sequential(*list(base_model.children())[:-1])

        # New "Head" for Regression
        self.regressor = nn.Sequential(
            nn.Linear(in_features=512, out_features=128),  # Adjust 512 to your model's output
            nn.ReLU(),
            nn.Linear(128, 1)  # Single output for insurance cost
        )

    def forward(self, x):
        # Tabular data needs to be reshaped to 'look' like an image for the CNN
        x = x.view(-1, 1, 1, 1)  # Example reshape
        x = self.feature_extractor(x)
        x = torch.flatten(x, 1)
        return self.regressor(x)


tl_model = InsuranceTransferModel(base_model)

