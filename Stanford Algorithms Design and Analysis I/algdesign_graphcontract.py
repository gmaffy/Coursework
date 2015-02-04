"""Implementation of the randomized contraction algorithm developed by Karger to find the minimum cut in
an undirected graph (represented as an adjacency list).
A single run of the algorithm has an n**-2 probability of finding a particular minimum cut solution,
but if we repeat the algorithm for (n**2)(ln n) trials we have only an n**-1 probability of failure."""


#######################################
import random
#######################################


#######################################
F = 'kargerMinCut.txt'
#######################################


#######################################
def read_graph(filename):
	graph_dict = {}
	with open(filename, 'r') as file:
		for line in file:
			i = line.split()
			graph_dict[int(i[0])] = [int(i[idx]) for idx in range(1,len(i))]
	return graph_dict
#######################################


#######################################
class AdjacencyGraph(object):
	"""Representation of undirected graph as an adjacency list with supported methods
	for graph contraction."""

	def __init__(self, adjacency_dictionary):
		self.adjacency_dict = adjacency_dictionary

	def count_nodes(self):
		return len(self.adjacency_dict.keys())

	def max_node(self):
		return max(self.adjacency_dict.keys())

	def count_edges(self):
		return sum([len(self.adjacency_dict[key]) for key in self.adjacency_dict.keys()])

	def fuse(self, nodeA, nodeB):
		"""Merge together nodeA and nodeB into a single 'supernode' and delete any resulting self-loops."""
		joint_edges = self.adjacency_dict[nodeA] + self.adjacency_dict[nodeB]
		supernode = self.max_node()+1

		#print nodeA, nodeB, joint_edges, supernode

		#cleaned_edges = [item for item in joint_edges if not item in (nodeA, nodeB)] #remove self loops

		#remove pre-fused nodes and replace with new one
		del self.adjacency_dict[nodeA]
		del self.adjacency_dict[nodeB]
		self.adjacency_dict[supernode] = joint_edges

		#replace any references to original nodes with updated one
		new_dict = {}
		for key in self.adjacency_dict.keys():
			new_list = []
			for item in self.adjacency_dict[key]:
				if item in (nodeA, nodeB):
					new_list.append(supernode)
				else:
					new_list.append(item)
			new_dict[key] = new_list

		cleaned_edges = [item for item in new_dict[supernode] if not item == supernode]
		new_dict[supernode] = cleaned_edges

		self.adjacency_dict = new_dict

	def choose_random_edge(self):
		start_node = random.choice(self.adjacency_dict.keys())
		return start_node, random.choice(self.adjacency_dict[start_node])
#######################################


#######################################
def graph_contract(graph):
	"""Input an AdjacencyGraph item and perform a single run of Karger's algorithm"""
	while graph.count_nodes() > 2:
		#choose two distinct random nodes
		nodeA, nodeB = graph.choose_random_edge()

		#glue them together
		graph.fuse(nodeA, nodeB)

	return len(graph.adjacency_dict[graph.adjacency_dict.keys()[0]]), graph.adjacency_dict

def multicontract(N, filename):
	"""graph_contract is not guaranteed to be correct. Probability of obtaining the correct answer
	can be increased by running the algorithm multiple times and collecting the best result."""
	min_cut_size = float("inf")
	best_graph = None
	for dummy in range(N):
		graph = AdjacencyGraph(read_graph(filename))
		current_size = graph_contract(graph)
		if 0 < current_size[0] < min_cut_size:
			min_cut_size = current_size[0]
			best_graph = current_size[1]
		if not dummy % 10:
			print dummy
	return min_cut_size, best_graph
#######################################


print multicontract(1000, F)

