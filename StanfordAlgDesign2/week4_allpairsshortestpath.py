class DirectedGraph(object):
	def __init__(self, n_nodes, outgoing_edge_dict, incoming_edge_dict):
		self.n_nodes = n_nodes
		self.out_edges = outgoing_edge_dict
		self.in_edges = incoming_edge_dict

def graph_reader(filename):
	n_nodes = None
	edge_dict = {}
	with open(filename, 'r') as fo:
		for idx, line in enumerate(fo):
			if idx == 0:
				n_nodes = int(line.split()[0])
				out_edge_dict = {i:[] for i in range(1,n_nodes+1)} #nodes are indexed from 1 #hash table of tail node : [(head node, edge weight) ... ]
				in_edge_dict = {i:[] for i in range(1,n_nodes+1)} #hash table of head node : [(tail node, edge weight) ... ]
			else:
				tail, head, cost = [int(i) for i in line.split()]
	
				out_edge_dict[tail].append((head, cost))
				in_edge_dict[head].append((tail, cost))

	return n_nodes, out_edge_dict, in_edge_dict

def bellman_ford(directed_graph, source):
	#A is a 2D array with row indices i =[0,1,2,...,n_nodes - 1) and column indices v=[0,1,2,...,n_nodes)
	A = [[None for dummy1 in range(directed_graph.n_nodes)] for dummy2 in range(directed_graph.n_nodes)]

	#base case
	for v in range(directed_graph.n_nodes):
		A[0][v] = float("inf")
	A[0][source - 1] = 0

	for i in range(1,directed_graph.n_nodes):
		for v in range(directed_graph.n_nodes):
				
				possibilities = directed_graph.in_edges[v+1] #list of head, cost incident to v+1
				possible_costs = [A[i-1][poss[0]-1] + poss[1] for poss in possibilities]
				possible_costs.append(A[i-1][v])
				A[i][v] = min(possible_costs)

	#detect negative-cost cycles
	for v in range(directed_graph.n_nodes):
		if not A[directed_graph.n_nodes - 2][v] == A[directed_graph.n_nodes - 1][v]:
			return "Problem is intractable due to negative-cost cycles"
	return A[-1]

def bellman_ford_repeat(directed_graph):
	"""Run bellman-ford n times (once with each node as source) and return
	the weight of the minimum-weight path in the entire graph."""
	global_min = float("inf")
	for source in range(1, directed_graph.n_nodes+1):
		print source
		current_output = bellman_ford(directed_graph, source)
		if type(current_output) == type("string"):
			return "NULL"
		else:
			current_min = min(current_output)
			if current_min < global_min:
				global_min = current_min
	return global_min

def dijkstra(directed_graph, source, maximum = float("inf")):
	distances = [maximum for dummy in range(directed_graph.n_nodes)]
	distances[source-1] = 0

	to_explore = [source,]

	while to_explore:
		current = to_explore.pop(0)

		for neighbor, cost in directed_graph.out_edges[current]:



				alt = distances[current - 1] + cost

				if alt < distances[neighbor - 1]:
					distances[neighbor - 1] = alt

					to_explore.append(neighbor)

	return distances


## test ##
dg_nocycle = DirectedGraph(*graph_reader("g_simple_nocycle.txt"))
# dg_cycle = DirectedGraph(*graph_reader("g_simple_cycle.txt"))
bf_nocycle = bellman_ford(dg_nocycle, 1)
# bf_cycle = bellman_ford_repeat(dg_cycle)
print bf_nocycle
# print bf_cycle
dijkstra_nocycle = dijkstra(dg_nocycle, 1)
print dijkstra_nocycle

#g1 = DirectedGraph(*graph_reader("g1.txt"))
#g2 = DirectedGraph(*graph_reader("g2.txt"))
#g3 = DirectedGraph(*graph_reader("g3.txt"))

#print bellman_ford_repeat(g1)
#print bellman_ford_repeat(g2)
#print bellman_ford_repeat(g3)




