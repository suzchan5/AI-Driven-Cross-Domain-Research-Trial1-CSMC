import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# 共通パラメータ設定 (Human Scale: 30 minutes)
# ---------------------------------------------------------
dt = 0.01                # Time step (10ms)
T_total = 1800.0         # 全期間 30分 = 1800秒
steps = int(T_total / dt)
time = np.linspace(0, T_total, steps)
target_r = 1.0

# 外乱生成関数
def generate_disturbance(t_array):
    d = np.zeros_like(t_array)
    # 定常的な緊張感 (周期150秒程度のゆったりした波)
    d = 0.5 * np.sin(2 * np.pi * (1/150) * t_array)
    # パニックパルス: 開始12分(720s)〜14分(840s)の2分間
    panic_mask = (t_array >= 720.0) & (t_array <= 840.0)
    d[panic_mask] -= 4.0
    return d

# シミュレーション実行関数
def run_simulation(phase_name, K_gain, phi, use_tanh=True, use_delay=False):
    x = np.zeros(steps)
    u = np.zeros(steps)
    d = generate_disturbance(time)
    x[0] = 0.05
    
    # Plant Params
    v_drift = 0.05
    sigma = 0.05
    
    for t in range(steps - 1):
        error = x[t] - target_r
        
        # Phase 1: 遅延あり
        if use_delay and t > 10:
             # 100ms (10 steps) delay
             s = x[t-10] - target_r
        else:
             s = error

        # Control Law
        if not use_tanh:
            # Phase 1 & 3 (Sgn/Saturation like)
            # Phase 1は純粋なSgnだと計算不能になるので、非常に急峻なTanhで近似
            u[t] = -K_gain * np.tanh(s / 0.001) 
        else:
            # Phase 2 & 4 (Tanh)
            if phi > 0:
                u[t] = -K_gain * np.tanh(s / phi)
            else:
                u[t] = -K_gain * np.sign(s) # Fallback

        noise = sigma * np.random.normal(0, np.sqrt(dt))
        dx = (v_drift + u[t] + d[t]) * dt + noise
        x[t+1] = x[t] + dx

    # 遵守率
    within_band = (x >= 0.8) & (x <= 1.2)
    compliance = np.mean(within_band) * 100
    
    # 描画と保存
    plt.figure(figsize=(12, 6))
    plt.plot(time, x, label=f"Result (Compliance: {compliance:.1f}%)", color='blue')
    plt.axhline(y=target_r, color='black', linestyle='--', label="Target")
    plt.fill_between(time, 0.8, 1.2, color='green', alpha=0.1, label="Allowed Band")
    # パニック領域の明示
    plt.axvspan(720, 840, color='red', alpha=0.05, label="Panic Pulse")
    
    plt.title(f"Phase {phase_name}: {compliance:.1f}% Compliance (30min Scale)")
    plt.xlabel("Time [s]")
    plt.ylabel("Recall Level")
    plt.ylim(0, 1.5)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    filename = f"ResearchProject_Trial1/docs/images/phase{phase_name}_30min.png"
    plt.savefig(filename)
    plt.close()
    print(f"Saved {filename}")

# --- 実行 ---
os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)

# Phase 1: Divergence (Delay + High Gain) -> DelayなしでもGain過多で発散気味にする
# Delayを入れるとEuler法では即発散して描画できないため、「不適切な高ゲイン＋不連続」で代用
run_simulation("1", K_gain=15.0, phi=0.001, use_tanh=False) 

# Phase 2: Weak Gain (Smooth but Fail)
run_simulation("2", K_gain=0.5, phi=1.0, use_tanh=True)

# Phase 3: Chattering (High Gain + Narrow Boundary)
run_simulation("3", K_gain=10.0, phi=0.05, use_tanh=True)

# Phase 4: Optimized
run_simulation("4", K_gain=3.0, phi=0.3, use_tanh=True)
