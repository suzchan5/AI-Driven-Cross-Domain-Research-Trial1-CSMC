import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def draw_stick_figure(ax, x, y, tilt_deg=0, mood='happy'):
    # Head
    head = patches.Circle((x, y + 1.5), 0.3, facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(head)
    
    # Body (rotate based on tilt)
    angle = np.deg2rad(tilt_deg)
    # Pivot is at feet (x, y)
    # Body end point
    body_len = 1.2
    bx = x - body_len * np.sin(angle)
    by = y + body_len * np.cos(angle)
    
    ax.plot([x, bx], [y, by], color='black', linewidth=2) # Body
    
    # Arms
    ax.plot([x - 0.2, x + 0.2], [y + 0.8, y + 0.8], color='black', linewidth=2) 
    
    # Legs (simplified)
    ax.plot([x, x-0.3], [y, y-0.5], color='black', linewidth=2)
    ax.plot([x, x+0.3], [y, y-0.5], color='black', linewidth=2)

    # Face expression
    if mood == 'panic':
        # Open mouth O
        ax.add_patch(patches.Circle((x, y + 1.5), 0.05, facecolor='black'))
        # Sweat
        ax.text(x + 0.4, y + 1.7, "💦", fontsize=15)
    elif mood == 'happy':
        # Smile
        ax.text(x - 0.1, y + 1.45, "☺", fontsize=20, rotation=tilt_deg)

def plot_illustration():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # --- Shared Environment ---
    for ax in [ax1, ax2]:
        ax.set_xlim(-2, 4)
        ax.set_ylim(-1, 4)
        ax.axis('off')
        
        # Cliff
        cliff = patches.Polygon([[-2, -1], [1, -1], [1, 2], [-2, 2]], closed=True, facecolor='#D2B48C', edgecolor='none')
        ax.add_patch(cliff)
        ground_line = patches.Polygon([[1, -1], [4, -1], [4, -2], [1, -2]], closed=True, facecolor='#eeeeee') # Abyss bottom
        # ax.add_patch(ground_line)
        
        # Abyss Label
        ax.text(2.5, 0.5, "Panic Hole\n(Mind Blanking)", ha='center', color='gray', fontsize=10)

        # Wind (Stress)
        ax.arrow(-1.5, 2.5, 1.5, 0, head_width=0.1, head_length=0.2, color='red', linewidth=3, alpha=0.5)
        ax.text(-0.8, 2.7, "Stress Wind", color='red', fontsize=12, fontweight='bold')

    # --- Panel 1: Without AI ---
    ax1.set_title("Without AI Support\n(Sensitive Person)", fontsize=16, fontweight='bold', color='darkred')
    # Person falling
    draw_stick_figure(ax1, 0.8, 2.0, tilt_deg=45, mood='panic')
    ax1.text(2.0, 1.5, "Ahhh!", fontsize=14, fontweight='bold', color='red')
    
    # --- Panel 2: With AI ---
    ax2.set_title("With AI Support\n(Resilience)", fontsize=16, fontweight='bold', color='darkblue')
    # Person standing
    draw_stick_figure(ax2, 0.8, 2.0, tilt_deg=-5, mood='happy')
    
    # AI Support (Cushion/Backrest)
    rect = patches.Rectangle((-0.2, 2.0), 1.0, 1.5, angle=0, facecolor='#e6f3ff', edgecolor='blue', linewidth=2, alpha=0.5)
    # Support Arm
    ax2.add_patch(patches.FancyBboxPatch((0.2, 1.5), 0.2, 1.5, boxstyle="round,pad=0.1", fc="royalblue", ec="blue"))
    ax2.text(-0.5, 2.5, "AI Support", color='blue', fontsize=12, fontweight='bold', ha='right')
    ax2.text(2.0, 1.5, "I'm OK!", fontsize=14, fontweight='bold', color='green')

    # Save
    os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)
    filename = "ResearchProject_Trial1/docs/images/concept_illustration.png"
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    print(f"Saved {filename}")

if __name__ == "__main__":
    plot_illustration()
