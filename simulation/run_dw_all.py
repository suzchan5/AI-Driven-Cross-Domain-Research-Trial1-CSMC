import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# Double-Well Potential Simulation Engine
# ---------------------------------------------------------
dt = 0.01

def run_dw_simulation(
    duration_minutes, 
    label, 
    color, 
    param_a,          # Potential depth parameter (Higher = Deeper/More Stable)
    param_b=1.0,      # Shape parameter
    K_gain=0.0, 
    phi=0.0, 
    use_control=False,
    use_delay=False,      # Phase 1
    use_chattering=False, # Phase 3
    pulse_strength=-2.0,  # Enough to push over the hill if not careful
    filename=""
):
    # Time Setup
    T_total = duration_minutes * 60.0
    steps = int(T_total / dt)
    time = np.linspace(0, T_total, steps)
    
    # State Vars
    x = np.zeros(steps)
    u = np.zeros(steps)
    x[0] = 1.0 # Start at Healthy state (+1)
    
    # Pulse Timing (30 min scale: 12m-14m = 720s-840s)
    # For Fig 0 comparison, we use the same timing
    pulse_start = 720.0
    pulse_end = 840.0
    
    for t in range(steps - 1):
        # 1. Disturbance
        # Slow wave + Panic Pulse
        d = 0.3 * np.sin(2 * np.pi * (1/150) * time[t]) 
        if pulse_start <= time[t] <= pulse_end:
            d += pulse_strength
            
        # 2. Control Input (C-SMC)
        control_val = 0.0
        if use_control:
            curr_x = x[t]
            if use_delay and t > 100: # 1s delay
                 curr_x = x[t-100]
            
            # Target is Healthy State (r = 1.0)
            s = curr_x - 1.0
            
            if use_chattering: # Phase 3
                 control_val = -K_gain * np.tanh(s / 0.01)
            elif phi > 0:
                 control_val = -K_gain * np.tanh(s / phi)
            else:
                 control_val = 0.0

        u[t] = control_val

        # 3. Dynamics (Double-Well)
        # Potential V(x) = -a/2 x^2 + b/4 x^4
        # Force = -dV/dx = ax - bx^3
        # dx = (ax - bx^3 + u + d) dt + noise
        
        internal_force = param_a * x[t] - param_b * (x[t]**3)
        
        noise = 0.05 * np.random.normal(0, np.sqrt(dt))
        dx = (internal_force + u[t] + d) * dt + noise
        
        x[t+1] = x[t] + dx
        
        # Hard limit to prevent numerical explosion if it runs away too far (though x^3 usually contains it)
        if x[t+1] > 3: x[t+1] = 3
        if x[t+1] < -3: x[t+1] = -3

    # 4. Plot and Save
    plt.figure(figsize=(10, 6))
    plt.plot(time, x, label=label, color=color, linewidth=2)
    
    # Reference Lines
    plt.axhline(y=1.0, color='green', linestyle='--', label="Healthy State (+1.0)")
    plt.axhline(y=-1.0, color='red', linestyle='--', label="Depressed/Collapsed (-1.0)")
    plt.axhline(y=0.0, color='black', linestyle=':', label="Tipping Point (0.0)")
    
    plt.fill_between(time, 0.8, 1.2, color='green', alpha=0.1, label="Target Band")
    plt.axvspan(pulse_start, pulse_end, color='red', alpha=0.05, label="Panic Pulse")

    plt.ylim(-2.0, 2.0)
    plt.xlim(0, T_total)
    plt.title(f"{label} (Double-Well Model)")
    plt.xlabel("Time [s]")
    plt.ylabel("State x (Recall Level)")
    plt.legend(loc='lower left')
    plt.grid(True, alpha=0.3)
    
    if filename:
        plt.savefig(filename)
        print(f"Saved {filename}")
        plt.close()
    
    # Calculate Compliance (Stay within Healthy Band)
    within_band = (x >= 0.8) & (x <= 1.2)
    return np.mean(within_band) * 100

