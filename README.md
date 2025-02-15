# CFG Graph

# Project Goal

The goal of this project is to design an algorithm that can identify paths in a directed graph using a context-free grammar (CFG). Specifically, it should be able to identify paths in the graph that follow the language of a context-free grammar (CFG).

# Problem Explanation

Given a directed graph **G = (V, E)**, where:
- **V** is the set of vertices, and
- **E** is the set of edges, and each edge **e ∈ E** is labeled.

The task is to check if there exists a path between a vertex **v ∈ V** and another vertex **u ∈ V** where the path adheres to the language defined by a context-free grammar **L**. 

The goal is to verify if a path exists in the graph from vertex **v** to vertex **u**, where the path follows the rules defined by the context-free grammar **L**.

# Grammar (CFG) Overview

A context-free grammar (CFG) is defined by:
- **Σ**: The alphabet of terminal symbols.
- **N**: The set of non-terminal symbols (uppercase letters).
- **T**: The set of terminal symbols (lowercase letters).
- **P**: The set of production rules.
- **S**: The start symbol.

For example, the following is a CFG in **Chomsky Normal Form (CNF)**:

```
S → HP
S → PG
H → OR
P → WR
O → y
W → j
R → k
G → x
```

**Start Symbol**: **S**


In the second part of the problem, we consider all the vertices of the graph. We will design an algorithm that, given the input from Part One, identifies all reachable vertices from a given start vertex **s** based on the rules of the CFG.

The algorithm will return all vertices **v ∈ V** where there exists a path from **s** to **v** that follows the context-free grammar **L**.


