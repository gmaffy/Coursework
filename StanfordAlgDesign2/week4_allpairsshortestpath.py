import time

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
	start_time = time.time()
	for source in range(1, directed_graph.n_nodes+1):
		print source, '\t', time.time() - start_time, '\t', global_min
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

def reweight(directed_graph, path_lengths):
	"""Given a graph directed_graph and a list of integers <= 0 path_lengths,
	reweight all edges in a graph such that the new value of each edge (u,v)
	is the original value plus the path length of u minus the path length of v.

	Returns new directed graph."""
	current_out_edges = directed_graph.out_edges
	current_in_edges = directed_graph.in_edges

	new_out_edges = {}
	new_in_edges = {}
	for key in current_out_edges.keys():
		new_out_edges[key] = []
		for value in current_out_edges[key]:
			new_out_edges[key].append((value[0], value[1]+path_lengths[key-1]-path_lengths[value[0]-1]))

	for key in new_out_edges.keys():
		for value in new_out_edges[key]:
			try:
				new_in_edges[value[0]].append((key, value[1]))
			except KeyError:
				new_in_edges[value[0]] = [(key, value[1]),]

	return DirectedGraph(directed_graph.n_nodes, new_out_edges, new_in_edges)


def johnson(directed_graph):
	start = time.time()
	#step 1: add vertex s with zero-weight edges to all other vertices
	s = directed_graph.n_nodes + 1
	directed_graph.out_edges[s] = [(node, 0) for node in range(1, s)]
	for key in directed_graph.in_edges.keys():
		directed_graph.in_edges[key].append((s,0))
	directed_graph.in_edges[s] = []
	directed_graph.n_nodes += 1

	#step 2: run bellman-ford
	path_lengths = bellman_ford(directed_graph, s)
	if type(path_lengths) == "string":
		return "NULL"

	directed_graph.out_edges.pop(s, None)
	directed_graph.in_edges.pop(s, None)
	directed_graph.n_nodes -= 1
	for key in directed_graph.in_edges.keys():
		directed_graph.in_edges[key].pop() #remove all references to s

	#step 3: reweight all edges using path_lengths
	reweighted_graph = reweight(directed_graph, path_lengths)

	#step 4: run Dijkstra for every possible source vertex on reweighted graph
	global_min = float("inf")

	for source in range(1,reweighted_graph.n_nodes + 1):
		output = dijkstra(reweighted_graph, source)
		#return output
		#step 5: reweight output

		#return path_lengths[0]
		reweighted_output = [item - path_lengths[source-1] + path_lengths[idx] for idx, item in enumerate(path_lengths)]
		current_min = min(reweighted_output)

		if current_min < global_min:
			global_min = current_min

		#print source, '\t', time.time() - start, '\t', global_min/2

	return global_min / 2, time.time() - start


## test ##
#dg_nocycle = DirectedGraph(*graph_reader("g_simple_nocycle.txt"))
# dg_cycle = DirectedGraph(*graph_reader("g_simple_cycle.txt"))
#bf_nocycle = bellman_ford(dg_nocycle, 1)
# bf_cycle = bellman_ford_repeat(dg_cycle)
#print bf_nocycle
# print bf_cycle
#dijkstra_nocycle = dijkstra(dg_nocycle, 1)
#print dijkstra_nocycle

#g1 = DirectedGraph(*graph_reader("g1.txt"))
#g2 = DirectedGraph(*graph_reader("g2.txt"))
g3 = DirectedGraph(*graph_reader("g3.txt"))

#print bellman_ford_repeat(g1)
#print bellman_ford_repeat(g2)
#print bellman_ford_repeat(g3)

print johnson(g3)