# ---------------------------------------------------------
# 2. Execution Sequence
# ---------------------------------------------------------
os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)

# A. Pre-Experiment (Fig 0): High vs Low Stability (Control OFF)
# param_a determines the depth of the well.
# Low Stability (High Sensitivity): a = 0.5 (Shallow well, easy to flip)
# High Stability (Low Sensitivity): a = 2.0 (Deep well, hard to flip)

plt.figure(figsize=(10, 6))

# Helper to get trace without plotting immediately
def get_dw_trace(a, pulse_mag=-2.0):
    steps = int(1800.0/dt)
    time = np.linspace(0, 1800.0, steps)
    x = np.zeros(steps)
    x[0] = 1.0
    for t in range(steps-1):
        d = 0.3 * np.sin(2*np.pi*(1/150)*time[t])
        if 720 <= time[t] <= 840: d += pulse_mag
        force = a*x[t] - 1.0*(x[t]**3)
        noise = 0.05 * np.random.normal(0, np.sqrt(dt))
        dx = (force + d)*dt + noise
        x[t+1] = x[t] + dx
    return time, x

# Run Traces
t, x_stable = get_dw_trace(a=2.0, pulse_mag=-3.0) # Strong pulse needed to test stable one
_, x_unstable = get_dw_trace(a=0.5, pulse_mag=-3.0) # Same pulse kills the unstable one

plt.plot(t, x_stable, label="Low Sensitivity (Stable Well)", color="blue")
plt.plot(t, x_unstable, label="High Sensitivity (Shallow Well)", color="red")

plt.axhline(y=1.0, color='green', linestyle='--', label="Healthy")
plt.axhline(y=-1.0, color='red', linestyle='--', label="Collapsed")
plt.axhline(y=0.0, color='black', linestyle=':', label="Tipping Point")
plt.axvspan(720, 840, color='red', alpha=0.05)
plt.title("Fig. 0: Stress Response without AI Support (Double-Well)")
plt.xlabel("Time [s]")
plt.ylabel("State x")
plt.ylim(-2.0, 2.0)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("ResearchProject_Trial1/docs/images/personality_comparison.png")
print("Saved Fig 0")


# B. Phase 1-4 Experiments
# Target: High Sensitivity (Shallow Well, a=0.5) needs AI Support
target_a = 0.5
pulse_mag = -2.5 # Strong enough to flip the shallow well (-0.5*x + x^3 ...)

# Phase 1: Divergence (Delay)
run_dw_simulation(30, "Phase 1: Delay Divergence", "red", param_a=target_a, pulse_strength=pulse_mag, K_gain=8.0, phi=0.01, use_control=True, use_delay=True, filename="ResearchProject_Trial1/docs/images/phase1_30min.png")

# Phase 2: Weak Gain (Succumbs to pressure -> flips to negative)
# Low Gain is not enough to counteract pulse_mag + well slope
run_dw_simulation(30, "Phase 2: Weak Gain (Collapse)", "orange", param_a=target_a, pulse_strength=pulse_mag, K_gain=0.5, phi=1.0, use_control=True, filename="ResearchProject_Trial1/docs/images/phase2_30min.png")

# Phase 3: Chattering (High Gain, Narrow Phi)
run_dw_simulation(30, "Phase 3: Chattering", "purple", param_a=target_a, pulse_strength=pulse_mag, K_gain=10.0, phi=0.01, use_control=True, use_chattering=True, filename="ResearchProject_Trial1/docs/images/phase3_30min.png")

# Phase 4: Optimized C-SMC
# Gain must be strong enough to prevent crossing x=0
comp = run_dw_simulation(30, "Phase 4: Optimized C-SMC", "blue", param_a=target_a, pulse_strength=pulse_mag, K_gain=5.0, phi=0.3, use_control=True, filename="ResearchProject_Trial1/docs/images/phase4_30min.png")
print(f"Phase 4 Compliance: {comp:.2f}%")
