# BayesNetwork_18051
Simple Library for Bayes Networks, it includes the functions: 

ver. 0.0.1 --bug with fully described function

you install it with pip install 

CreateNetwrok
is_fully_described
get_factors
to_compact_form
get_joint_probability

You define the nodes as: 
A = Node('A', [], {(): {0: 0.1, 1: 0.9}})
B = Node('B', [], {(): {0: 0.2, 1: 0.8}})
C = Node('C', [A, B], {(0, 0): {0: 0.3, 1: 0.7}, (0, 1): {0: 0.4, 1: 0.6}, (1, 0): {0: 0.5, 1: 0.5}, (1, 1): {0: 0.6, 1: 0.4}})
D = Node('D', [], {(): {0: 0.7, 1: 0.3}})
E = Node('E', [C, D], {(0, 0): {0: 0.8, 1: 0.2}, (0, 1): {0: 0.9, 1: 0.1}, (1, 0): {0: 0.1, 1: 0.9}, (1, 1): {0: 0.2, 1: 0.8}})
nodes = [A, B, C, D, E]

The edges as: 
edges = {A: [C], B: [C], C: [E], D: [E]}

and you create a network as:
network = BayesianNetwork(nodes,edges)

YOu can also use the functions as such: 
print(network.is_fully_described(A, E))
print(network.get_factors())
print(network.to_compact_form())

Here you define the state of the joint probability like this: 
state = {'A': 1, 'B': 0, 'C': 1, 'D': 0, 'E': 1}

And use it like this
print(network.get_joint_probability(state))
