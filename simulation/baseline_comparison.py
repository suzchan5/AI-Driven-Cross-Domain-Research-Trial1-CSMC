"""
Strategy 2: Baseline Comparison

This script compares C-SMC against standard control methods:
1. No Control (baseline)
2. Simple PID Control
3. Rule-based Intervention
4. Proposed C-SMC

Outputs a comparison table showing success rate, avg error, and chattering.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

# Simulation parameters
T = 1800  # 30 minutes
dt = 0.01
t = np.arange(0, T, dt)
n_trials = 100  # Monte Carlo

# System parameters (Double-Well)
a = 2.0
b = 1.0
sigma = 0.3
r = 1.0  # Target state

# Disturbance (Panic pulse at t=720-840s)
def disturbance(t_val):
    if 720 <= t_val <= 840:
        return -2.5
    else:
        return 0.2 * np.sin(2 * np.pi * t_val / 300)

# Controllers
def no_control(x, t_val):
    return 0.0

def pid_control(x, t_val, integral, prev_error, Kp=3.0, Ki=0.1, Kd=0.5):
    """Simple PID controller"""
    error = r - x
    integral += error * dt
    derivative = (error - prev_error) / dt
    u = Kp * error + Ki * integral + Kd * derivative
    return np.clip(u, -10, 10), integral, error

def rule_based_control(x, t_val):
    """Simple threshold-based rule"""
    if x < 0.5:
        return 5.0  # Strong intervention
    elif x < 0.8:
        return 2.0  # Moderate intervention
    else:
        return 0.0  # No intervention

def csmc_control(x, t_val, K=5.0, phi=0.3):
    """Proposed C-SMC"""
    s = x - r
    u = -K * np.tanh(s / phi)
    return u

# Simulation function
def simulate(controller_type, trial_idx=0):
    """
    Run simulation with specified controller.
    
    Returns:
        success: whether state stayed above 0
        avg_error: mean absolute error from target
        chattering: number of rapid input changes
    """
    np.random.seed(trial_idx)
    x = np.ones(len(t))
    u_hist = np.zeros(len(t))
    
    # PID state
    integral = 0.0
    prev_error = 0.0
    
    for i in range(1, len(t)):
        t_val = t[i]
        
        # Control input
        if controller_type == 'none':
            u = no_control(x[i-1], t_val)
        elif controller_type == 'pid':
            u, integral, prev_error = pid_control(x[i-1], t_val, integral, prev_error)
        elif controller_type == 'rule':
            u = rule_based_control(x[i-1], t_val)
        elif controller_type == 'csmc':
            u = csmc_control(x[i-1], t_val)
        
        u_hist[i] = u
        
        # System dynamics
        d = disturbance(t_val)
        drift = a * x[i-1] - b * (x[i-1] ** 3)
        noise = sigma * np.random.randn() * np.sqrt(dt)
        
        x[i] = x[i-1] + (drift + u + d) * dt + noise
        x[i] = np.clip(x[i], -1.5, 1.5)
    
    # Metrics
    success = np.all(x > 0)
    avg_error = np.mean(np.abs(x - r))
    
    # Chattering: count sign changes in control input derivative
    du = np.diff(u_hist)
    chattering = np.sum(np.abs(np.diff(np.sign(du))) > 0)
    
    return success, avg_error, chattering, x, u_hist

# Run experiments
print("=" * 70)
print("Strategy 2: Baseline Comparison")
print("=" * 70)

methods = {
    'No Control': 'none',
    'PID Control': 'pid',
    'Rule-based': 'rule',
    'C-SMC (Proposed)': 'csmc'
}

results = {}

for name, method in methods.items():
    print(f"\nRunning {name}...")
    
    successes = []
    errors = []
    chatterings = []
    
    for trial in range(n_trials):
        success, error, chatter, _, _ = simulate(method, trial)
        successes.append(success)
        errors.append(error)
        chatterings.append(chatter)
    
    success_rate = np.mean(successes) * 100
    avg_error = np.mean(errors)
    avg_chatter = np.mean(chatterings)
    
    results[name] = {
        'success_rate': success_rate,
        'error': avg_error,
        'error_sem': sem(errors),
        'chattering': avg_chatter,
        'chattering_sem': sem(chatterings)
    }
    
    print(f"  Success Rate: {success_rate:.1f}%")
    print(f"  Avg Error: {avg_error:.3f}")
    print(f"  Chattering Events: {avg_chatter:.1f}")

# Generate comparison table
print("\n" + "=" * 70)
print("COMPARISON TABLE")
print("=" * 70)
print(f"{'Method':<20} {'Success Rate (%)':<20} {'Avg Error':<15} {'Chattering':<15}")
print("-" * 70)

for name in methods.keys():
    r = results[name]
    print(f"{name:<20} {r['success_rate']:>18.1f}  {r['error']:>13.3f}  {r['chattering']:>13.1f}")

print("=" * 70)

# Visualize one representative run from each method
fig, axes = plt.subplots(4, 2, figsize=(14, 12))

for idx, (name, method) in enumerate(methods.items()):
    _, _, _, x_traj, u_traj = simulate(method, trial_idx=42)  # Fixed seed for reproducibility
    
    # Plot state
    ax1 = axes[idx, 0]
    ax1.plot(t/60, x_traj, 'b-', linewidth=1.5)
    ax1.axhline(0, color='r', linestyle='--', label='Tipping Point')
    ax1.axhline(r, color='g', linestyle=':', label='Target')
    ax1.fill_between(t/60, -2, 0, alpha=0.1, color='red', label='Panic Zone')
    ax1.set_ylabel('State x(t)')
    ax1.set_title(f'{name}: State Trajectory')
    ax1.legend(loc='lower right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1.5, 1.5)
    
    # Plot control input
    ax2 = axes[idx, 1]
    ax2.plot(t/60, u_traj, 'r-', linewidth=1.0)
    ax2.set_ylabel('Control Input u(t)')
    ax2.set_title(f'{name}: Control Signal')
    ax2.grid(True, alpha=0.3)
    
    if idx == 3:
        ax1.set_xlabel('Time (minutes)')
        ax2.set_xlabel('Time (minutes)')

plt.tight_layout()
plt.savefig('baseline_comparison.png', dpi=150)
print("\nFigure saved: baseline_comparison.png")

# Generate LaTeX table code
print("\n" + "=" * 70)
print("LaTeX Table Code:")
print("=" * 70)
print(r"""
\begin{table}[H]
\centering
\caption{ベースライン手法との定量比較（Monte Carlo n=100）}
\label{tab:baseline}
\small
\begin{tabular}{lccc}
\toprule
手法 & 成功率 (\%) & 平均誤差 & チャタリング回数 \\
\midrule""")

for name in methods.keys():
    r = results[name]
    latex_name = name.replace('C-SMC', r'\textbf{C-SMC}')
    print(f"{latex_name:<25} & {r['success_rate']:>6.1f} & {r['error']:>6.3f} & {r['chattering']:>6.1f} \\\\")

print(r"""\bottomrule
\end{tabular}
\end{table}
""")
print("=" * 70)
