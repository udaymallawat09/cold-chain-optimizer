# 🧊 Cold Chain Thermodynamic Routing Engine

## Overview
Traditional logistics software routes vehicles based purely on physical distance or transit time. This project introduces a **Thermodynamic Routing Engine** designed specifically for the food technology and biopharmaceutical industries. It calculates the optimal delivery path by minimizing biochemical degradation (spoilage) rather than just minimizing time, ensuring highly perishable products arrive with maximum remaining shelf-life.

## Biochemical Model
The core of the routing engine relies on reaction kinetics. Instead of treating all transit hours equally, the algorithm calculates a kinetic penalty for temperature abuse using a **$Q_{10}$ Temperature Coefficient Model**.
* **Baseline Temperature:** Assumes an optimal refrigerated environment (e.g., 4.0°C).
* **Exponential Spoilage:** If a truck's refrigeration unit fails, the algorithm applies an exponential degradation multiplier.
* **Result:** The system intelligently detours shipments through slower, but properly chilled routes to minimize total microbial growth.

## System Architecture & DSA
This project was built from scratch without relying on external routing libraries to demonstrate core Data Structures and Algorithms (DSA) proficiency:
* **Graph Representation:** Supply chain networks are built from raw CSV data into Adjacency Lists.
* **Custom Min-Heap:** A from-scratch Priority Queue dynamically ranks the safest routes based on cumulative kinetic cost.
* **Modified Dijkstra's Algorithm:** Explores the network to find the absolute lowest-degradation path from hub to destination.

## Tech Stack
* **Backend:** Python, Custom DSA (Min-Heap, Graph Theory)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Frontend UI:** Streamlit


