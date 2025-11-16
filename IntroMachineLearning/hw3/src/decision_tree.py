import numpy as np


class DecisionTree:
    def __init__(self, max_depth=1):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.tree = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))

        # stopping conditions
        if num_labels == 1:
            return {"value": np.unique(y)[0]}

        if depth >= self.max_depth:
            majority = np.bincount(y).argmax()
            return {"value": majority}

        feature, threshold, info_gain = find_best_split(X, y)

        if feature is None or info_gain <= 0:
            majority = np.bincount(y).argmax()
            return {"value": majority}

        X_left, y_left, X_right, y_right = split_dataset(X, y, feature, threshold)

        left_subtree = self._grow_tree(X_left, y_left, depth + 1)
        right_subtree = self._grow_tree(X_right, y_right, depth + 1)

        return {
            "feature": feature,
            "threshold": threshold,
            "info_gain": info_gain,
            "n_samples": num_samples,
            "n_features": num_features,
            "left": left_subtree,
            "right": right_subtree
        }

    def predict(self, X):
        """
        Predict labels for each row in X.
        """
        preds = []
        for x in X:
            pred = self._predict_tree(x, self.tree)
            preds.append(pred)
        return np.array(preds)

    def _predict_tree(self, x, tree_node):
        """
        x: a single sample (1D array)
        node: current node in decision tree (dict)
        """
        # leaf node
        if "value" in tree_node:
            return tree_node["value"]

        feature = tree_node["feature"]
        threshold = tree_node["threshold"]

        # go left or right
        if x[feature] <= threshold:
            return self._predict_tree(x, tree_node["left"])
        else:
            return self._predict_tree(x, tree_node["right"])
        
    def compute_feature_importance(self):
        """
        Compute feature importance based on information gain at each split.
        Importance = weighted sum of IG.
        """
        num_features = self.tree["n_features"]
        importance = np.zeros(num_features)

        def traverse(node):
            # leaf node
            if "value" in node:
                return

            feature = node["feature"]
            ig = node["info_gain"]
            n = node["n_samples"]

            importance[feature] += ig * n  # weighted contribution

            traverse(node["left"])
            traverse(node["right"])

        traverse(self.tree)

        # normalize
        importance = importance / (importance.sum() + 1e-12)
        return importance


# Split dataset based on a feature and threshold
def split_dataset(X, y, feature_index, threshold):
    """
    Return:
        X_left, y_left, X_right, y_right
    """
    feature_values = X[:, feature_index]
    
    left_mask = feature_values <= threshold
    right_mask = feature_values > threshold

    X_left = X[left_mask]
    y_left = y[left_mask]

    X_right = X[right_mask]
    y_right = y[right_mask]

    return X_left, y_left, X_right, y_right


# Find the best split for the dataset
def find_best_split(X, y):
    """
    Try all features and all unique thresholds.
    Return:
        best_feature, best_threshold, best_info_gain
    """
    n_samples, n_features = X.shape

    # parent entropy
    parent_entropy = entropy(y)

    best_feature = None
    best_threshold = None
    best_info_gain = -np.inf

    for feature in range(n_features):

        feature_values = X[:, feature]
        thresholds = np.unique(feature_values)

        for threshold in thresholds:

            X_left, y_left, X_right, y_right = split_dataset(
                X, y, feature, threshold
            )

            # skip invalid split
            if len(y_left) == 0 or len(y_right) == 0:
                continue

            # compute information gain
            n_left = len(y_left)
            n_right = len(y_right)

            child_entropy = (
                (n_left / n_samples) * entropy(y_left)
                + (n_right / n_samples) * entropy(y_right)
            )

            info_gain = parent_entropy - child_entropy

            # update best split
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_feature = feature
                best_threshold = threshold

    return best_feature, best_threshold, best_info_gain


def entropy(y):
    """
    y: numpy array of 0/1 labels
    """
    values, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)

    ent = 0.0
    for p in probs:
        if p > 0:
            ent -= p * np.log2(p)
    return ent