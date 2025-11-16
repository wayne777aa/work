import typing as t
import torch
import numpy as np
import torch.nn as nn
from sklearn.metrics import roc_curve, auc


class WeakClassifier(nn.Module):
    """
    Use pyTorch to implement a 1 ~ 2 layer model.
    No non-linear activation in the `intermediate layers` allowed.
    """
    def __init__(self, input_dim):
        super(WeakClassifier, self).__init__()
        self.linear = nn.Linear(input_dim, 1, bias=True)

    def forward(self, x):
        # x: numpy array or torch tensor
        if isinstance(x, np.ndarray):
            x = torch.tensor(x, dtype=torch.float32)

        logits = self.linear(x)
        probs = torch.sigmoid(logits)
        probs = torch.clamp(probs, 1e-7, 1 - 1e-7)
        return probs


def entropy_loss(outputs, targets):
    """
    outputs: (N, 1) sigmoid probabilities
    targets: (N,) or (N, 1)
    return: scalar BCE loss
    """
    eps = 1e-12
    targets = targets.view(-1)
    outputs = outputs.view(-1)

    loss = -(
        targets * torch.log(outputs + eps) +
        (1 - targets) * torch.log(1 - outputs + eps)
    )
    return loss.mean()


def plot_learners_roc(
    y_preds: t.List[t.Sequence[float]],
    y_trues: t.Sequence[int],
    fpath='./tmp.png',
):
    """
    y_preds: list of length T, each element is prob array of shape (N,)
    y_trues: (N,)
    """
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, auc

    plt.figure(figsize=(8, 6))
    y_trues = np.array(y_trues)

    for i, pred in enumerate(y_preds):
        pred = np.array(pred)
        fpr, tpr, _ = roc_curve(y_trues, pred)
        auc_score = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'Learner {i+1} (AUC={auc_score:.3f})')

    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves of Weak Learners')
    plt.legend()
    plt.grid(True)

    plt.savefig(fpath, dpi=300)
    plt.close()