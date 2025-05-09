import numpy as np

class BanditEnv:
    def __init__(self, k: int, stationary=True): # (k臂拉霸機, 是否為平穩環境)
        self.k = k
        self.stationary = stationary
        self.reset()

    def reset(self):
        # 重置每個 arm 的真實平均獎勵（mu），並清空歷史記錄
        self.q_true = np.random.normal(loc=0.0, scale=1.0, size=self.k) # q_true[a] 真實期望 reward，給定選擇動作 a
        self.action_history = []
        self.reward_history = []

    def step(self, action: int) -> float:
        # 防呆 避免選一個不存在的臂
        assert 0 <= action < self.k, f"Invalid action {action}, must be in [0, {self.k - 1}]"
        
        # 若為 non-stationary 環境，進行random walk
        if not self.stationary:
            self.q_true += np.random.normal(loc=0.0, scale=0.01, size=self.k)
        
        # 根據 q_true[action] + N(0, 1) 產生 reward
        reward = np.random.normal(loc=self.q_true[action], scale=1.0)
        
        # 記錄歷史
        self.action_history.append(action)
        self.reward_history.append(reward)

        return reward

    def export_history(self):
        return self.action_history, self.reward_history
