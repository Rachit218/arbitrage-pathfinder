import streamlit as st
import pandas as pd
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Arbitrage Detector", layout="wide")
st.title("Graph-Theoretic Arbitrage Detector")
st.markdown("**Core Engine:** C++ (Bellman-Ford) | **Data Ingress:** Python (Binance API)")

# Helper function to run the C++ engine
def run_cpp_engine():
    # Ensure we use the correct absolute path for the executable
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(script_dir, 'arbitrage_engine')
    
    # Run the compiled C++ binary
    if os.name == 'nt': # Windows
        exe_path += ".exe"
        
    result = subprocess.run([exe_path], capture_output=True, text=True)
    return result.stdout

# --- Section 1: Data Pipeline ---
st.sidebar.header("Control Panel")
if st.sidebar.button("1. Fetch Live Market Data"):
    with st.spinner("Pulling 20-currency snapshot from Binance..."):
        # Run your fetch_rates.py script
        subprocess.run(["python3", "fetch_rates.py"])
    st.sidebar.success("Market data updated!")

# Load the current market graph
try:
    df = pd.read_csv("market_edges.csv")
    nodes = set(df['source']).union(set(df['target']))
    st.sidebar.metric(label="Active Currencies (V)", value=len(nodes))
    st.sidebar.metric(label="Directed Edges (E)", value=len(df))
except FileNotFoundError:
    st.error("No market data found. Please fetch data first.")
    st.stop()

# --- Section 2: Execution & Visualization ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Engine Output")
    if st.button("2. Execute C++ Scan", type="primary"):
        with st.spinner("Running Bellman-Ford in microseconds..."):
            cpp_output = run_cpp_engine()
            st.code(cpp_output, language='bash')
            
            # Parse output for visualization
            arbitrage_path = []
            if "ARBITRAGE DETECTED" in cpp_output:
                st.success("Negative-weight cycle isolated.")
                # Extract the sequence line
                for line in cpp_output.split('\n'):
                    if line.startswith("Sequence:"):
                        path_str = line.replace("Sequence: ", "").strip()
                        # Convert "USDT -> BTC -> ETH -> USDT" into a list
                        arbitrage_path = [node.strip() for node in path_str.split("->")]
            else:
                st.info("Market is perfectly balanced.")
                
            st.session_state['arbitrage_path'] = arbitrage_path

with col2:
    st.subheader("Market Graph Topology")
    
    # Build the NetworkX Graph
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row['source'], row['target'], weight=row['rate'])
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Use a circular layout so all 20 nodes are evenly spaced
    pos = nx.circular_layout(G)
    
    # Draw the base market (faint, low opacity)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, alpha=0.1, ax=ax)
    
    # If an arbitrage path exists in the session state, highlight it
    if 'arbitrage_path' in st.session_state and st.session_state['arbitrage_path']:
        path = st.session_state['arbitrage_path']
        # Create a list of edge tuples from the path list
        highlight_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        
        # Draw the profitable loop in thick red
        nx.draw_networkx_edges(
            G, pos, 
            edgelist=highlight_edges, 
            edge_color='red', 
            width=3.0, 
            arrows=True, 
            arrowsize=20,
            ax=ax
        )
    
    plt.axis('off')
    st.pyplot(fig)