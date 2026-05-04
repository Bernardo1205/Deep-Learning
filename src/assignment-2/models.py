import torch
import torch.nn as nn


class AlexNet(nn.Module):
    """
    AlexNet architecture for 12-class image classification.

    This is an adaptation of the classic AlexNet architecture designed to work
    with variable input image sizes using adaptive pooling layers.
    """
    def __init__(self, num_classes=12):
        super(AlexNet, self).__init__()

        self.features = nn.Sequential(
            # First convolutional layer: 3 input channels -> 96 output channels
            # Kernel 11x11, stride 4 for aggressive downsampling
            nn.Conv2d(in_channels=3, out_channels=96, kernel_size=11, stride=4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Second convolutional layer: 96 -> 256 channels
            nn.Conv2d(in_channels=96, out_channels=256, kernel_size=5, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Third convolutional layer: 256 -> 384 channels
            nn.Conv2d(in_channels=256, out_channels=384, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),

            # Fourth convolutional layer: 384 -> 384 channels
            nn.Conv2d(in_channels=384, out_channels=384, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),

            # Fifth convolutional layer: 384 -> 256 channels
            nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),

            # Allows CNNs to accept images of varying dimensions without changing the network architecture.
            # It automatically calculates the necessary kernel size and stride
            nn.AdaptiveAvgPool2d((1, 1)),
            # Flatten the output to [batch_size, 256*6*6] = [batch_size, 9216]
            nn.Flatten()
        )

        # Fully connected layers for classification
        self.classifier = nn.Sequential(
            nn.Linear(in_features=256, out_features=4096),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=4096, out_features=4096),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=4096, out_features=num_classes),
        )

    def forward(self, x):
        """
        Forward pass through the network.

        Args:
            x: Input tensor of shape [batch_size, 3, height, width]

        Returns:
            Logits of shape [batch_size, num_classes]
        """
        x = self.features(x)
        x = self.classifier(x)
        return x

