class DirectedGraph(object):
	def __init__(self, n_nodes, outgoing_edge_dict, incoming_edge_dict, cheapest_incoming_edge_dict):
		self.n_nodes = n_nodes
		self.out_edges = outgoing_edge_dict
		self.in_edges = incoming_edge_dict
		self.cheapest_in_edges = cheapest_incoming_edge_dict

def graph_reader(filename):
	n_nodes = None
	edge_dict = {}
	with open(filename, 'r') as fo:
		for idx, line in enumerate(fo):
			if idx == 0:
				n_nodes = int(line.split()[0])
				out_edge_dict = {i:[] for i in range(1,n_nodes+1)} #nodes are indexed from 1 #hash table of tail node : [(head node, edge weight) ... ]
				in_edge_dict = {i:[] for i in range(1,n_nodes+1)} #hash table of head node : [(tail node, edge weight) ... ]
				cheapest_incoming_edge = {i: (None, float("inf")) for i in range(1,n_nodes)} #hash table of head node : (min-cost tail node, edge weight)
			else:
				tail, head, cost = [int(i) for i in line.split()]
	
				out_edge_dict[tail].append((head, cost))
				in_edge_dict[head].append((tail, cost))

				if cost < cheapest_incoming_edge[head][1]:
					cheapest_incoming_edge[head] = (tail, cost)

	return n_nodes, out_edge_dict, in_edge_dict, cheapest_incoming_edge

def bellman_ford(directed_graph, source):
	#A is a 2D array with row indices i =[0,1,2,...,n_nodes - 1) and column indices v=[0,1,2,...,n_nodes)
	A = [[None for dummy1 in range(directed_graph.n_nodes)] for dummy2 in range(directed_graph.n_nodes)]

	#base case
	for v in range(directed_graph.n_nodes):
		A[0][v] = float("inf")
	A[0][source - 1] = 0

	for i in range(directed_graph.n_nodes):
		for v in range(directed_graph.n_nodes):
			cheapest_head, cheapest_cost = directed_graph.cheapest_in_edges[v+1]
			A[i][v] = min(A[i-1][v], A[i-1][cheapest_head - 1] + cheapest_cost)

	#detect negative-cost cycles
	for v in range(directed_graph.n_nodes):
		if not A[directed_graph.n_nodes - 2][v] == A[directed_graph.n_nodes - 1][v]:
			return "Problem is intractable due to negative-cost cycles"
	return A

