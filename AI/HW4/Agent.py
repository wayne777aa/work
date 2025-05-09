import numpy as np
import random

class Agent:
    def __init__(self, k: int, epsilon: float, step_size: float = None):
        self.k = k
        self.epsilon = epsilon
        self.step_size = step_size
        self.reset()

    def reset(self):
        # Q 值重置為0
        self.q_estimates = np.zeros(self.k)
        # 記錄每個動作被選過幾次
        self.action_counts = np.zeros(self.k, dtype=int)

    def select_action(self) -> int:
        if random.random() < self.epsilon: # 產生0~1的float
            # Exploration：隨機選擇一個動作
            return random.randint(0, self.k - 1)
        else:
            # Exploitation：選擇目前 Q 值最高的動作（若有多個並列會選最小index）
            return int(np.argmax(self.q_estimates))

    def update_q(self, action: int, reward: float):
        self.action_counts[action] += 1
        count = self.action_counts[action]

        if self.step_size is not None: # constant step-size update method: Q_n = Q_n-1 + alpha * (R-Q_n-1)
            alpha = self.step_size
        else: # sample-average method: Q_n = Q_n-1 + (R-Q_n-1)/n
            alpha = 1 / count

        self.q_estimates[action] += alpha * (reward - self.q_estimates[action])
