import typing as t
from sklearn.metrics import roc_auc_score
import numpy as np
import numpy.typing as npt
import pandas as pd
from loguru import logger
import matplotlib.pyplot as plt


class LogisticRegression:
    def __init__(self, learning_rate: float = 1e-4, num_iterations: int = 100):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.intercept = None

    def fit(
        self,
        inputs: npt.NDArray[np.float64],
        targets: t.Sequence[int],  # 0 or 1
    ) -> None:
        """
        Implement your fitting function here.
        The weights and intercept should be kept in self.weights and self.intercept.
        """
        n_samples, n_features = inputs.shape
        self.weights = np.zeros(n_features)  # Initialize weights to zeros
        self.intercept = 0.0

        for i in range(self.num_iterations):
            linear = np.dot(inputs, self.weights) + self.intercept  # z = Xw + b
            pred = self.sigmoid(linear)  # predicted probabilities
            error = pred - targets

            dw = (1 / n_samples) * np.dot(inputs.T, error)  # gradient of weights
            db = (1 / n_samples) * np.sum(error)  # gradient of intercept

            self.weights -= self.learning_rate * dw  # update weights
            self.intercept -= self.learning_rate * db  # update intercept
            if i % 5000 == 0:
                _, preds = self.predict(inputs)
                acc = accuracy_score(targets, preds)
                logger.info(f"Iteration {i+1}, Train-Acc={acc:.4f}")

    def predict(self, inputs) -> t.Tuple[np.ndarray, np.ndarray]:
        """
        Implement your prediction function here.
        The return should contains
        1. sample probabilty of being class_1
        2. sample predicted class
        """
        linear = np.dot(inputs, self.weights) + self.intercept
        probs = self.sigmoid(linear)
        classes = (probs >= 0.5).astype(int)  # probs >= 0.5 -> class 1, else class 0
        return probs, classes

    def sigmoid(self, x):
        """
        Implement the sigmoid function.
        """
        return 1 / (1 + np.exp(-x))  # change into 0~1


class FLD:
    """Implement FLD
    You can add arguments as you need,
    but don't modify those already exist variables.
    """
    def __init__(self):
        self.w = None
        self.m0 = None
        self.m1 = None
        self.sw = None
        self.sb = None
        self.slope = None

    def fit(
        self,
        inputs: npt.NDArray[np.float64],
        targets: t.Sequence[int],
    ) -> None:
        """Compute m0, m1, Sw, Sb, and projection direction w."""
        # 分出兩個類別的資料
        class0 = inputs[np.array(targets) == 0]
        class1 = inputs[np.array(targets) == 1]

        # 類別平均
        self.m0 = np.mean(class0, axis=0)
        self.m1 = np.mean(class1, axis=0)

        # 類內散佈矩陣 Sw = S0 + S1
        s0 = np.dot((class0 - self.m0).T, (class0 - self.m0))
        s1 = np.dot((class1 - self.m1).T, (class1 - self.m1))
        self.sw = s0 + s1

        # 類間散佈矩陣 Sb = (m1 - m0)(m1 - m0)^T
        mean_diff = (self.m1 - self.m0).reshape(-1, 1)
        self.sb = np.dot(mean_diff, mean_diff.T)

        # 投影方向 w = Sw^{-1} * (m1 - m0)
        self.w = np.linalg.inv(self.sw).dot(self.m1 - self.m0)

        # 計算斜率（用於畫圖）
        if len(self.w) == 2 and self.w[0] != 0:
            self.slope = self.w[1] / self.w[0]
        else:
            self.slope = None

    def predict(self, inputs: npt.NDArray[np.float64],) -> np.ndarray:
        """Project samples and classify based on proximity to projected class means."""
        # 投影到 w 上
        projected = inputs @ self.w
        mean0_proj = self.m0 @ self.w
        mean1_proj = self.m1 @ self.w

        # 根據距離哪個平均近決定分類
        preds = np.where(
            np.abs(projected - mean0_proj) < np.abs(projected - mean1_proj),
            0,
            1,
        )
        return preds

    def plot_projection(
        self,
        inputs: npt.NDArray[np.float64],
        targets: t.Sequence[int],
        preds: t.Optional[t.Sequence[int]] = None,
    ) -> None:
        """Plot the projection line, decision boundary, and colorized points."""
        if preds is None:
            preds = self.predict(inputs)

        plt.figure(figsize=(6, 6))

        # 投影線
        x_vals = np.linspace(inputs[:, 0].min(), inputs[:, 0].max(), 100)
        if self.slope is not None:
            y_vals = self.slope * (x_vals - self.m0[0]) + self.m0[1]
            plt.plot(x_vals, y_vals, color="gray", label="Projection line")

        # 投影線段 & 資料點（有顏色與 marker）
        w_unit = self.w / np.linalg.norm(self.w)  # 單位向量 w
        correct = np.array(preds) == np.array(targets)
        for i in range(len(inputs)):
            color = "green" if correct[i] else "red"
            marker = "o" if targets[i] == 0 else "^"
            xi = inputs[i]
            vec = xi - self.m0
            scalar_proj = np.dot(vec, w_unit)
            proj = self.m0 + scalar_proj * w_unit
            # 投影線段
            plt.plot([xi[0], proj[0]], [xi[1], proj[1]], color="gray", alpha=0.3)
            # 原始點
            plt.scatter(xi[0], xi[1], c=color, marker=marker, edgecolor="black")
            # 投影點
            plt.scatter(proj[0], proj[1], c="gray", s=10, zorder=3, edgecolor="black")

        # Decision boundary
        mean0_proj = self.m0 @ self.w
        mean1_proj = self.m1 @ self.w
        mid_proj = (mean0_proj + mean1_proj) / 2
        # 找到該中點對應的空間座標
        mid_pt = mid_proj * self.w / np.linalg.norm(self.w)**2
        x_range = plt.xlim()
        y_range = plt.ylim()
        x_len = x_range[1] - x_range[0]
        y_len = y_range[1] - y_range[0]
        line_length = 0.7 * min(x_len, y_len)
        # 找垂直於 w 的單位向量
        perp = np.array([-self.w[1], self.w[0]]) / np.linalg.norm(self.w)
        start = mid_pt - perp * line_length
        end = mid_pt + perp * line_length
        plt.plot([start[0], end[0]], [start[1], end[1]], color="blue", linestyle="--", label="Decision boundary")

        w_str = np.array2string(self.w, precision=3, separator=',')
        intercept = self.m0[1] - self.slope * self.m0[0] if self.slope is not None else None
        plt.title(f"Projection onto FLD axis (w={w_str})\nSlope={self.slope:.3f}, Intercept={intercept:.3f}")
        plt.axis("equal")
        plt.savefig("fld_projection.png")
        plt.close()


