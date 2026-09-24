#!/usr/bin/env python3
"""
Generate System Architecture Flowchart Diagram for PDF Documentation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def create_flowchart(output_filename="system_flowchart.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Title
    ax.text(5, 5.7, "TDMA Schedule Planner & Optimizer — End-to-End Workflow", 
            ha="center", va="center", fontsize=14, fontweight="bold", color="#1e3799")

    # Boxes
    boxes = [
        {"x": 0.5, "y": 3.8, "w": 2.5, "h": 1.2, "title": "1. Radio Input Data", "desc": "16 Node Coordinates\nRadio Range: 500m", "color": "#e8f4f8", "border": "#2980b9"},
        {"x": 3.75, "y": 3.8, "w": 2.5, "h": 1.2, "title": "2. Graph Construction", "desc": "Distance-1 Links (Physical G)\nDistance-2 Links (Conflict G)", "color": "#e8f8f5", "border": "#27ae60"},
        {"x": 7.0, "y": 3.8, "w": 2.5, "h": 1.2, "title": "3. Optimization Engine", "desc": "DSATUR & Graph Coloring\nSpatial Reuse Allocation", "color": "#fef9e7", "border": "#f39c12"},
        {"x": 2.1, "y": 1.0, "w": 2.5, "h": 1.2, "title": "4. Schedule Verification", "desc": "Zero 1-Hop Collision Check\nZero 2-Hop Collision Check", "color": "#f4ecf7", "border": "#8e44ad"},
        {"x": 5.4, "y": 1.0, "w": 2.5, "h": 1.2, "title": "5. EMANE Profile Generator", "desc": "emane_tdma_schedule.xml\n1ms Slot & NEM Mapping", "color": "#ebdef0", "border": "#6c5ce7"},
    ]

    for b in boxes:
        rect = patches.FancyBboxPatch(
            (b["x"], b["y"]), b["w"], b["h"],
            boxstyle="round,pad=0.1",
            facecolor=b["color"],
            edgecolor=b["border"],
            linewidth=2
        )
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"] - 0.3, b["title"], 
                ha="center", va="center", fontsize=10, fontweight="bold", color="#2c3e50")
        ax.text(b["x"] + b["w"]/2, b["y"] + 0.35, b["desc"], 
                ha="center", va="center", fontsize=8.5, color="#34495e")

    # Arrows
    arrow_props = dict(arrowstyle="->", lw=2, color="#2c3e50")
    
    # 1 -> 2
    ax.annotate("", xy=(3.75, 4.4), xytext=(3.0, 4.4), arrowprops=arrow_props)
    # 2 -> 3
    ax.annotate("", xy=(7.0, 4.4), xytext=(6.25, 4.4), arrowprops=arrow_props)
    # 3 -> 4
    ax.annotate("", xy=(3.35, 2.2), xytext=(8.25, 3.8), arrowprops=dict(arrowstyle="->", lw=2, color="#2c3e50", connectionstyle="arc3,rad=0.3"))
    # 4 -> 5
    ax.annotate("", xy=(5.4, 1.6), xytext=(4.6, 1.6), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"[+] Saved system flowchart to {output_filename}")


if __name__ == "__main__":
    create_flowchart()
