import math

def subsets(mySet):
	"""Take a list of elements and return all permutations of that list,
	including the empty list and the original list."""
	return reduce(lambda z, x: z + [y + [x] for y in z], mySet, [[]])

def ts_reader(filename):
	graph_dict = {}
	with open(filename,'r') as fo:
		for idx, line in enumerate(fo):
			if idx:
				graph_dict[idx-1] = [float(item) for item in line.split()]
	return graph_dict


class TravelingSalesman(object):

	def __init__(self, graph_dict):
		self.graph_dict = graph_dict #hash of node : (x coord, y coord); nodes are indexed from zero
		self.n_nodes = len(self.graph_dict.keys())
		self.build_subsets()
		self.build_array()

	def cost(self, node1, node2):
		"""Return euclidean distance between two nodes"""
		x1, y1 = self.graph_dict[node1]
		x2, y2 = self.graph_dict[node2]
		return math.sqrt((y1-y2)**2 + (x1-x2)**2)
	
	def build_subsets(self):
		self.subset_to_integer = {tuple(sorted(item+[0])) : idx for idx, item in enumerate(subsets([i for i in range(1,self.n_nodes)]))}
		self.integer_to_subset = dict((v, k) for (k, v) in self.subset_to_integer.items())

		# self.subsets_containing_node = {i : [] for i in range(self.n_nodes)} #allows us to know which subsets contain given nodes
		# for subset in self.subset_to_integer.keys():
		# 	for node in subset:
		# 		self.subsets_containing_node[node].append(self.subset_to_integer[subset])
		# del self.subsets_containing_node[0]

		self.subsets_by_size = {i : [] for i in range(1,self.n_nodes+1)} #maps size of subsets : integer IDs of subsets of that size
		for subset in self.subset_to_integer.keys():
			self.subsets_by_size[len(subset)].append(self.subset_to_integer[subset])

	def build_array(self):
		#A will be a 2D array indexed by subsets of nodes that contain 0, and destinations
		#j = {1,2,...,n}
		self.array = [[None for dummy1 in range(self.n_nodes)] for dummy2 in range(len(self.integer_to_subset.keys()))]
		for row_index in range(len(self.integer_to_subset.keys())):
			self.array[row_index][0] = float("inf")
		self.array[self.subset_to_integer[(0,)]][0] = 0

	def solve(self):
		for subproblem_size in range(2,self.n_nodes+1):
			for subset_id in self.subsets_by_size[subproblem_size]:
				for destination in self.integer_to_subset[subset_id]:
					if not destination == 0:
						subset_without_dest = [i for i in self.integer_to_subset[subset_id] if not i == destination]
						subset_without_dest = tuple(subset_without_dest)
						subsetid_without_dest = self.subset_to_integer[subset_without_dest]

						recurrence_array = [self.array[subsetid_without_dest][k] + self.cost(k, destination) for k in subset_without_dest]
						self.array[subset_id][destination] = min(recurrence_array)

		#return self.array
		final_subset_id = self.subsets_by_size[self.n_nodes][0]
		#return self.array[final_subset_id]
		return min([self.array[final_subset_id][j] + self.cost(j,0) for j in range(2,self.n_nodes)])


testgraph_linear = {i : [0,i] for i in range(5)}
for j in range(9,4,-1):
	testgraph_linear[j] = [1,j-5]
print testgraph_linear

if __name__ == "__main__":
	graph = ts_reader("tsp.txt")
	ts = TravelingSalesman(testgraph_linear)
	print "dictionarieis built"
	print ts.solve()