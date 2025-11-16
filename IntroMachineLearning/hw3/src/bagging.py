import typing as t
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from .utils import WeakClassifier


class BaggingClassifier:
    def __init__(self, input_dim: int) -> None:
        """Free to add args as you need, like batch-size, learning rate, etc."""

        # create 10 learners, dont change.
        self.learners = [
            WeakClassifier(input_dim=input_dim) for _ in range(10)
        ]

    def fit(self, X_train, y_train, num_epochs: int, learning_rate: float):
        """
        Bagging: train 10 learners, each on a bootstrap sample.
        """
        X = torch.tensor(X_train, dtype=torch.float32)
        y = torch.tensor(y_train, dtype=torch.float32)

        N = len(y)

        for learner in self.learners:

            # ------- bootstrap sampling -------
            idx = np.random.choice(N, size=N, replace=True)
            X_boot = X[idx]
            y_boot = y[idx]

            # optimizer for this specific learner
            optimizer = optim.Adam(learner.parameters(), lr=learning_rate)

            for epoch in range(num_epochs):
                optimizer.zero_grad()

                prob = learner(X_boot).view(-1)
                eps = 1e-12
                prob = torch.clamp(prob, eps, 1 - eps)

                loss_vec = -(
                    y_boot * torch.log(prob) +
                    (1 - y_boot) * torch.log(1 - prob)
                )
                loss = loss_vec.mean()

                loss.backward()
                optimizer.step()

        return self

    def predict_learners(self, X) -> t.Union[t.Sequence[int], t.Sequence[float]]:
        """
        Return:
            pred_classes: List[num_learners] of np.array shape (N,)
            pred_probs:   List[num_learners] of np.array shape (N,)
        """
        X = torch.tensor(X, dtype=torch.float32)

        pred_classes = []
        pred_probs = []

        for learner in self.learners:
            with torch.no_grad():
                prob = learner(X).view(-1).numpy()
                pred = (prob >= 0.5).astype(float)

            pred_classes.append(pred)
            pred_probs.append(prob)

        return pred_classes, pred_probs

    def compute_feature_importance(self) -> t.Sequence[float]:
        """
        Feature importance for Bagging:
        Average absolute weight across all learners.
        """
        num_features = self.learners[0].linear.weight.shape[1]
        importance = np.zeros(num_features)

        for learner in self.learners:
            w = learner.linear.weight.detach().cpu().numpy().reshape(-1)
            importance += np.abs(w) # 用絕對值避免正負相抵

        # average
        importance = importance / len(self.learners)

        # normalize to sum = 1
        importance = importance / (importance.sum() + 1e-12)

        return importance
