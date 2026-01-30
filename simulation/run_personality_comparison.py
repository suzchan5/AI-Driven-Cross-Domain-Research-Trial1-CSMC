import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# 共通設定
# ---------------------------------------------------------
dt = 0.01

def run_open_loop_simulation(duration_minutes, label, color, time_constant_factor):
    # 秒単位
    T_total = duration_minutes * 60.0
    steps = int(T_total / dt)
    time = np.linspace(0, T_total, steps)
    
    x = np.zeros(steps)
    x[0] = 1.0 # 初期値
    
    # ドリフト項（復元力）
    # High (tau=1) は復元力が弱く、Low (tau=5) は復元力が相対的に強いというよりは、
    # 外乱に対する感度が低い。
    # ここでは簡易的に、入力全般に対するゲインを time_constant_factor で割ることで表現
    
    v_drift = -0.05 
    pulse_strength = -4.0 # 5章と同じ強烈なパルス (-40 -> -4 スケール)
    
    # パルス発生タイミング: 両者比較のため 150s - 250s (100秒間) に固定
    pulse_start_t = 150.0
    pulse_end_t = 250.0
    
    for t in range(steps - 1):
        d = 0.0
        # パルス外乱
        if pulse_start_t <= time[t] <= pulse_end_t:
            d = pulse_strength
        
        # 緩やかな定常外乱も入れておく
        d += 0.5 * np.sin(2 * np.pi * (1/30) * time[t]) 

        # ダイナミクス:
        # dx = (1/tau) * (u + d + drift) * dt
        # tauが大きいほど、変化量 dx は小さくなる
        
        noise = 0.05 * np.random.normal(0, np.sqrt(dt))
        
        # Open Loopなので u = 0
        total_force = (v_drift + d) 
        dx = (1.0 / time_constant_factor) * total_force * dt + noise
        
        x[t+1] = x[t] + dx

    # 実時間プロット
    plt.plot(time, x, label=f"{label} (tau={time_constant_factor})", color=color, linewidth=2)
    return x

# ---------------------------------------------------------
# 実行と保存
# ---------------------------------------------------------
os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)
plt.figure(figsize=(10, 6))

# Case B: Low Sensitivity (30 min scale) -> Tau = 5.0 (鈍感、慣性大)
# 1800秒までシミュレーション
x_long = run_open_loop_simulation(30.0, "Low Sensitivity", "blue", time_constant_factor=5.0)

# Case A: High Sensitivity (6 min scale) -> Tau = 1.0 (敏感、慣性小)
# 360秒までシミュレーション
x_short = run_open_loop_simulation(6.0, "High Sensitivity", "red", time_constant_factor=1.0)

plt.axhline(y=1.0, color='black', linestyle='--', label="Target Level (1.0)")
plt.axhline(y=0.0, color='black', linestyle=':', label="Breakdown (0.0)")
plt.fill_between(np.linspace(0, 1800, 100), 0.8, 1.2, color='green', alpha=0.1, label="Allowed Band")

plt.ylim(-0.5, 1.5) # 0以下も見せる
plt.xlim(0, 1800)

plt.title("Fig. 0: Stress Response Comparison (No AI Support)")
plt.xlabel("Time [s]")
plt.ylabel("Recall Level")
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)

filename = "ResearchProject_Trial1/docs/images/personality_comparison.png"
plt.savefig(filename)
print(f"Saved {filename}")
