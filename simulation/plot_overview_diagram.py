import numpy as np
import matplotlib.pyplot as plt
import os

def plot_overview_diagram():
    # Setup
    x = np.linspace(-2.2, 2.2, 400)
    # Double-Well Potential: V(x) = -0.5*x^2 + 0.25*x^4
    # Flip it for visualization so "Wells" look like valleys? 
    # Usually Potential V(x) is y-axis.
    V = -0.5 * x**2 + 0.25 * x**4
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, V, color='black', linewidth=2, label='Cognitive Potential Landscape')
    
    # 1. Draw Wells
    plt.text(1.2, -0.3, "Healthy State\n(Flow)", ha='center', color='green', fontsize=12, fontweight='bold')
    plt.text(-1.2, -0.3, "Collapsed State\n(Mind Blanking)", ha='center', color='darkred', fontsize=12, fontweight='bold')
    plt.text(0, 0.1, "Tipping Point\n(Separatrix)", ha='center', color='black', fontsize=10)
    
    # 2. Draw System State (The Ball)
    # Position the ball slightly displaced by panic, but held by AI
    ball_x = 0.5 
    ball_y = -0.5 * ball_x**2 + 0.25 * ball_x**4
    plt.scatter([ball_x], [ball_y], s=300, color='royalblue', edgecolors='black', zorder=10, label='Current Cognitive State')
    
    # 3. Draw Disurbance (Panic) - Pushing towards left (Collapse)
    plt.arrow(ball_x + 0.2, ball_y + 0.1, -0.6, 0, head_width=0.05, head_length=0.1, fc='red', ec='red', linewidth=3)
    plt.text(ball_x, ball_y + 0.2, "Panic Pulse (Disturbance d)", color='red', fontsize=11, fontweight='bold', ha='center')
    
    # 4. Draw C-SMC Intervention - Pushing back towards right (Health)
    # Using a "Wall" or opposing arrow
    plt.arrow(ball_x - 0.4, ball_y - 0.1, 0.6, 0, head_width=0.05, head_length=0.1, fc='blue', ec='blue', linewidth=3)
    plt.text(ball_x, ball_y - 0.25, "C-SMC Intervention (u)", color='blue', fontsize=11, fontweight='bold', ha='center')

    # 5. Annotations
    plt.axvline(0, color='black', linestyle=':', linewidth=1)
    
    # Shading for Boundary Layer
    # Phi=0.3 around Target=1.0 -> [0.7, 1.3]
    # Map this to the potential curve
    x_band = np.linspace(0.7, 1.3, 100)
    V_band = -0.5 * x_band**2 + 0.25 * x_band**4
    plt.fill_between(x_band, V_band, 0.5, color='green', alpha=0.1, label='Cognitive Boundary Layer ($\phi=0.3$)')
    plt.text(1.0, 0.3, "Safety Band", color='green', fontsize=10, ha='center')

    # Formatting
    plt.title("Overview of Cognitive Sliding Mode Control System", fontsize=14)
    plt.xlabel("Cognitive State $x$ (Recall Level)")
    plt.ylabel("Potential Energy $V(x)$")
    plt.ylim(-0.6, 0.6)
    plt.xlim(-2.0, 2.0)
    plt.yticks([]) # Hide y-axis numbers as it's qualitative
    plt.grid(False)
    
    # Save
    os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)
    filename = "ResearchProject_Trial1/docs/images/system_overview.png"
    plt.savefig(filename)
    print(f"Saved {filename}")

if __name__ == "__main__":
    plot_overview_diagram()
