import pandas as pd
from src.min_heap import MinHeap
from src.kinetic_models import calculate_degradation

def build_graph_from_csv(file_path):
    """
    Converts a Pandas CSV of logistics routes into an Adjacency List graph.
    """
    df = pd.read_csv(file_path)
    graph = {}
    
    for _, row in df.iterrows():
        source = row['source']
        dest = row['destination']
        hours = row['transit_hours']
        temp = row['avg_temp_celsius']
        
        if source not in graph:
            graph[source] = []
        if dest not in graph:
            graph[dest] = []
            
        # Add the directed edge: (destination, transit_hours, average_temperature)
        graph[source].append((dest, hours, temp))
        
    return graph

def dijkstra_cold_chain(graph, start_node, target_node):
    """
    Finds the route that minimizes biochemical degradation.
    """
    # Track the minimum degradation to reach each node
    min_degradation = {node: float('inf') for node in graph}
    min_degradation[start_node] = 0
    
    # Track the optimal path
    previous_nodes = {node: None for node in graph}
    
    pq = MinHeap()
    pq.push((0, start_node))
    
    while not pq.is_empty():
        current_deg, current_node = pq.pop()
        
        # Stop early if we reached the target optimally
        if current_node == target_node:
            break
            
        # Skip if we already found a cleaner path to this node
        if current_deg > min_degradation[current_node]:
            continue
            
        # Explore neighbor warehouses
        for neighbor, hours, temp in graph[current_node]:
            # Calculate the biochemical cost for this specific truck route
            leg_degradation = calculate_degradation(hours, temp)
            total_degradation = current_deg + leg_degradation
            
            # If this path causes less spoilage, update and push to the heap
            if total_degradation < min_degradation[neighbor]:
                min_degradation[neighbor] = total_degradation
                previous_nodes[neighbor] = current_node
                pq.push((total_degradation, neighbor))
                
    # Reconstruct the optimal route backward from the target
    path = []
    current = target_node
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
        
    # Check if a path actually exists
    if min_degradation[target_node] == float('inf'):
        return None, float('inf')
        
    return path, round(min_degradation[target_node], 3)

def dijkstra_shortest_time(graph, start_node, target_node):
    """
    Standard routing algorithm: finds the fastest physical route (ignores temperature).
    Useful for comparing against our kinetic model.
    """
    min_time = {node: float('inf') for node in graph}
    min_time[start_node] = 0
    previous_nodes = {node: None for node in graph}
    
    pq = MinHeap()
    pq.push((0, start_node))
    
    while not pq.is_empty():
        current_time, current_node = pq.pop()
        
        if current_node == target_node:
            break
        if current_time > min_time[current_node]:
            continue
            
        for neighbor, hours, temp in graph[current_node]:
            total_time = current_time + hours # Ignoring temperature entirely
            
            if total_time < min_time[neighbor]:
                min_time[neighbor] = total_time
                previous_nodes[neighbor] = current_node
                pq.push((total_time, neighbor))
                
    path = []
    current = target_node
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
        
    return path, round(min_time[target_node], 1)