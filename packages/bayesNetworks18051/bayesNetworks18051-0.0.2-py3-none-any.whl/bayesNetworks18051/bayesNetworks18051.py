import numpy as np

class Node:
    def __init__(self, name, parents, probabilities):
        self.name = name
        self.parents = parents
        self.probabilities = probabilities
        
    def get_probability(self, state):
        parent_state = tuple([state[p.name] for p in self.parents])
        return self.probabilities[parent_state][state[self.name]]

class BayesianNetwork:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        
    def is_fully_described(self, node1, node2):
        def dfs(node, node2, visited):
            if node == node2:
                return True
            visited.add(node)
            for neighbor in self.edges[node]:
                if neighbor in visited:
                    continue
                if dfs(neighbor, node2, visited):
                    return True
            return False
        
        return dfs(node1, node2, set())
        
    def get_factors(self):
        factors = []
        for node in self.nodes:
            factors.append((node.name, [p.name for p in node.parents]))
        return factors
    
    def to_compact_form(self):
        compact_form = []
        for node in self.nodes:
            compact_form.append((node.name, [p.name for p in node.parents], node.probabilities))
        return compact_form
    
    def get_joint_probability(self, state):
        joint_probability = 1
        for node in self.nodes:
            joint_probability *= node.get_probability(state)
        return joint_probability





