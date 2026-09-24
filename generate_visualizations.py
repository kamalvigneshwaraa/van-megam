#!/usr/bin/env python3
"""
Generate Visualization Charts for TDMA Optimizer Documentation
Produces PNG images of Network Topology with Slot Coloring and TDMA Schedule Timeline.
"""

import matplotlib.pyplot as plt
import networkx as nx
from tdma_brain import build_physical_graph, optimize_schedule, NODE_COORDINATES, RADIO_RANGE

SLOT_COLORS = [
    "#e6194B", "#3cb44b", "#ffe119", "#4363d8", "#f58231", 
    "#911eb4", "#42d4f4", "#f032e6", "#bfef45", "#fabed4", 
    "#469990", "#dcbeff", "#9A6324", "#fffac8", "#800000"
]


def generate_topology_plot(node_coords, schedule, output_filename="topology_graph.png"):
    G = build_physical_graph(node_coords, RADIO_RANGE)
    pos = {node: coords for node, coords in node_coords.items()}
    node_colors = [SLOT_COLORS[schedule[node] % len(SLOT_COLORS)] for node in G.nodes()]

    plt.figure(figsize=(9, 7))
    plt.title("TDMA Wireless Network Topology & Slot Assignment\n(Nodes with same color share timeslots via Spatial Reuse)", fontsize=12, fontweight="bold", pad=15)

    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="#7f8c8d", width=1.5, label="1-Hop Link (<=500m)")
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, edgecolors="#2c3e50", linewidths=2)

    node_labels = {node: f"{node}\n(Slot {schedule[node]})" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_weight="bold", font_family="sans-serif")

    plt.xlabel("X Coordinate (meters)", fontsize=10)
    plt.ylabel("Y Coordinate (meters)", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"[+] Saved topology graph plot to {output_filename}")


def generate_schedule_timeline_plot(schedule, output_filename="tdma_timeline.png"):
    num_slots = max(schedule.values()) + 1
    def node_sort_key(name):
        nums = "".join(filter(str.isdigit, name))
        return int(nums) if nums else name

    sorted_nodes = sorted(schedule.keys(), key=node_sort_key)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title("TDMA Schedule Allocation Frame Matrix (Slot vs Node)", fontsize=12, fontweight="bold", pad=15)

    for i, node in enumerate(sorted_nodes):
        slot = schedule[node]
        color = SLOT_COLORS[slot % len(SLOT_COLORS)]
        ax.barh(node, 1, left=slot, color=color, edgecolor="#2c3e50", height=0.6)
        ax.text(slot + 0.5, i, f"Slot {slot}", ha="center", va="center", color="black", fontweight="bold", fontsize=8)

    ax.set_xlabel("Time Slot Index (1ms duration each)", fontsize=10, fontweight="bold")
    ax.set_ylabel("Radio Node ID", fontsize=10, fontweight="bold")
    ax.set_xlim(0, num_slots)
    ax.set_xticks(range(num_slots))
    ax.set_xticklabels([f"Slot {s}" for s in range(num_slots)])
    ax.grid(True, axis="x", linestyle="--", alpha=0.6)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"[+] Saved TDMA timeline plot to {output_filename}")


if __name__ == "__main__":
    G, G_conflict, schedule = optimize_schedule(NODE_COORDINATES, RADIO_RANGE)
    generate_topology_plot(NODE_COORDINATES, schedule, "topology_graph.png")
    generate_schedule_timeline_plot(schedule, "tdma_timeline.png")
