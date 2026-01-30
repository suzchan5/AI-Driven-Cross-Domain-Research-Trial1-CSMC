import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# 1. OU Simulation Engine
# ---------------------------------------------------------
dt = 0.01

def run_ou_simulation(
    duration_minutes, 
    label, 
    color, 
    theta,            # Recovery Rate (1/Tau)
    K_gain=0.0, 
    phi=0.0, 
    use_control=False,
    use_delay=False,      # Phase 1
    use_chattering=False, # Phase 3 (Narrow boundary + High Gain)
    pulse_strength=-4.0,
    filename=""
):
    # Time Setup
    T_total = duration_minutes * 60.0
    steps = int(T_total / dt)
    time = np.linspace(0, T_total, steps)
    
    # State Vars
    x = np.zeros(steps)
    u = np.zeros(steps)
    x[0] = 1.0 
    mu = 1.0 # Baseline
    
    # Pulse Timing (Fixed for comparison: 12m-14m, i.e., 20% point for 30m, but let's fix relative to duration)
    # 論文の記述に合わせて 30分スケールの場合 12m-14m (720s-840s)
    # 6分スケールの場合 2.4m-2.8m (144s-168s) -> これだと比較しにくいので
    # 予備実験比較用には「実時間」で合わせるが、Phase 1-4は「30分スケール」で統一して実行する。
    
    pulse_start = 720.0
    pulse_end = 840.0
    
    # 予備実験で6分スケールでやる場合、範囲外になるが、
    # 今回はPhase 1-4は全て「30分スケール High Sensitivity」で統一するため問題なし。
    # 予備実験の6分スケール(High Sensitivity)も、横軸を30分取って「途中で終わる」のではなく
    # 「30分生きた時のHigh Sensitivity挙動」を見るべき。
    # つまり、High Sensitivity Parameter (Theta=1.0) で 30分回せば良い。
    
    for t in range(steps - 1):
        # 1. Disturbance
        d = 0.5 * np.sin(2 * np.pi * (1/150) * time[t]) # Slow wave
        if pulse_start <= time[t] <= pulse_end:
            d += pulse_strength
            
        # 2. Control Input
        control_val = 0.0
        if use_control:
            curr_x = x[t]
            if use_delay and t > 100: # 1s delay
                 curr_x = x[t-100]
            
            error = curr_x - mu
            s = error
            
            if use_chattering: # Phase 3: Sign like behavior
                 # Tanh with very steep slope
                 control_val = -K_gain * np.tanh(s / 0.01)
            elif phi > 0:
                 control_val = -K_gain * np.tanh(s / phi)
            else:
                 control_val = 0.0 # Phase 2 (Gain too low) -> handled by K_gain
            
        u[t] = control_val

        # 3. Dynamics (OU Process)
        # dx = theta*(mu - x)*dt + (u + d)*dt + sigma*dW
        noise = 0.05 * np.random.normal(0, np.sqrt(dt))
        
        dx = theta * (mu - x[t]) * dt + (u[t] + d) * dt + noise
        x[t+1] = x[t] + dx

    # 4. Plot and Save
    plt.figure(figsize=(10, 6))
    plt.plot(time, x, label=label, color=color, linewidth=2)
    plt.axhline(y=1.0, color='black', linestyle='--', label="Target")
    plt.fill_between(time, 0.8, 1.2, color='green', alpha=0.1, label="Allowed Band")
    
    # Show Pulse Area
    plt.axvspan(pulse_start, pulse_end, color='red', alpha=0.05, label="Panic Pulse")

    plt.ylim(-0.2, 1.6)
    plt.xlim(0, T_total)
    plt.title(f"{label} (Time Scale: {duration_minutes} min)")
    plt.xlabel("Time [s]")
    plt.ylabel("Recall Level")
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    if filename:
        plt.savefig(filename)
        print(f"Saved {filename}")
        plt.close()
    
    # Calculate Compliance
    within_band = (x >= 0.8) & (x <= 1.2)
    return np.mean(within_band) * 100

# ---------------------------------------------------------
# 2. Execution Sequence
# ---------------------------------------------------------
os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)

