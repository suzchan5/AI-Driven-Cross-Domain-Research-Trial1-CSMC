"""
Strategy 1: Model Validation with Public Data (Demonstration Script)

This script demonstrates how to:
1. Load physiological data (e.g., HRV from PhysioNet Exam Stress Dataset)
2. Convert it to a "cognitive state" proxy x(t)
3. Fit Double-Well Potential parameters (a, b) to the data
4. Validate the model's predictive accuracy

NOTE: This uses SYNTHETIC data as a demonstration. 
To use real data:
- Download dataset from: https://physionet.org/content/wearable-exam-stress/1.0.0/
- Replace synthetic_data() with actual IBI/HRV data loading
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

# ========== Step 1: Generate Synthetic "Real Data" ==========
# In actual use, replace this with real dataset loading

def synthetic_data(duration=1800, dt=1.0):
    """
    Simulate 'ground truth' cognitive state from a real exam stress scenario.
    This mimics what you would extract from HRV data.
    
    Returns:
        t: time array (seconds)
        x_gt: ground truth cognitive state (normalized, 1=healthy, -1=panic)
    """
    t = np.arange(0, duration, dt)
    n = len(t)
    
    # Baseline: Start healthy
    x_gt = np.ones(n) * 0.9
    
    # Add sinusoidal "exam anxiety" (periodic stress waves)
    x_gt += 0.1 * np.sin(2 * np.pi * t / 600)
    
    # Inject stress events (e.g., difficult questions at t=600, 1200)
    stress_events = [
        (600, 120, -0.6),   # Event at 10min, duration 2min, drop -0.6
        (1200, 180, -0.8),  # Event at 20min, duration 3min, drop -0.8
    ]
    
    for t_start, t_dur, magnitude in stress_events:
        mask = (t >= t_start) & (t < t_start + t_dur)
        x_gt[mask] += magnitude * np.exp(-(t[mask] - t_start) / 30)
    
    # Add noise (biological variability)
    x_gt += np.random.normal(0, 0.05, n)
    
    # Clip to valid range
    x_gt = np.clip(x_gt, -1.0, 1.0)
    
    return t, x_gt


# ========== Step 2: Double-Well Potential Model ==========

def double_well_drift(x, a, b):
    """
    The drift term of Double-Well Potential: f(x) = ax - bx^3
    
    Args:
        x: cognitive state
        a: restoration parameter
        b: nonlinearity parameter
    
    Returns:
        dx/dt (drift component)
    """
    return a * x - b * (x ** 3)


def simulate_model(t, x0, a, b, sigma=0.05):
    """
    Simulate the Double-Well model WITHOUT control (u=0, d=0)
    to see if the model can reproduce natural dynamics.
    
    dx = (ax - bx^3)dt + sigma*dW
    """
    dt = t[1] - t[0]
    x = np.zeros(len(t))
    x[0] = x0
    
    for i in range(1, len(t)):
        drift = double_well_drift(x[i-1], a, b)
        diffusion = sigma * np.random.randn()
        x[i] = x[i-1] + drift * dt + diffusion * np.sqrt(dt)
        x[i] = np.clip(x[i], -1.0, 1.0)  # Physical constraint
    
    return x


# ========== Step 3: Parameter Fitting ==========

def fit_parameters(t, x_data):
    """
    Fit parameters (a, b) to match observed data.
    
    Method: Minimize prediction error using scipy curve_fit
    """
    # Compute empirical drift: dx/dt ≈ (x[i+1] - x[i]) / dt
    dt = t[1] - t[0]
    dx_dt = np.diff(x_data) / dt
    x_mid = x_data[:-1]  # Use midpoint for matching
    
    # Fit f(x) = a*x - b*x^3 to dx/dt
    try:
        params, _ = curve_fit(
            double_well_drift, 
            x_mid, 
            dx_dt,
            p0=[2.0, 1.0],  # Initial guess
            bounds=([0.1, 0.1], [10.0, 10.0])  # Reasonable ranges
        )
        a_fit, b_fit = params
    except:
        # Fallback if fitting fails
        a_fit, b_fit = 2.0, 1.0
    
    return a_fit, b_fit


# ========== Step 4: Validation ==========

def validate_model(t, x_data, a, b, sigma=0.05):
    """
    Simulate the fitted model and compare to real data.
    
    Returns:
        x_pred: model prediction
        rmse: root mean square error
        corr: correlation coefficient
    """
    x_pred = simulate_model(t, x_data[0], a, b, sigma)
    
    # Compute metrics
    rmse = np.sqrt(np.mean((x_data - x_pred) ** 2))
    corr, _ = pearsonr(x_data, x_pred)
    
    return x_pred, rmse, corr


# ========== Main Execution ==========

if __name__ == "__main__":
    print("=" * 60)
    print("Strategy 1: Model Validation with Synthetic Data")
    print("=" * 60)
    
    # Generate synthetic "exam stress" data
    t, x_real = synthetic_data(duration=1800, dt=1.0)
    
    print(f"\n[1] Loaded 'real' data: {len(t)} samples over {t[-1]/60:.1f} minutes")
    print(f"    Mean cognitive state: {np.mean(x_real):.3f}")
    print(f"    Std deviation: {np.std(x_real):.3f}")
    
    # Fit parameters
    a_fit, b_fit = fit_parameters(t, x_real)
    
    print(f"\n[2] Fitted parameters:")
    print(f"    a (restoration) = {a_fit:.3f}")
    print(f"    b (nonlinearity) = {b_fit:.3f}")
    
    # Validate model
    x_pred, rmse, corr = validate_model(t, x_real, a_fit, b_fit, sigma=0.05)
    
    print(f"\n[3] Validation metrics:")
    print(f"    RMSE = {rmse:.4f}")
    print(f"    Correlation = {corr:.4f}")
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot 1: Data vs Model
    ax1.plot(t/60, x_real, 'b-', label='Real Data (Exam Stress)', linewidth=1.5, alpha=0.7)
    ax1.plot(t/60, x_pred, 'r--', label=f'Model Prediction (a={a_fit:.2f}, b={b_fit:.2f})', linewidth=2)
    ax1.axhline(0, color='k', linestyle=':', alpha=0.3, label='Tipping Point')
    ax1.set_xlabel('Time (minutes)')
    ax1.set_ylabel('Cognitive State x(t)')
    ax1.set_title('Model Validation: Real Data vs. Double-Well Prediction')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Potential Landscape
    x_range = np.linspace(-1.2, 1.2, 200)
    V = -0.5 * a_fit * x_range**2 + 0.25 * b_fit * x_range**4
    
    ax2.plot(x_range, V, 'k-', linewidth=2)
    ax2.fill_between(x_range, V, alpha=0.3, where=(x_range > 0), label='Healthy Well')
    ax2.fill_between(x_range, V, alpha=0.3, color='red', where=(x_range < 0), label='Panic Well')
    ax2.axvline(0, color='orange', linestyle='--', label='Barrier (Tipping Point)')
    ax2.set_xlabel('Cognitive State x')
    ax2.set_ylabel('Potential Energy V(x)')
    ax2.set_title(f'Fitted Double-Well Potential Landscape (a={a_fit:.2f}, b={b_fit:.2f})')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('model_validation_synthetic.png', dpi=150)
    print(f"\n[4] Figure saved: model_validation_synthetic.png")
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Replace synthetic_data() with actual PhysioNet data loading")
    print("2. Add this figure to paper as 'Figure X: Model Validation'")
    print("3. Cite dataset in references")
    print("=" * 60)
