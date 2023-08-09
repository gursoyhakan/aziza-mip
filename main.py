
import mip as mp
# Define the nodes
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# Define the edges and their distances
edges = {
            (1, 2): 1, (2, 5): 2, (5, 8): 1, (8, 11): 5, (11, 14): 6, (14, 17): 7,
            (17, 20): 8,
            (1, 3): 1, (2, 3): 1, (3, 6): 2, (6, 8): 3, (6, 9): 5, (9, 12): 6, (12, 14): 1,
            (12, 15): 3, (15, 18): 2, (18, 20): 1, (1, 4): 1, (1, 7): 1, (4, 7): 1,
            (7, 9): 1,
            (7, 10): 5, (10, 13): 2, (13, 16): 5, (16, 19): 11, (19, 20): 5,
            (13, 15): 5, (10, 12): 1, (15, 19): 7, (1, 19): 26, (2, 18): 18
}
# Create the model
model = mp.Model()
# Create decision variables
x = {}
incoming = {}
outgoing = {}
for node in nodes:
    incoming[node] = model.add_var(var_type=mp.INTEGER)
    outgoing[node] = model.add_var(var_type=mp.INTEGER)
for edge in edges:
    x[edge] = model.add_var(var_type=mp.BINARY, name=f"x_{edge[0]}_{edge[1]}")
# Set up the objective function
objective = model.add_var(var_type=mp.CONTINUOUS)
objective = mp.xsum(edges[edge] * x[edge] for edge in edges)
model.objective = mp.minimize(objective)

# Add constraints
# Leaving node 1
model += mp.xsum(x[edge] for edge in edges if edge[0] == 1) >= 1
# Departure from node 20
model += mp.xsum(x[edge] for edge in edges if edge[1] == 20) >= 1

# Incoming vs. outgoing edges for each node

for node in nodes:
    if node != 1 and node != 20:
        incoming[node] = mp.xsum(x[edge] for edge in edges if edge[1] == node)
        outgoing[node] = mp.xsum(x[edge] for edge in edges if edge[0] == node)
        model += incoming[node] >= outgoing[node]
# number leaving 1 is greater than or equal to number came to 20
outgoing[1] = mp.xsum(x[edge] for edge in edges if edge[0] == 1)
incoming[20] = mp.xsum(x[edge] for edge in edges if edge[1] == 20)
model += incoming[20] >= outgoing[1]

'''
# Flow conservation
for node in nodes:
    if node != 0 and node != 20:
        incoming[node] = mp.xsum(x[edge] for edge in edges if edge[1] == node)
        outgoing[node] = mp.xsum(x[edge] for edge in edges if edge[0] == node)
        model += incoming[node] == outgoing[node]
'''
# Solve the model
model.optimize()
# Retrieve and print results
if model.status == mp.OptimizationStatus.OPTIMAL:
    for edge in edges:
        if x[edge].x >= 0.5:  # Check if edge is selected
            print(f"Edge {edge}: Distance {edges[edge]}")
else:
    print(f"Model Status : {model.status}")
