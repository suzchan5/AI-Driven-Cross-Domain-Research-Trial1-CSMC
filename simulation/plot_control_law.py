import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# C-SMC Control Law Visualization
# ---------------------------------------------------------
def plot_control_law():
    # Parameters from Phase 4
    K = 5.0
    phi = 0.3
    
    # Error range (s = x - r)
    s = np.linspace(-1.0, 1.0, 500)
    
    # 1. Ideal SMC (Sign function) - Phase 3 like
    u_ideal = -K * np.sign(s)
    
    # 2. Proposed C-SMC (Tanh function) - Phase 4
    u_csmc = -K * np.tanh(s / phi)
    
    plt.figure(figsize=(8, 6))
    
    # Plot Ideal
    plt.plot(s, u_ideal, label="Ideal SMC (Hard Switching)", color='gray', linestyle='--', linewidth=1.5)
    
    # Plot C-SMC
    plt.plot(s, u_csmc, label=f"Proposed C-SMC (Tanh, $\phi={phi}$)", color='blue', linewidth=3)
    
    # Visualize Boundary Layer
    # The linear region is roughly [-phi, phi] if using saturation, 
    # but for tanh it's continuous. We mark the characteristic range.
    plt.axvspan(-phi, phi, color='green', alpha=0.1, label=f"Cognitive Boundary Layer ($\pm\phi$)")
    
    # Annotations
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel("Sliding Variable $s = x - r$ (Error)")
    plt.ylabel("Control Input $u$ (Cognitive Intervention)")
    plt.title("Fig. C: Designed Control Law with Boundary Layer")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save
    os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)
    filename = "ResearchProject_Trial1/docs/images/control_law.png"
    plt.savefig(filename)
    print(f"Saved {filename}")

if __name__ == "__main__":
    plot_control_law()
