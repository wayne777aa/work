import typing as t
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from .utils import WeakClassifier


class AdaBoostClassifier:
    def __init__(self, input_dim: int, num_learners: int = 10) -> None:
        """Free to add args as you need, like batch-size, learning rate, etc."""

        self.sample_weights = None
        # create 10 learners, dont change.
        self.learners = [
            WeakClassifier(input_dim=input_dim) for _ in range(num_learners)
        ]
        self.alphas = []

    def fit(self, X_train, y_train, num_epochs: int = 1000, learning_rate: float = 0.01):
        """
        Train AdaBoost with weak logistic regression learners.
        """
        X = torch.tensor(X_train, dtype=torch.float32)
        y = torch.tensor(y_train, dtype=torch.float32)

        # convert y to {-1, +1}
        y_signed = y.clone()
        y_signed[y == 0] = -1  

        N = len(y)
        self.sample_weights = torch.ones(N) / N

        self.alphas = []

        for t, learner in enumerate(self.learners):

            # optimizer for this learner
            optimizer = optim.Adam(learner.parameters(), lr=learning_rate)

            for epoch in range(num_epochs):
                optimizer.zero_grad()

                # forward
                prob = learner(X).view(-1)        # sigmoid outputs
                eps = 1e-12
                prob = torch.clamp(prob, eps, 1 - eps)

                # BCE per-sample
                loss_vec = -(
                    y * torch.log(prob) + (1 - y) * torch.log(1 - prob)
                )

                # weighted loss
                weighted_loss = (self.sample_weights * loss_vec).sum()

                weighted_loss.backward()
                optimizer.step()

            # ---------- after training this learner ----------
            # compute predictions (hard label for error)
            with torch.no_grad():
                prob = learner(X).view(-1)
                prob = torch.clamp(prob, 1e-7, 1 - 1e-7)
                preds = (prob >= 0.5).float()

            # convert to {-1, +1}
            preds_signed = preds.clone()
            preds_signed[preds == 0] = -1

            # weighted error
            incorrect = (preds_signed != y_signed).float()
            weighted_error = (self.sample_weights * incorrect).sum().item()

            # avoid division by zero or invalid alpha
            weighted_error = max(min(weighted_error, 0.999), 1e-6)

            alpha_t = 0.5 * np.log((1 - weighted_error) / weighted_error)
            self.alphas.append(alpha_t)

            # update sample weights
            w_new = self.sample_weights * torch.exp(-alpha_t * y_signed * preds_signed)
            w_new = w_new / w_new.sum()
            self.sample_weights = w_new

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
        Feature importance for AdaBoost:
        Sum over learners of |alpha_t| * |weight_t|
        """
        num_features = self.learners[0].linear.weight.shape[1]
        importance = np.zeros(num_features)
        # AdaBoost 的第 t 個弱分類器的權重, 第 t 個弱分類器的線性模型
        for alpha_t, learner in zip(self.alphas, self.learners):
            w = learner.linear.weight.detach().cpu().numpy().reshape(-1)
            importance += np.abs(alpha_t) * np.abs(w) # 每個 feature 的重要性 = Σ_t |α_t| × |w_t[i]|

        # Normalize so sum = 1
        importance = importance / (importance.sum() + 1e-12) # 1e-12 避免除以 0
        return importance
