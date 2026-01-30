import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. パラメータ設定
# ---------------------------------------------------------
dt = 0.01           # 時間分解能 (10msに緩和)
T_total = 360.0     # 全シミュレーション時間 (6分間 = 360秒)
steps = int(T_total / dt)

# 制御対象 (DDMプラント) パラメータ
v_drift = 0.05      # 想起能力 (時間スケールに合わせて調整)
sigma = 0.05        # ノイズも少しマイルドに

# C-SMC 制御パラメータ (Phase 4 最適化値 - 最終版)
K_gain = 3.0        # ゲインをスケーリング (30 -> 3: 時間が伸びた分、小さな力で済む)
phi = 0.3           # 境界層幅 (そのまま)
target_r = 1.0      # 目標想起レベル

# ---------------------------------------------------------
# 2. 変数初期化
# ---------------------------------------------------------
x = np.zeros(steps)     # 想起レベル x(t)
u = np.zeros(steps)     # 制御入力 u(t)
d = np.zeros(steps)     # 外乱 d(t)
time = np.linspace(0, T_total, steps)

# 初期状態
x[0] = 0.05

# ---------------------------------------------------------
# 3. シミュレーションループ
# ---------------------------------------------------------
for t in range(steps - 1):
    # --- 外乱の設定 (地獄の商談モデル - スローペース版) ---
    # 定常的な緊張感 (ゆったりとした波: 周期30秒程度)
    d[t] = 0.5 * np.sin(2 * np.pi * (1/30) * time[t]) 
    
    # 突発的パニックパルス (2.5分〜3分付近: 150s - 170s)
    if 150.0 <= time[t] <= 170.0:
        d[t] -= 4.0 # パルス強度もスケーリング (-40 -> -4)

    # --- C-SMC 制御則の計算 ---
    error = x[t] - target_r
    
    # 切換面 s の定義 (微分項を排除し、単純な誤差フィードバックへ)
    s = error
    
    # 境界層を導入した tanh 制御入力
    u[t] = -K_gain * np.tanh(s / phi)
    
    # --- 状態更新 (DDM 確率微分方程式の Euler-Maruyama 近似) ---
    noise = sigma * np.random.normal(0, np.sqrt(dt))
    # システム方程式: dx/dt = v_drift + u + d
    dx = (v_drift + u[t] + d[t]) * dt + noise
    x[t+1] = x[t] + dx

# ---------------------------------------------------------
# 4. 遵守率 (Compliance Rate) の計算
# ---------------------------------------------------------
# 許容バンド [0.8, 1.2] 内に滞在した時間の割合
within_band = (x >= 0.8) & (x <= 1.2)
compliance_rate = np.mean(within_band) * 100

print(f"Final Compliance Rate: {compliance_rate:.2f}%")

# ---------------------------------------------------------
# 5. 可視化
# ---------------------------------------------------------
plt.figure(figsize=(12, 6))
plt.plot(time, x, label=f"C-SMC (Compliance: {compliance_rate:.1f}%)", color='blue')
# plt.plot(time, d/10 + 1.0, label="Disturbance (scaled)", color='red', alpha=0.3) # 外乱の可視化オプション
plt.axhline(y=target_r, color='black', linestyle='--', label="Target r = 1.0")
plt.fill_between(time, 0.8, 1.2, color='green', alpha=0.1, label="Allowed Band [0.8, 1.2]")

plt.title("Memory Retrieval Stability: Final C-SMC Optimization")
plt.xlabel("Time [s]")
plt.ylabel("Recall Level x(t)")
plt.ylim(0, 1.5)
plt.legend(loc='lower right')
plt.grid(True, which='both', linestyle='--', alpha=0.5)

# 保存
plt.savefig("simulation_result.png")
print("Simulation result saved as simulation_result.png")
