import json
from collections import defaultdict


class CFGGraphPathFinder:
    def __init__(self, graph, cfg):
        self.graph = graph  # {node: [(neighbor, label)]}
        self.cfg = self.validate_cfg(cfg)  # Validate CFG
        self.reverse_cfg = self.build_reverse_cfg()

    def validate_cfg(self, cfg):
        """Validates and normalizes the CFG."""
        if 'S' not in cfg:
            raise ValueError("CFG must have a start symbol 'S'")
        for nt, rules in cfg.items():
            if not isinstance(rules, list):
                raise ValueError(f"Invalid format for non-terminal {nt}")
            for rule in rules:
                if not isinstance(rule, list):
                    raise ValueError(f"Invalid production rule {rule} for non-terminal {nt}")
        return cfg

    def build_reverse_cfg(self):
        """Reverses the CFG for easier lookup."""
        reverse_cfg = defaultdict(set)
        for nt, rules in self.cfg.items():
            for rule in rules:
                reverse_cfg[tuple(rule)].add(nt)
        return reverse_cfg

    def find_paths(self, start, end): #fds
        """Finds all paths from start to end that conform to the CFG."""
        if start not in self.graph:
            print(f"Error: Start node '{start}' not found in graph.")
            return []

        paths = []
        stack = [(start, [start], [])]  # (current_node, path, labels)
        memo = set()

        while stack:
            node, path, labels = stack.pop()
            if (node, tuple(labels)) in memo:
                continue
            memo.add((node, tuple(labels)))

            print(f"Exploring path: {' -> '.join(path)}, Labels: {''.join(labels)}")

            if node == end:
                if self.valid_string(labels):
                    paths.append((path, labels))
                continue

            for neighbor, label in self.graph.get(node, []):
                stack.append((neighbor, path + [neighbor], labels + [label]))

        return paths

    def valid_string(self, labels): #cyk
        """Checks if the label sequence can be derived from the CFG using CYK parsing."""
        n = len(labels) # Length of the sequence
        if n == 0:
            return False
        # Initialize a 2D table for CYK parsing

        table = [[set() for _ in range(n)] for _ in range(n)]

        # step1: Fill the diagonal of the table
        for i, label in enumerate(labels):
            if (label,) in self.reverse_cfg:
                table[i][i] = self.reverse_cfg[(label,)]
            print(f"CYK Table[{i}][{i}] initialized with: {table[i][i]}")  # Debugging output

        # step2: Fill the rest of the table for sequences of length > 1
        for length in range(2, n + 1):  # Span length
            for i in range(n - length + 1): # End of the current span
                j = i + length - 1 # End of the current span
                for k in range(i, j): # Split point
                    # Combine valid productions
                    for B in table[i][k]:
                        for C in table[k + 1][j]:
                            if (B, C) in self.reverse_cfg:
                                table[i][j] |= self.reverse_cfg[(B, C)]
                                print(f"CYK Table[{i}][{j}] updated with: {table[i][j]}")  # Debugging output

        print(f"Final CYK Table: {table}")  # Debugging output

        return 'S' in table[0][n - 1]

    def find_reachable_nodes(self, source):
        """Finds all nodes that can be reached from the source node."""
        visited = set() #nodes visited
        stack = [source] #node to visit

        while stack:
            node = stack.pop() # DFS - remove the last added node
            if node in visited:
                continue
            visited.add(node) # Mark node as visited
            # Explore all neighbors
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor) # Add unvisited neighbors to stack

        return visited


def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file '{file_path}'.")
        exit(1)


def main(graph_file, cfg_file, start, end):
    graph = load_json(graph_file)
    cfg = load_json(cfg_file)

    finder = CFGGraphPathFinder(graph, cfg)
    paths = finder.find_paths(start, end) #dfs
    reachable_nodes = finder.find_reachable_nodes(start)

    if paths:
        print("Valid Paths:")
        for path, labels in paths:
            print(f"Path: {' -> '.join(path)}, Labels: {''.join(labels)}")
    else:
        print("No valid paths found.")

    print("\nNodes reachable from", start, ":", reachable_nodes)


if __name__ == "__main__":
    graph_file = "graph.json"
    cfg_file = "cfg.json"
    start = "A"
    end = "E"

    main(graph_file, cfg_file, start, end)
