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
## Algorithmic Execution Pipeline
**Network Construction:** The data layer ingests the supply chain variables and constructs a directed graph using an Adjacency List, where warehouses are vertices ($V$) and transit routes are edges ($E$).
**State Initialization:** The user selects a source and destination warehouse via the Streamlit interface, triggering the routing algorithms.
**Kinetic Evaluation:** As the algorithm explores neighboring nodes, the $Q_{10}$ function computes the true cost of traversing each edge by cross-referencing transit hours against the refrigeration temperature.
**Priority Sorting:** Discovered paths are pushed into the custom Min-Heap structure, sorting the queue strictly by the lowest accumulated biochemical degradation.
**Graph Traversal:** The modified Dijkstra's algorithm continuously pops the safest route from the Min-Heap, bypassing physically faster routes if their thermal penalty indicates high cargo damage.Path Reconstruction: Once the destination node is reached, the system traces the optimal pointers backward to generate the final sequence of hubs.
**Data Visualization:** The Streamlit frontend receives the optimal array, renders the step-by-step route, and generates Seaborn bar charts to quantify the exact shelf-life preserved compared to standard time-based routing.
This modular architecture ensures that the complex kinetic calculations are entirely decoupled from the user interface. This separation of concerns allows you to scale the dataset, swap in different biochemical formulas for different pharmaceuticals, or integrate live IoT temperature sensors in the future without needing to rebuild the core pathfinder.

## Tech Stack
* **Backend:** Python, Custom DSA (Min-Heap, Graph Theory)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Frontend UI:** Streamlit


