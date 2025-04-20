import numpy as np
import pandas as pd
from tqdm import tqdm
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import timm
from typing import List, Tuple

"""
Notice:
    1) You can't add any additional package
    2) You can add or remove any function "except" fit, _build_tree, predict
    3) You can ignore the suggested data type if you want
"""

class ConvNet(nn.Module): # Don't change this part!
    def __init__(self):
        super(ConvNet, self).__init__()
        self.model = timm.create_model('mobilenetv3_small_100', pretrained=True, num_classes=300)

    def forward(self, x):
        x = self.model(x)
        return x
    
class DecisionTree:
    def __init__(self, max_depth=1):
        self.max_depth = max_depth

    def fit(self, X: pd.DataFrame, y: np.ndarray):
        self.data_size = len(X)
        total_steps = 2 ** self.max_depth
        self.progress = tqdm(total=total_steps, desc="Growing tree", position=0, leave=True)
        self.tree = self._build_tree(X, y, depth=0)
        self.progress.close()

    def _build_tree(self, X: pd.DataFrame, y: np.ndarray, depth: int):
        # (TODO) Grow the decision tree and return it
        if len(set(y)) == 1 or depth == self.max_depth: # If all samples have the same label or max depth is reached
            return {'label': self._majority_class(y)}
        
        best_feature, best_threshold = self._best_split(X, y)

        if best_feature is None:                        # If no valid split is found, return a leaf node
            return {'label': self._majority_class(y)}
        
        self.progress.update(1)                         # Update the training progress

        # Split the dataset into left and right subsets
        left_X, left_y, right_X, right_y = self._split_data(X, y, best_feature, best_threshold)
        
        # Return a non-leaf node containing split info and two child subtrees
        return {
            'feature': best_feature,
            'threshold': best_threshold,
            'left': self._build_tree(left_X, left_y, depth + 1),
            'right': self._build_tree(right_X, right_y, depth + 1)
        }

    def predict(self, X: pd.DataFrame)->np.ndarray:
        # (TODO) Call _predict_tree to traverse the decision tree to return the classes of the testing dataset
        # For each sample x in X, recursively traverse the tree to get a prediction
        # Collect all predictions into a NumPy array and return
        return np.array([self._predict_tree(x, self.tree) for x in X])
        

    def _predict_tree(self, x, tree_node):
        # (TODO) Recursive function to traverse the decision tree
        if 'label' in tree_node:                        # Base case: if the current node is a leaf, return its label
            return tree_node['label']
        
        # If the feature value is less than or equal to the threshold, go to the left subtree
        if x[tree_node['feature']] <= tree_node['threshold']:
            return self._predict_tree(x, tree_node['left'])
        else:
            return self._predict_tree(x, tree_node['right'])

    def _split_data(self, X: pd.DataFrame, y: np.ndarray, feature_index: int, threshold: float):
        # (TODO) split one node into left and right node 
        left_dataset_X, left_dataset_y, right_dataset_X, right_dataset_y = [], [], [], []
        for xi, yi in zip(X, y):
            if xi[feature_index] <= threshold:          # If the selected feature value is less than or equal to the threshold
                left_dataset_X.append(xi)
                left_dataset_y.append(yi)
            else:
                right_dataset_X.append(xi)
                right_dataset_y.append(yi)
        return left_dataset_X, left_dataset_y, right_dataset_X, right_dataset_y

    def _best_split(self, X: pd.DataFrame, y: np.ndarray):
        # (TODO) Use Information Gain to find the best split for a dataset
        best_gain = -1                                  # Track the highest information gain found
        best_feature_index = None                       # Index of the best feature for splitting
        best_threshold = None                           # Threshold value for the best split
        n_features = len(X[0])                          # Number of features in the dataset

        for feature_index in range(n_features):
            thresholds = sorted(set([x[feature_index] for x in X])) # Extract all unique values for this feature

            # Optional optimization: limit the number of thresholds to at most 20
            if len(thresholds) > 20:
                step = max(1, len(thresholds) // 20)
                thresholds = thresholds[::step]

            for threshold in thresholds:
                # Split y into left and right subsets based on threshold
                left_y = [yi for xi, yi in zip(X, y) if xi[feature_index] <= threshold]
                right_y = [yi for xi, yi in zip(X, y) if xi[feature_index] > threshold]

                # Compute information gain from this split
                gain = self._information_gain(y, left_y, right_y)

                # Update best split if a higher gain is found
                if gain > best_gain:
                    best_gain = gain
                    best_feature_index = feature_index
                    best_threshold = threshold

        return best_feature_index, best_threshold

    def _entropy(self, y: np.ndarray)->float:
        # (TODO) Return the entropy
        counts = np.bincount(y)                         # Count the number of occurrences of each class label
        probs = counts / len(y)                         # Convert counts to probabilities by dividing by total number of samples
        return -np.sum([p * np.log2(p) for p in probs if p > 0])
    
    # add by myself
    def _information_gain(self, parent_y, left_y, right_y):
        if len(left_y) == 0 or len(right_y) == 0:       # If either child is empty, the split is useless → return 0 gain
            return 0
        parent_entropy = self._entropy(parent_y)        # Entropy before the split
        left_entropy = self._entropy(left_y)            # Entropy of the left subset
        right_entropy = self._entropy(right_y)          # Entropy of the right subset
        p_left = len(left_y) / len(parent_y)            # Proportion of samples going to the left child
        p_right = len(right_y) / len(parent_y)          # Proportion of samples going to the right child
        return parent_entropy - (p_left * left_entropy + p_right * right_entropy) # Parent entropy − Weighted child entropy

    # add by myself
    def _majority_class(self, y):
        # np.bincount(y): counts the number of occurrences for each integer label
        # argmax(): returns the index (i.e., the class label) with the highest count
        return np.bincount(y).argmax()

def get_features_and_labels(model: ConvNet, dataloader: DataLoader, device)->Tuple[List, List]:
    # (TODO) Use the model to extract features from the dataloader, return the features and labels
    model.eval() # Set the model to evaluation mode
    features = []
    labels = []
    with torch.no_grad(): # Disable gradient computation (faster and saves memory)
        for images, batch_labels in tqdm(dataloader, desc="Extracting features"):
            images = images.to(device) # Move data to device
            output = model(images) # ConvNet Forward pass
            features.extend(output.cpu().numpy()) # Move outputs to CPU, convert to NumPy, and append
            labels.extend(batch_labels.numpy()) # Convert labels to NumPy and append
    return features, labels

def get_features_and_paths(model: ConvNet, dataloader: DataLoader, device)->Tuple[List, List]:
    # (TODO) Use the model to extract features from the dataloader, return the features and path of the images
    model.eval() # Set the model to evaluation mode
    features = []
    paths = []
    with torch.no_grad(): # Disable gradient computation (faster and saves memory)
        for images, image_ids in tqdm(dataloader, desc="Extracting features"):
            images = images.to(device) # Move data to device
            output = model(images) # ConvNet Forward pass
            features.extend(output.cpu().numpy()) # Move outputs to CPU, convert to NumPy, and append
            paths.extend(image_ids) # Store image identifiers for result mapping
    return features, paths