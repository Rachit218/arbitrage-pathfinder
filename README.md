# Quantitative Graph Algorithms: Arbitrage Pathfinder

![Language](https://img.shields.io/badge/Language-C++-blue)
![Algorithm](https://img.shields.io/badge/Algorithm-Bellman--Ford-success)
![Focus](https://img.shields.io/badge/Focus-Quantitative_Finance-purple)

This repository contains a highly optimized C++ implementation of the **Bellman-Ford algorithm**, engineered specifically to detect negative weight cycles in directed graphs. 

While Bellman-Ford is a standard shortest-path algorithm, this project applies it to a classic quantitative finance problem: **Statistical/Triangular Arbitrage in Foreign Exchange (FX) markets.**

---

## The Mathematics of Arbitrage

In a foreign exchange market, an arbitrage opportunity exists if a sequence of currency trades results in a risk-free profit. Mathematically, if we trade through $n$ currencies with exchange rates $r_1, r_2, \dots, r_n$, an arbitrage exists if:

$$r_1 \times r_2 \times \dots \times r_n > 1$$

To model this as a graph problem, we take the natural logarithm of both sides to convert the product into a sum:

$$\log(r_1) + \log(r_2) + \dots + \log(r_n) > 0$$

By multiplying the entire equation by $-1$, the inequality flips:

$$(-\log(r_1)) + (-\log(r_2)) + \dots + (-\log(r_n)) < 0$$

**The Graph Transformation:** By representing currencies as vertices (nodes) and setting the directed edge weights between them to $w = -\log(\text{rate})$, the search for a profitable arbitrage opportunity is mathematically reduced to finding a **negative weight cycle** in the graph.

---

## Algorithmic Limitations

To bridge the gap between textbook computer science and live-market realities, this implementation accounts for several strict algorithmic boundaries:

1. **Single vs. Multiple Cycles:** The Bellman-Ford algorithm is designed to flag the presence of a negative cycle and return the *first* one it resolves. It **does not** enumerate *all* possible arbitrage loops in the market.
2. **Global Reachability:** A standard Bellman-Ford search only detects cycles reachable from a single chosen source node. To ensure no market inefficiencies are missed, this implementation initializes all vertex distances to `0` (mathematically equivalent to adding a 'dummy node' connected to all currencies with a weight of 0), allowing it to detect disconnected arbitrage loops.
---

## Technical Architecture

* **Language:** C++ 
* **Time Complexity:** $O(V \times E)$, where $V$ is the number of currencies and $E$ is the number of exchange rates.
* **Space Complexity:** $O(V)$ auxiliary space to maintain the distance array and predecessor map.

---
## Quick Start & Usage

**1. Clone the repository and install UI dependencies:**
`git clone https://github.com/YourUsername/arbitrage-pathfinder.git`
`cd arbitrage-pathfinder`
`pip install streamlit pandas`

**2. Compile the C++ Backend Engine:**
Compile the source code using standard GCC with optimization flags to generate the executable that the Streamlit app will call.
`g++ -O3 bellman_ford.cpp -o arbitrage_finder`

**3. Launch the Streamlit Dashboard:**
`streamlit run app.py`
