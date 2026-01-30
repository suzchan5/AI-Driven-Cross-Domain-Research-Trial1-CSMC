import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def plot_concept_diagram():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Common Potential: Shallow Well (High Sensitivity)
    x = np.linspace(-2.0, 2.0, 400)
    # Shallow potential: a small, b large? Or just scale V.
    # Standard: V = -0.5*x^2 + 0.25*x^4
    # Shallow: Scale down.
    V = (-0.5 * x**2 + 0.25 * x**4) * 0.5 # Shallower
    
    # --- Plot 1: Without AI ---
    ax1.plot(x, V, color='gray', linewidth=2, linestyle='--')
    ax1.set_title("Without AI: High Vulnerability", fontsize=14, fontweight='bold', color='darkred')
    ax1.set_ylim(-0.4, 0.4)
    ax1.set_xlim(-1.8, 1.8)
    ax1.axis('off')
    
    # Ball falling
    ball_x_panic = -1.2 # Collapsed
    ball_y_panic = (-0.5 * ball_x_panic**2 + 0.25 * ball_x_panic**4) * 0.5
    ax1.scatter([1.0], [-0.125], s=100, color='lightgray', alpha=0.5) # Original position
    ax1.scatter([ball_x_panic], [ball_y_panic], s=400, color='gray', edgecolors='black') # Fallen
    
    # Annotations
    ax1.text(0, 0.3, "Stress Impact", ha='center', color='red', fontsize=12, fontweight='bold')
    ax1.arrow(0.5, 0.1, -1.0, 0, head_width=0.05, head_length=0.1, color='red', linewidth=3)
    ax1.text(1.0, -0.2, "Healthy", ha='center', color='gray')
    ax1.text(-1.2, -0.3, "Collapse\n(Mind Blanking)", ha='center', color='darkred', fontweight='bold')
    ax1.text(0, -0.35, "Typical response of\nHigh Sensitivity Person", ha='center', fontsize=10, style='italic', bbox=dict(facecolor='white', alpha=0.7))

    # --- Plot 2: With AI (C-SMC) ---
    ax2.plot(x, V, color='gray', linewidth=2, linestyle='--') # Underlying personality is same
    ax2.set_title("With AI: Augmented Resilience", fontsize=14, fontweight='bold', color='darkblue')
    ax2.set_ylim(-0.4, 0.4)
    ax2.set_xlim(-1.8, 1.8)
    ax2.axis('off')

    # Draw "Virtual Wall" (Boundary Layer)
    # The AI creates a virtual steep potential wall around the target
    # Visualize this as a Green Band or Shield
    rect = patches.Rectangle((0.7, -0.4), 0.6, 0.8, linewidth=0, edgecolor='none', facecolor='green', alpha=0.2)
    ax2.add_patch(rect)
    
    # Ball staying
    ball_x_safe = 0.9
    ball_y_safe = (-0.5 * ball_x_safe**2 + 0.25 * ball_x_safe**4) * 0.5
    ax2.scatter([ball_x_safe], [ball_y_safe], s=400, color='royalblue', edgecolors='black', zorder=10)
    
    # Annotations
    ax2.text(0, 0.3, "Same Stress Impact", ha='center', color='red', fontsize=12)
    ax2.arrow(0.5, 0.1, -0.4, 0, head_width=0.05, head_length=0.1, color='red', linewidth=3) # Blocked
    
    # Force arrow from AI
    ax2.arrow(0.6, 0.0, 0.3, 0, head_width=0.04, head_length=0.08, color='blue', linewidth=4)
    ax2.text(0.3, -0.1, "AI Support\n(C-SMC)", ha='center', color='blue', fontweight='bold')

    ax2.text(1.0, 0.35, "Safe Zone", ha='center', color='green', fontweight='bold')
    ax2.text(0, -0.35, "AI acts as a 'Mental Airbag',\nallowing sensitive people to stay Healthy.", ha='center', fontsize=10, style='italic', bbox=dict(facecolor='white', alpha=0.7, edgecolor='blue'))

    # Save
    os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)
    filename = "ResearchProject_Trial1/docs/images/concept_resilience.png"
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    print(f"Saved {filename}")

if __name__ == "__main__":
    plot_concept_diagram()
