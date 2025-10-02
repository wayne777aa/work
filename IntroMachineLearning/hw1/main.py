"""
1. Complete the implementation for the `...` part
2. Feel free to take strategies to make faster convergence
3. You can add additional params to the Class/Function as you need. But the key print out should be kept.
4. Traps in the code. Fix common semantic/stylistic problems to pass the linting
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger


class LinearRegressionBase:
    def __init__(self):
        self.weights = None
        self.intercept = None

    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError


class LinearRegressionCloseform(LinearRegressionBase):
    def fit(self, X, y):
        """Question1
        Complete this function
        """
        # 加 bias term (一欄 1) //np.c_: column-wise concatenation
        x_bias = np.c_[np.ones((X.shape[0], 1)), X]

        # Closed-form solution: beta_hat = (X^T X)^(-1) X^T y
        beta_hat = np.linalg.inv(x_bias.T @ x_bias) @ x_bias.T @ y

        self.intercept = beta_hat[0]
        self.weights = beta_hat[1:]

    def predict(self, X):
        """Question4
        Complete this function
        """
        return X @ self.weights + self.intercept


class LinearRegressionGradientdescent:
    def fit(
        self,
        X,
        y,
        learning_rate: float = 1e-3,
        epochs: int = 1000
    ):
        """Question2
        Complete this function
        """
        n_samples, n_features = X.shape  # # of row, # of column
        y = y.flatten()  # change the shape to (n,)
        self.weights = np.zeros(n_features)
        self.intercept = -35
        losses, lr_history = [], []
        for epoch in range(epochs):
            y_predict = self.predict(X)

            dm = -(2 / n_samples) * X.T @ (y - y_predict)  # slope m
            db = -(2 / n_samples) * np.sum(y - y_predict)  # intercept b

            self.weights -= learning_rate * dm
            self.intercept -= learning_rate * db

            loss = compute_mse(y_predict, y)
            losses.append(loss)
            lr_history.append(learning_rate)

            if epoch % 10000 == 0:
                logger.info(f'EPOCH {epoch}, {loss=:.4f}, {learning_rate=:.4f}')
        return losses, lr_history

    def predict(self, X):
        """Question4
        Complete this
        """
        return X @ self.weights + self.intercept


def compute_mse(prediction, ground_truth):
    mse = np.mean((prediction - ground_truth) ** 2)
    return mse


def main():
    train_df = pd.read_csv('./train.csv')  # Load training data
    test_df = pd.read_csv('./test.csv')  # Load test data
    train_x = train_df.drop(["Performance Index"], axis=1).to_numpy()
    train_y = train_df["Performance Index"].to_numpy()
    test_x = test_df.drop(["Performance Index"], axis=1).to_numpy()
    test_y = test_df["Performance Index"].to_numpy()

    LR_CF = LinearRegressionCloseform()
    LR_CF.fit(train_x, train_y)

    """This is the print out of question1"""
    logger.info(f'{LR_CF.weights=}, {LR_CF.intercept=:.4f}')

    LR_GD = LinearRegressionGradientdescent()
    losses, lr_history = LR_GD.fit(train_x, train_y, learning_rate=1e-4, epochs=50000)

    """
    This is the print out of question2
    Note: You need to screenshot your hyper-parameters as well.
    """
    logger.info(f'{LR_GD.weights=}, {LR_GD.intercept=:.4f}')
    """
    Question3: Plot the learning curve.
    Implement here
    """
    plt.plot(losses, color="blue", label="Train MSE loss")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.title("Training loss")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("learning_curve.png")
    plt.close()

    """Question4"""
    y_preds_cf = LR_CF.predict(test_x)
    y_preds_gd = LR_GD.predict(test_x)
    y_preds_diff = np.abs(y_preds_gd - y_preds_cf).mean()
    logger.info(f'Prediction difference: {y_preds_diff:.4f}')

    mse_cf = compute_mse(y_preds_cf, test_y)
    mse_gd = compute_mse(y_preds_gd, test_y)
    diff = (np.abs(mse_gd - mse_cf) / mse_cf) * 100
    logger.info(f'{mse_cf=:.4f}, {mse_gd=:.4f}. Difference: {diff:.3f}%')


if __name__ == '__main__':
    main()
