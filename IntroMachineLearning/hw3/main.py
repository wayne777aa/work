import numpy as np
import pandas as pd
from loguru import logger
import random
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

import torch
from src import AdaBoostClassifier, BaggingClassifier, DecisionTree
from src.utils import plot_learners_roc


def preprocess(X_train_df, X_test_df):
    """
    自動 one-hot categorical features + 標準化 numeric features
    並回傳 one-hot 展開後的所有 feature names
    """
    # --- 1. 找出 categorical columns ---
    categorical_cols = X_train_df.select_dtypes(include=['object']).columns
    numeric_cols = X_train_df.select_dtypes(exclude=['object']).columns

    # --- 2. one-hot encoding ---
    X_train_cat = pd.get_dummies(X_train_df[categorical_cols], drop_first=False)
    X_test_cat = pd.get_dummies(X_test_df[categorical_cols], drop_first=False)

    # 確保兩邊 one-hot 後欄位對齊
    X_train_cat, X_test_cat = X_train_cat.align(X_test_cat, join='left', axis=1, fill_value=0)

    cat_feature_names = list(X_train_cat.columns)

    # --- 3. numeric 部分取值 ---
    X_train_num = X_train_df[numeric_cols].astype(float)
    X_test_num = X_test_df[numeric_cols].astype(float)

    num_feature_names = list(numeric_cols)

    # --- 4. 標準化 numeric ---
    mean = X_train_num.mean(axis=0)
    std = X_train_num.std(axis=0) + 1e-12

    X_train_num = (X_train_num - mean) / std
    X_test_num = (X_test_num - mean) / std

    # --- 5. 合併 numeric + categorical ---
    X_train = np.hstack([X_train_num.values, X_train_cat.values])
    X_test = np.hstack([X_test_num.values, X_test_cat.values])

    # ---- return feature names ----
    feature_names = num_feature_names + cat_feature_names

    return X_train, X_test, feature_names


def plot_importance(importance, feature_names, title, fpath):
    plt.figure(figsize=(8, 5))
    idx = np.argsort(importance)[::-1]
    plt.barh(range(len(idx)), importance[idx])
    plt.yticks(range(len(idx)), np.array(feature_names)[idx])
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(fpath, dpi=300)
    plt.close()


def main():
    """You can control the seed for reproducibility"""
    random.seed(777)
    torch.manual_seed(777)
    np.random.seed(777)

    train_df = pd.read_csv('./train.csv')
    test_df = pd.read_csv('./test.csv')

    X_train_df = train_df.drop(['target'], axis=1)
    y_train = train_df['target'].to_numpy().astype(int)  # (n_samples, )

    X_test_df = test_df.drop(['target'], axis=1)
    y_test = test_df['target'].to_numpy().astype(int)

    """
    TODO: Implement you preprocessing function.
    """
    X_train, X_test, feature_names = preprocess(X_train_df, X_test_df)
    input_dim = X_train.shape[1]

    logger.info("Preprocessing done.")

    """
    TODO: Implement your ensemble methods.
    1. You can modify the hyperparameters as you need.
    2. You must print out logs (e.g., accuracy) with loguru.
    """
    # AdaBoost
    clf_adaboost = AdaBoostClassifier(input_dim=input_dim, num_learners=10)
    clf_adaboost.fit(X_train, y_train, num_epochs=200, learning_rate=0.01)

    y_pred_classes, y_pred_probs = clf_adaboost.predict_learners(X_test)

    # 最終 ensemble 預測：sign(Σ α_t h_t(x))
    final_scores = np.zeros(len(y_test))
    for alpha_t, pred in zip(clf_adaboost.alphas, y_pred_classes):
        # pred ∈ {0,1} → 轉為 {-1,+1}
        pred_signed = np.where(pred == 1, 1, -1)
        final_scores += alpha_t * pred_signed

    final_pred = (final_scores >= 0).astype(int)
    accuracy_ = accuracy_score(y_test, final_pred)
    logger.info(f'AdaBoost - Accuracy: {accuracy_:.4f}')

    plot_learners_roc(
        y_preds=y_pred_probs,
        y_trues=y_test,
        fpath='./adaboost_roc.png'
    )
    feature_importance = clf_adaboost.compute_feature_importance()
    plot_importance(feature_importance, feature_names, "AdaBoost Feature Importance", "./adaboost_importance.png")

    # Bagging
    clf_bagging = BaggingClassifier(input_dim=input_dim)
    clf_bagging.fit(X_train, y_train, num_epochs=200, learning_rate=0.01)

    y_pred_classes, y_pred_probs = clf_bagging.predict_learners(X_test)

    # voting
    all_preds = np.array(y_pred_classes)  # shape = (10, N)
    final_pred = (all_preds.mean(axis=0) >= 0.5).astype(int)
    accuracy_ = accuracy_score(y_test, final_pred)
    logger.info(f'Bagging - Accuracy: {accuracy_:.4f}')

    plot_learners_roc(
        y_preds=y_pred_probs,
        y_trues=y_test,
        fpath='./bagging_roc.png'
    )
    feature_importance = clf_bagging.compute_feature_importance()
    plot_importance(feature_importance, feature_names, "Bagging Feature Importance", "./bagging_importance.png")

    # Decision Tree
    clf_tree = DecisionTree(max_depth=7)
    clf_tree.fit(X_train, y_train)
    y_pred_classes = clf_tree.predict(X_test)
    accuracy_ = accuracy_score(y_test, y_pred_classes)
    logger.info(f'DecisionTree - Accuracy: {accuracy_:.4f}')

    # feature importance (tree-based)
    feature_importance = clf_tree.compute_feature_importance()
    plot_importance(feature_importance, feature_names, "Decision Tree Feature Importance", "./tree_importance.png")


if __name__ == '__main__':
    main()
