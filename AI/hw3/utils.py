from torchvision import transforms
from torch.utils.data import Dataset
import os
import PIL
from typing import List, Tuple
import matplotlib.pyplot as plt

class TrainDataset(Dataset):
    def __init__(self, images, labels):
        self.transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=3),    # RGB
            transforms.Resize((224, 224)),                  # resize to 224x224
            transforms.ToTensor()                           # transform to PyTorch tensor
        ])
        self.images, self.labels = images, labels

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image_path = self.images[idx]
        image = PIL.Image.open(image_path)                  # open image

        if self.transform:
            image = self.transform(image)                   # transform

        label = self.labels[idx]
        return image, label

class TestDataset(Dataset):
    def __init__(self, image):
        self.transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=3),    # RGB
            transforms.Resize((224, 224)),                  # resize to 224x224
            transforms.ToTensor()                           # transform to PyTorch tensor
        ])
        self.image = image

    def __len__(self):
        return len(self.image)

    def __getitem__(self, idx):
        image_path = self.image[idx]
        image = PIL.Image.open(image_path)                  # open image

        if self.transform:
            image = self.transform(image)                   # transform

        base_name = os.path.splitext(os.path.basename(image_path))[0] # ID
        return image, base_name
    
def load_train_dataset(path: str='data/train/')->Tuple[List, List]:
    # (TODO) Load training dataset from the given path, return images and labels
    images = []
    labels = []
    label_dict = {0: "elephant", 1: "jaguar", 2: "lion", 3: "parrot", 4: "penguin"} # number and name

    for label_idx, label_name in label_dict.items(): 
        folder_path = os.path.join(path, label_name)        # folder_path
        if not os.path.isdir(folder_path):
            continue
        for filename in os.listdir(folder_path):            # find filename
            if filename.lower().endswith(('jpg', 'jpeg', 'png')): # make name lowercase ,check if it is the image
                images.append(os.path.join(folder_path, filename)) # path and filename save into images
                labels.append(label_idx)                    # index save into labels

    return images, labels

def load_test_dataset(path: str='data/test/')->List:
    # (TODO) Load testing dataset from the given path, return images
    images = []
    for filename in os.listdir(path):
        if filename.lower().endswith(('jpg', 'jpeg', 'png')): # make name lowercase ,check if it is the image
            images.append(os.path.join(path, filename))     # path and filename save into images
    return images

def plot(train_losses: List, val_losses: List):
    # (TODO) Plot the training loss and validation loss of CNN, and save the plot to 'loss.png'
    #        xlabel: 'Epoch', ylabel: 'Loss'
    plt.figure()
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Training and Validation Loss')
    plt.savefig('loss.png')
    print("Save the plot to 'loss.png'")