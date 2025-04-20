import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from tqdm import tqdm
from typing import Tuple
import pandas as pd

class CNN(nn.Module):
    def __init__(self, num_classes=5):
        # (TODO) Design your CNN, it can only be less than 3 convolution layers
        super(CNN, self).__init__()
        # 1st Convolution Layer：input 3 channel（RGB）, output 16 feature map , kernel = 3x3 , padding = 1 →  keep size（224x224）
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(16) # Normalize output values, speed up training and improve stability
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2) # For each non-overlapping 2x2 block, take max → size halved (112x112)
        # 2nd Convolution Layer: input 16 channels, output 32 channels
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(32) # Normalize output values, speed up training and improve stability
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2) # For each non-overlapping 2x2 block, take max → size halved (56x56)

        # two pooling layers: 224 -> 112 -> 56, resulting in 32 x 56 x 56
        self.fc1 = nn.Linear(32 * 56 * 56, 128)         # make 128-dimensional feature vector
        self.dropout = nn.Dropout(0.5)                  # Randomly set 50% of neurons to zero
        self.fc2 = nn.Linear(128, num_classes)          # make 5 logits

    def forward(self, x):
        # (TODO) Forward the model
        x = self.pool(F.relu(self.bn1(self.conv1(x))))  # Each block: Conv → BN → ReLU → Pooling
        x = self.pool(F.relu(self.bn2(self.conv2(x))))  # Each block: Conv → BN → ReLU → Pooling
        x = x.view(x.size(0), -1)                       # make flatten
        x = F.relu(self.fc1(x))                         # make 128-dimensional and ReLU
        x = self.dropout(x)                             # Randomly set 50% of neurons to zero
        x = self.fc2(x)                                 # make 5 classes
        return x

def train(model: CNN, train_loader: DataLoader, criterion, optimizer, device)->float:
    # (TODO) Train the model and return the average loss of the data, we suggest use tqdm to know the progress
    model.train()                                       # Set model to training mode
    running_loss = 0.0                                  # Accumulate total loss
    for images, labels in tqdm(train_loader, desc="Training", leave=False):
        images, labels = images.to(device), labels.to(device) # Move data to device

        optimizer.zero_grad()                           # Reset gradients before backward pass
        outputs = model(images)                         # CNN Forward pass
        loss = criterion(outputs, labels)               # Compute loss
        loss.backward()                                 # Backward pass to compute gradients
        optimizer.step()                                # Update model parameters(according to gradients)

        running_loss += loss.item() * images.size(0)    # Accumulate loss

    avg_loss = running_loss / len(train_loader.dataset) # Compute average loss over entire dataset
    return avg_loss


def validate(model: CNN, val_loader: DataLoader, criterion, device)->Tuple[float, float]:
    # (TODO) Validate the model and return the average loss and accuracy of the data, we suggest use tqdm to know the progress
    model.eval()                                        # Set the model to evaluation mode
    # initialize
    running_loss = 0.0  
    correct = 0
    total = 0

    with torch.no_grad():                               # Disable gradient computation (faster and saves memory)
        for images, labels in tqdm(val_loader, desc="Validating", leave=False):
            images, labels = images.to(device), labels.to(device) # Move data to device
            
            outputs = model(images)                     # CNN Forward pass
            loss = criterion(outputs, labels)           # Compute loss
            running_loss += loss.item() * images.size(0)# accumulate loss

            _, predicted = torch.max(outputs, 1)        # Get the predicted class

            # Update total and correct prediction count
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    # Calculate average loss and accuracy
    avg_loss = running_loss / len(val_loader.dataset)
    accuracy = correct / total
    return avg_loss, accuracy

def test(model: CNN, test_loader: DataLoader, criterion, device):
    # (TODO) Test the model on testing dataset and write the result to 'CNN.csv'
    model.eval()                                        # Set the model to evaluation mode
    predictions = []
    ids = []

    with torch.no_grad():                               # Disable gradient computation (faster and saves memory)
        for images, image_ids in tqdm(test_loader, desc="Testing", leave=False):
            images = images.to(device)                  # Move data to device
            outputs = model(images)                     # CNN Forward pass
            _, predicted = torch.max(outputs, 1)        # Get the predicted class
            predictions.extend(predicted.cpu().numpy()) # Store predictions
            ids.extend(image_ids)                       # Store image IDs

    # Create a DataFrame to store results in the CSV
    df = pd.DataFrame({"id": ids, "prediction": predictions})
    df.to_csv("CNN.csv", index=False)
    print(f"Predictions saved to 'CNN.csv'")
    return