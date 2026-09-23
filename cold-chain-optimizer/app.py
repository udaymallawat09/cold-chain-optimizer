import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Ensure the app can find your src folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.dijkstra_router import dijkstra_cold_chain, dijkstra_shortest_time
from src.kinetic_models import calculate_degradation

# --- HELPER FUNCTIONS ---
def build_graph_from_dataframe(df):
    """Converts the uploaded Pandas DataFrame into our Adjacency List graph."""
    graph = {}
    for _, row in df.iterrows():
        source, dest = row['source'], row['destination']
        hours, temp = row['transit_hours'], row['avg_temp_celsius']
        
        if source not in graph: graph[source] = []
        if dest not in graph: graph[dest] = []
            
        graph[source].append((dest, hours, temp))
    return graph

def get_path_metrics(graph, path):
    """Calculates both time and degradation for a given path to compare them fairly."""
    total_time = 0
    total_deg = 0
    if not path: return 0, 0
    
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        for neighbor, hrs, temp in graph[u]:
            if neighbor == v:
                total_time += hrs
                total_deg += calculate_degradation(hrs, temp)
                break
    return total_time, total_deg

# --- STREAMLIT UI ---
st.set_page_config(page_title="Kinetic Routing Engine", layout="wide")
st.title("🧊 Cold Chain Thermodynamic Routing Engine")
st.markdown("Upload a logistics CSV to calculate the route that minimizes biochemical spoilage.")

# Sidebar for User Inputs
st.sidebar.header("1. Upload Network Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV (source, destination, transit_hours, avg_temp_celsius)", type=["csv"])

if uploaded_file is not None:
    # Read the user's file
    df = pd.read_csv(uploaded_file)
    st.subheader("Network Overview")
    st.dataframe(df, use_container_width=True)
    
    # Build the graph and extract unique nodes for the dropdown menus
    graph = build_graph_from_dataframe(df)
    all_nodes = sorted(list(graph.keys()))
    
    st.sidebar.header("2. Select Route")
    start_node = st.sidebar.selectbox("Starting Warehouse", all_nodes)
    target_node = st.sidebar.selectbox("Destination", all_nodes)
    
    # Run the simulation when the user clicks the button
    if st.sidebar.button("Calculate Optimal Route"):
        # Run standard algorithm
        fastest_path, _ = dijkstra_shortest_time(graph, start_node, target_node)
        fast_time, fast_deg = get_path_metrics(graph, fastest_path)
        
        # Run kinetic algorithm
        kinetic_path, _ = dijkstra_cold_chain(graph, start_node, target_node)
        kin_time, kin_deg = get_path_metrics(graph, kinetic_path)
        
        # --- UI DISPLAY ---
        if not kinetic_path:
            st.error("No valid route exists between these locations.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("🕒 Standard Route (Fastest)")
                st.write(f"**Path:** {' ➔ '.join(fastest_path)}")
                st.metric("Total Transit Time", f"{fast_time:.1f} hrs")
                st.metric("Biochemical Spoilage", f"{fast_deg:.2f} units", delta=f"+{(fast_deg - kin_deg):.2f} units", delta_color="inverse")
                
            with col2:
                st.success("🧬 Kinetic Route (Lowest Spoilage)")
                st.write(f"**Path:** {' ➔ '.join(kinetic_path)}")
                st.metric("Total Transit Time", f"{kin_time:.1f} hrs")
                st.metric("Biochemical Spoilage", f"{kin_deg:.2f} units")
                
            # Render the Seaborn Comparison Chart
            st.markdown("---")
            st.subheader("Route Comparison Analysis")
            
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(
                x=['Standard Route (Time-Based)', 'Kinetic Route (Spoilage-Based)'], 
                y=[fast_deg, kin_deg], 
                palette=['#e74c3c', '#2ecc71'], 
                hue=['Standard Route (Time-Based)', 'Kinetic Route (Spoilage-Based)'],
                legend=False,
                ax=ax
            )
            ax.set_ylabel("Accumulated Degradation Units")
            ax.set_title("Biochemical Spoilage by Route")
            st.pyplot(fig)
else:
    st.info("👈 Please upload a logistics CSV file in the sidebar to begin.")