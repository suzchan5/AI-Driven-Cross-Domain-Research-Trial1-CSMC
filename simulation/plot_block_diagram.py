import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def draw_block_diagram():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Style definitions
    box_props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=2)
    arrow_props = dict(arrowstyle='->', linewidth=2, color='black')
    text_props = dict(ha='center', va='center', fontsize=12, fontweight='bold')

    # --- 1. Blocks ---
    # Controller Block
    ax.add_patch(patches.Rectangle((3.5, 2.5), 2.5, 1.5, fill=True, facecolor='#e6f3ff', edgecolor='blue', linewidth=2))
    ax.text(4.75, 3.25, "C-SMC Agent\n(Controller)\n\n$u = -K \\tanh(s/\\phi)$", **text_props)

    # Plant Block
    ax.add_patch(patches.Rectangle((8.0, 2.5), 2.5, 1.5, fill=True, facecolor='#fff0f0', edgecolor='red', linewidth=2))
    ax.text(9.25, 3.25, "Human Cognition\n(Plant)\n\nDouble-Well\nDynamics", **text_props)

    # Summing Junctions
    # Compare (x - r)
    circle_sum1 = patches.Circle((2.0, 3.25), 0.3, fill=True, facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(circle_sum1)
    # Add Control + Disturbance
    circle_sum2 = patches.Circle((7.0, 3.25), 0.3, fill=True, facecolor='white', edgecolor='black', linewidth=2)
    ax.add_patch(circle_sum2)

    # --- 2. Connections (Arrows) ---
    
    # Reference r -> Sum1
    ax.annotate("", xy=(1.7, 3.25), xytext=(0.5, 3.25), arrowprops=arrow_props)
    ax.text(1.0, 3.5, "Goal $r=1.0$\n(Flow State)", ha='center', fontsize=11)
    ax.text(1.8, 3.5, "+", fontsize=14, fontweight='bold')

    # Sum1 -> Controller (Error e)
    ax.annotate("", xy=(3.5, 3.25), xytext=(2.3, 3.25), arrowprops=arrow_props)
    ax.text(2.9, 3.5, "Error $s$\n(Anxiety)", ha='center', fontsize=11)

    # Controller -> Sum2 (Input u)
    ax.annotate("", xy=(6.7, 3.25), xytext=(6.0, 3.25), arrowprops=arrow_props)
    ax.text(6.35, 3.5, "$u$\n(AI Support)", ha='center', fontsize=11, color='blue')
    ax.text(6.8, 3.5, "+", fontsize=14, fontweight='bold')

    # Disturbance d -> Sum2
    ax.annotate("", xy=(7.0, 3.55), xytext=(7.0, 5.0), arrowprops=dict(arrowstyle='->', linewidth=2, color='red'))
    ax.text(7.0, 5.2, "Panic Disturbance $d$\n(External Pressure)", ha='center', fontsize=11, color='red', fontweight='bold')
    ax.text(7.2, 3.6, "+", fontsize=14, fontweight='bold')

    # Sum2 -> Plant (Total Input)
    ax.annotate("", xy=(8.0, 3.25), xytext=(7.3, 3.25), arrowprops=arrow_props)

    # Plant -> Output x
    ax.annotate("", xy=(11.5, 3.25), xytext=(10.5, 3.25), arrowprops=arrow_props)
    ax.text(11.0, 3.5, "Output $x$\n(Recall Level)", ha='center', fontsize=11)

    # Feedback Loop (x -> Sum1)
    ax.annotate("", xy=(2.0, 2.95), xytext=(2.0, 1.5), arrowprops=arrow_props) # Up to Sum1
    ax.plot([11.0, 11.0, 2.0, 2.0], [3.25, 1.5, 1.5, 2.95], color='black', linewidth=1.5, linestyle='--') # Feedback path
    ax.text(6.5, 1.7, "Feedback (Metacognition / Monitoring)", ha='center', fontsize=11, style='italic')
    ax.text(2.2, 2.8, "-", fontsize=16, fontweight='bold') # Negative feedback

    # Title
    ax.text(6.0, 5.8, "Fig. D: Cognitive Sliding Mode Control System Architecture", ha='center', fontsize=14, fontweight='bold')

    # Save
    os.makedirs("ResearchProject_Trial1/docs/images", exist_ok=True)
    filename = "ResearchProject_Trial1/docs/images/system_block_diagram.png"
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    print(f"Saved {filename}")

if __name__ == "__main__":
    draw_block_diagram()
