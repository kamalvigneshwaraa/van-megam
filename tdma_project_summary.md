# TDMA Network Schedule Planner & Optimizer
**Vaan Megam Networks (VMN) — Wireless Protocol Development Internship Task**


## 1. Concept & Problem Overview

In a **Time Division Multiple Access (TDMA)** wireless network, radio nodes share the same frequency channel by taking turns in designated **time-slots**. If two nearby radios transmit at the same time, their signals overlap and cause interference, destroying transmitted data packets.

To guarantee **100% collision-free transmission** while maximizing network capacity, our software brain solves two critical interference challenges:

```

### Direct Link Interference (Distance-1)
* **Rule:** Radios within direct transmission range ($\le 500$ meters) are 1-hop neighbors.
* **Requirement:** Must be assigned different timeslots so they do not jam each other directly.

### Hidden Terminal Interference (Distance-2)
* **Rule:** If Node A and Node C both transmit to mutual intermediate neighbor Node B at the same time (Node A $\to$ Node B $\leftarrow$ Node C), their signals collide at receiver B.
* **Requirement:** Even if Node A and Node C cannot hear each other directly, they are 2-hop neighbors through B and **must be assigned different timeslots**.

### Spatial Reuse ($> 2$ Hops)
* **Rule:** Radios separated by more than 2 hops cause zero interference at any common receiver.
* **Benefit:** They can **safely reuse the exact same timeslot**, shortening total frame length and boosting overall network capacity!

---

## 2. System Architecture & Processing Workflow

The overall system functions as a centralized software brain that processes radio coordinates, constructs conflict graphs, applies optimization heuristics, and translates schedule matrices into emulator configurations through five core stages:

1. **Radio Input Data Processing:** Accepts 2D coordinates for all radio nodes and configures radio transmission range (500.0 meters).
2. **Graph Construction:** Builds the physical topology graph $G$ for 1-hop direct links and the Distance-2 conflict graph $G_{\text{conflict}}$ for 1-hop and 2-hop interference.
3. **Optimization Engine:** Applies graph coloring heuristics (DSATUR algorithm) to find the minimum number of timeslots required, maximizing spatial reuse.
4. **Schedule Verification:** Automatically verifies that zero 1-hop and zero 2-hop neighbors share a timeslot.
5. **EMANE Profile Generation:** Converts the optimized schedule matrix into native EMANE TDMA Radio Model XML configuration profiles.

---

## 3. Part 1 — Graph Theory & Optimization Algorithms

Part 1 models the physical wireless network as a graph mathematical structure and applies graph coloring optimization algorithms:

1. **Physical Topology Graph Construction:** Nodes represent radios with static 2D coordinates. An edge is created between Node A and Node B if Euclidean distance $\le 500.0$ meters.
2. **Distance-2 Conflict Graph Construction:** An edge is placed between two nodes if their shortest path distance in the physical graph is 1 or 2 hops. Nodes separated by $> 2$ hops share NO edge in the conflict graph, explicitly allowing **Spatial Reuse**.
3. **Graph Coloring Heuristics:** Finding the minimal number of slots is an NP-hard problem. The system applies the **DSATUR (Degree of Saturation)** algorithm to dynamically prioritize nodes with the highest saturation degree, producing optimal slot reuse.
4. **Automated Verification Engine:** Checks every pair of nodes to guarantee zero 1-hop and zero 2-hop collisions.

---

## 4. Part 2 — Physical Emulator (EMANE Setup & Integration)

In Part 2, the calculated schedule matrix is translated into native **EMANE TDMA Radio Model profiles** and multicast events:

* **Native Profile Generation:** Creates XML schedule profiles defining 1ms timeslot durations, recurring frame structures, operating frequencies, and per-node transmission allocations.
* **Multicast Event Publishing:** Broadcasts real-time schedule updates to EMANE event daemons via UDP multicast socket.
* **Containerized Deployment:** Uses Docker containerization to package EMANE and the schedule brain into a consolidated testing environment.

---

## 5. Project Conclusion

This project successfully designs and implements a centralized software brain that calculates optimal, collision-free TDMA schedules. By enforcing Distance-1 and Distance-2 graph coloring constraints while maximizing spatial reuse, the system minimizes frame length and maximizes overall wireless network throughput.
