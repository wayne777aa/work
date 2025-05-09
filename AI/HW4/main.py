import numpy as np
import matplotlib.pyplot as plt
from BanditEnv import BanditEnv
from Agent import Agent

def run_experiment(epsilon, runs=2000, steps=10000, Stationary=False, Step_size=0.1): # 變數: epsilon, runs 執行次數, steps 幾步
    k = 10                                                                            #      Stationary 是否為平穩環境, Step_size = alpha
    rewards = np.zeros((runs, steps))
    optimal_actions = np.zeros((runs, steps))

    for run in range(runs):
        env = BanditEnv(k, stationary=Stationary)
        agent = Agent(k, epsilon, step_size=Step_size)

        for step in range(steps):
            action = agent.select_action()
            reward = env.step(action)
            agent.update_q(action, reward)

            rewards[run, step] = reward
            if action == np.argmax(env.q_true):
                optimal_actions[run, step] = 1

    avg_rewards = rewards.mean(axis=0) # avg_rewards[t]：第 t 步的 reward 平均值（所有 run）
    optimal_action_rate = optimal_actions.mean(axis=0)

    return avg_rewards, optimal_action_rate


epsilons = [0, 0.01, 0.1]
results = {}

for eps in epsilons:
    rewards, optimal_rate = run_experiment(eps)
    results[eps] = (rewards, optimal_rate)

# Plot 平均獎勵
plt.figure(figsize=(12, 5))
for eps in epsilons:
    plt.plot(results[eps][0], label=f"ε = {eps}")
plt.title("Average Reward over Time")
plt.xlabel("Steps")
plt.ylabel("Average Reward")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("reward_plot.png")

# Plot 最佳動作選擇率
plt.figure(figsize=(12, 5))
for eps in epsilons:
    plt.plot(results[eps][1], label=f"ε = {eps}")
plt.title("Optimal Action Selection Rate")
plt.xlabel("Steps")
plt.ylabel("Optimal Action %")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("optimal_action_plot.png")