def compute_auc(y_trues, y_preds):
    return roc_auc_score(y_trues, y_preds)


def accuracy_score(y_trues, y_preds):
    y_trues = np.array(y_trues)
    y_preds = np.array(y_preds)
    return np.mean(y_trues == y_preds)


def main():
    # Read data
    train_df = pd.read_csv('./train.csv')
    test_df = pd.read_csv('./test.csv')

    # Part1: Logistic Regression
    x_train = train_df.drop(['target'], axis=1).to_numpy()  # (n_samples, n_features)
    y_train = train_df['target'].to_numpy()  # (n_samples, )

    x_test = test_df.drop(['target'], axis=1).to_numpy()
    y_test = test_df['target'].to_numpy()

    LR = LogisticRegression(
        learning_rate=1e-2,  # You can modify the parameters as you want
        num_iterations=25001,  # You can modify the parameters as you want
    )
    LR.fit(x_train, y_train)
    y_pred_probs, y_pred_classes = LR.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred_classes)
    auc_score = compute_auc(y_test, y_pred_probs)
    logger.info(f'LR: Weights: {LR.weights[:5]}, Intercep: {LR.intercept}')
    logger.info(f'LR: Accuracy={accuracy:.4f}, AUC={auc_score:.4f}')

    # Part2: FLD
    cols = ['27', '30']  # Dont modify
    x_train = train_df[cols].to_numpy()
    y_train = train_df['target'].to_numpy()
    x_test = test_df[cols].to_numpy()
    y_test = test_df['target'].to_numpy()

    FLD_ = FLD()
    """
    (TODO): Implement your code to
    1) Fit the FLD model
    2) Make prediction
    3) Compute the evaluation metrics

    Please also take care of the variables you used.
    """
    FLD_.fit(x_train, y_train)
    fld_preds = FLD_.predict(x_test)
    fld_acc = accuracy_score(y_test, fld_preds)

    logger.info(f'FLD: m0={FLD_.m0}, m1={FLD_.m1} of {cols=}')
    logger.info(f'FLD: \nSw=\n{FLD_.sw}')
    logger.info(f'FLD: \nSb=\n{FLD_.sb}')
    logger.info(f'FLD: \nw=\n{FLD_.w}')
    logger.info(f'FLD: Accuracy={fld_acc:.4f}')

    """
    (TODO): Implement your code below to plot the projection
    """
    FLD_.plot_projection(x_test, y_test, fld_preds)


if __name__ == '__main__':
    main()
