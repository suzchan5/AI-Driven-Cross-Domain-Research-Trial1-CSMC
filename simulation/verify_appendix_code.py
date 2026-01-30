#!/usr/bin/env python3
"""
C-SMC Appendix Code Verification
Double-Well Potential Model with Monte Carlo Simulation
"""
import numpy as np

# --- 1. Simulation Parameters ---
dt = 0.01           # Time step (10ms)
T_total = 1800.0    # Total duration (30 min)
steps = int(T_total / dt)
n_trials = 100      # Monte Carlo trials

# --- 2. Double-Well Potential Model Parameters ---
a = 1.0             # Potential parameter (bistability)
b = 1.0             # Cubic nonlinearity
sigma = 0.1         # Neural noise standard deviation

# --- 3. C-SMC Controller Parameters ---
K_gain = 5.0        # Control Gain
phi = 0.3           # Boundary Layer (Cognitive Flexibility)
target_r = 1.0      # Target Recall Level

# --- 4. Monte Carlo Simulation ---
print(f"Running {n_trials} Monte Carlo trials...")
print(f"Parameters: K={K_gain}, phi={phi}, sigma={sigma}, a={a}, b={b}")
print(f"Duration: {T_total}s ({T_total/60:.0f} min), dt={dt}s, steps={steps}")
print()

compliance_rates = []

for trial in range(n_trials):
    if (trial + 1) % 20 == 0:
        print(f"  Trial {trial + 1}/{n_trials}...")
    
    x = np.zeros(steps)
    x[0] = 0.9      # Initial state (near healthy)
    time = np.linspace(0, T_total, steps)
    
    for t in range(steps - 1):
        # Disturbance: Steady-state stress + Panic pulse
        d = 0.5 * np.sin(2 * np.pi * (1/150) * time[t])
        if 720 <= time[t] <= 840:  # 12-14 min panic
            d -= 2.5
        
        # C-SMC Controller
        s = x[t] - target_r
        u = -K_gain * np.tanh(s / phi)
        
        # Double-Well Potential Dynamics: dx = (ax - bx³ + u + d)dt + σdW
        noise = sigma * np.random.normal(0, np.sqrt(dt))
        drift = a * x[t] - b * x[t]**3
        dx = (drift + u + d) * dt + noise
        x[t+1] = x[t] + dx
    
    within_band = (x >= 0.8) & (x <= 1.2)
    compliance_rates.append(np.mean(within_band) * 100)

# --- 5. Statistical Results ---
mean_rate = np.mean(compliance_rates)
std_rate = np.std(compliance_rates)
min_rate = np.min(compliance_rates)
max_rate = np.max(compliance_rates)

print()
print("=" * 50)
print("RESULTS")
print("=" * 50)
print(f"Compliance Rate: {mean_rate:.1f}% ± {std_rate:.1f}% (n={n_trials})")
print(f"Range: [{min_rate:.1f}%, {max_rate:.1f}%]")
print()

# Verify against reported value
reported_mean = 99.6
reported_std = 0.3
if abs(mean_rate - reported_mean) < 1.0 and abs(std_rate - reported_std) < 0.5:
    print("✓ PASS: Results consistent with reported values (99.6% ± 0.3%)")
else:
    print("✗ FAIL: Results differ from reported values!")
    print(f"  Expected: {reported_mean}% ± {reported_std}%")
    print(f"  Got: {mean_rate:.1f}% ± {std_rate:.1f}%")
