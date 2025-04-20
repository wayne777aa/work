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
        if len(set(y)) == 1 or depth == self.max_depth:
            return {'label': self._majority_class(y)}
        
        best_feature, best_threshold = self._best_split(X, y)
        if best_feature is None:
            return {'label': self._majority_class(y)}
        
        self.progress.update(1)

        left_X, left_y, right_X, right_y = self._split_data(X, y, best_feature, best_threshold)
        

        return {
            'feature': best_feature,
            'threshold': best_threshold,
            'left': self._build_tree(left_X, left_y, depth + 1),
            'right': self._build_tree(right_X, right_y, depth + 1)
        }

    def predict(self, X: pd.DataFrame)->np.ndarray:
        # (TODO) Call _predict_tree to traverse the decision tree to return the classes of the testing dataset
        return np.array([self._predict_tree(x, self.tree) for x in X])

    def _predict_tree(self, x, tree_node):
        # (TODO) Recursive function to traverse the decision tree
        if 'label' in tree_node:
            return tree_node['label']
        if x[tree_node['feature']] <= tree_node['threshold']:
            return self._predict_tree(x, tree_node['left'])
        else:
            return self._predict_tree(x, tree_node['right'])

    def _split_data(self, X: pd.DataFrame, y: np.ndarray, feature_index: int, threshold: float):
        # (TODO) split one node into left and right node 
        left_dataset_X, left_dataset_y, right_dataset_X, right_dataset_y = [], [], [], []
        for xi, yi in zip(X, y):
            if xi[feature_index] <= threshold:
                left_dataset_X.append(xi)
                left_dataset_y.append(yi)
            else:
                right_dataset_X.append(xi)
                right_dataset_y.append(yi)
        return left_dataset_X, left_dataset_y, right_dataset_X, right_dataset_y

    def _best_split(self, X: pd.DataFrame, y: np.ndarray):
        # (TODO) Use Information Gain to find the best split for a dataset
        best_gain = -1
        best_feature_index = None
        best_threshold = None
        n_features = len(X[0])

        for feature_index in range(n_features):
            thresholds = sorted(set([x[feature_index] for x in X]))

            if len(thresholds) > 20:
                step = max(1, len(thresholds) // 20)
                thresholds = thresholds[::step]

            for threshold in thresholds:
                left_y = [yi for xi, yi in zip(X, y) if xi[feature_index] <= threshold]
                right_y = [yi for xi, yi in zip(X, y) if xi[feature_index] > threshold]
                gain = self._information_gain(y, left_y, right_y)
                if gain > best_gain:
                    best_gain = gain
                    best_feature_index = feature_index
                    best_threshold = threshold

        return best_feature_index, best_threshold

    def _entropy(self, y: np.ndarray)->float:
        # (TODO) Return the entropy
        counts = np.bincount(y)
        probs = counts / len(y)
        return -np.sum([p * np.log2(p) for p in probs if p > 0])
    
    # add by myself
    def _information_gain(self, parent_y, left_y, right_y):
        if len(left_y) == 0 or len(right_y) == 0:
            return 0
        parent_entropy = self._entropy(parent_y)
        left_entropy = self._entropy(left_y)
        right_entropy = self._entropy(right_y)
        p_left = len(left_y) / len(parent_y)
        p_right = len(right_y) / len(parent_y)
        return parent_entropy - (p_left * left_entropy + p_right * right_entropy)

    # add by myself
    def _majority_class(self, y):
        return np.bincount(y).argmax()

def get_features_and_labels(model: ConvNet, dataloader: DataLoader, device)->Tuple[List, List]:
    # (TODO) Use the model to extract features from the dataloader, return the features and labels
    model.eval()
    features = []
    labels = []
    with torch.no_grad():
        for images, batch_labels in tqdm(dataloader, desc="Extracting features"):
            images = images.to(device)
            output = model(images)
            features.extend(output.cpu().numpy())
            labels.extend(batch_labels.numpy())
    return features, labels

def get_features_and_paths(model: ConvNet, dataloader: DataLoader, device)->Tuple[List, List]:
    # (TODO) Use the model to extract features from the dataloader, return the features and path of the images
    model.eval()
    features = []
    paths = []
    with torch.no_grad():
        for images, image_ids in tqdm(dataloader, desc="Extracting features"):
            images = images.to(device)
            output = model(images)
            features.extend(output.cpu().numpy())
            paths.extend(image_ids)
    return features, paths