# A. Pre-Experiment (Fig 0): High vs Low Sensitivity (Control OFF)
# High Sensitivity (Theta=1.0): 復元力あるが、外乱に負けて大きく振れる
# Low Sensitivity (Theta=0.2): 復元力弱い(変化遅い)が、外乱に対しても変化遅い -> 式変形必要
# OUモデルで「外乱感度」を変えるには、dx = theta*(mu-x) + k_d * d ... と係数を分けるべきだが
# ここでは簡易的に Theta を変えることとする。
# Thetaが大きい＝復元早い＝時定数短い＝High Sensitivity
# Thetaが小さい＝復元遅い＝時定数長い＝Low Sensitivity

plt.figure(figsize=(10, 6))

# Low Sensitivity (Blue)
x_low = run_ou_simulation(30, "Low Sensitivity (Tau=Large)", "blue", theta=0.1, use_control=False)["x"] if False else None # Dummy call structure
# ... 上記関数だとPlotしてしまうので、再実装
T_total = 1800.0
steps = int(T_total/dt)
time = np.linspace(0, T_total, steps)

# --- Manual Plot for Fig 0 Combined ---
def get_ou_trace(theta, d_scale=1.0):
    x = np.zeros(steps)
    x[0] = 1.0
    mu = 1.0
    for t in range(steps-1):
        d = 0.5 * np.sin(2*np.pi*(1/150)*time[t])
        if 720 <= time[t] <= 840: d -= 4.0
        
        noise = 0.05 * np.random.normal(0, np.sqrt(dt))
        # Important: Sensitivity to disturbance.
        # High Sensitivity: d affects x directly magnitude 1.0
        # Low Sensitivity: d affects x with magnitude 0.2 (Inertia)
        dx = theta*(mu - x[t])*dt + (d * d_scale)*dt + noise
        x[t+1] = x[t] + dx
    return x

x_low = get_ou_trace(theta=0.5, d_scale=0.2) # Low impact
x_high = get_ou_trace(theta=0.5, d_scale=1.0) # High impact

plt.figure(figsize=(10, 6))
plt.plot(time, x_low, label="Low Sensitivity (Stable)", color="blue")
plt.plot(time, x_high, label="High Sensitivity (Vulnerable)", color="red")
plt.axhline(y=1.0, color='black', linestyle='--')
plt.fill_between(time, 0.8, 1.2, color='green', alpha=0.1)
plt.axvspan(720, 840, color='red', alpha=0.05)
plt.title("Fig. 0: Stress Response without AI Support (OU Model)")
plt.xlabel("Time [s]")
plt.ylabel("Recall Level")
plt.ylim(-0.5, 1.5)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("ResearchProject_Trial1/docs/images/personality_comparison.png")
print("Saved Fig 0")

# B. Phase 1-4 Experiments (High Sensitivity, 30 min)
# すべて High Sensitivity (d_scale=1.0, theta=0.5) に対して制御を行う
base_theta = 0.5

# Phase 1: Divergence (Delay 1s, High Gain)
run_ou_simulation(30, "Phase 1: Delay Divergence", "red", theta=base_theta, K_gain=8.0, phi=0.01, use_control=True, use_delay=True, filename="ResearchProject_Trial1/docs/images/phase1_30min.png")

# Phase 2: Smooth but Weak (Low Gain)
run_ou_simulation(30, "Phase 2: Weak Gain", "orange", theta=base_theta, K_gain=1.0, phi=1.0, use_control=True, filename="ResearchProject_Trial1/docs/images/phase2_30min.png")

# Phase 3: Chattering (High Gain, Narrow Phi)
run_ou_simulation(30, "Phase 3: Chattering", "purple", theta=base_theta, K_gain=10.0, phi=0.01, use_control=True, use_chattering=True, filename="ResearchProject_Trial1/docs/images/phase3_30min.png")

# Phase 4: Optimized
# C-SMC should cancel disturbance d=-4.0. Need K > 4.0.
# Let K=5.0, Phi=0.3
comp = run_ou_simulation(30, "Phase 4: Optimized C-SMC", "blue", theta=base_theta, K_gain=5.0, phi=0.3, use_control=True, filename="ResearchProject_Trial1/docs/images/phase4_30min.png")
print(f"Phase 4 Compliance: {comp:.2f}%")
