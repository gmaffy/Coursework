import math
import itertools

def all_binary_strings(length):
	#print sorted(["".join(seq) for seq in itertools.product("01", repeat=length)])
	return ["".join(seq) for seq in itertools.product("01", repeat=length)]

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

class TravelingSalesmanBinary(TravelingSalesman):

	def build_subsets(self):
		#self.subset_to_integer = {'1'+item[::-1] : int(item,2) for item in all_binary_strings(self.n_nodes - 1)}
		self.subset_array = []
		formatting = '{0:'+str(self.n_nodes-1)+'b}'
		#print 2**(self.n_nodes-1)
		for int10 in range(2**(self.n_nodes - 1)):
			bin = formatting.format(int10)
			if len(bin.split()[0]) < self.n_nodes - 1:
				bin = '0'*(self.n_nodes - 1 - len(bin.split()[0])) + bin.split()[0]
			self.subset_array.append('1'+bin[::-1])

		#print self.subset_array[0:100]
		#self.integer_to_subset = dict((v, k) for (k, v) in self.subset_to_integer.items())
		self.subsets_by_size = {i : [] for i in range(1,self.n_nodes+1)} #maps size of subsets : integer IDs of subsets of that size
		for subset in self.subset_array:
			#print subset, subset.count("1"), self.subset_to_index(subset)
			self.subsets_by_size[subset.count("1")].append(self.subset_to_index(subset))

		#print self.subset_array
		#print self.subsets_by_size

	def subset_to_index(self, subset):
		binary = subset[1::]
		binary = binary[::-1]
		integer = int(binary, 2)
		#print 'binint', binary, integer
		return integer

	def build_array(self):
		#A will be a 2D array indexed by subsets of nodes that contain 0, and destinations
		#j = {1,2,...,n}
		self.array = [[None for dummy1 in range(self.n_nodes)] for dummy2 in range(len(self.subset_array))]
		#self.array = [[None for dummy1 in range(self.n_nodes)] for dummy2 in range(2)]
		for row_index in range(len(self.array)):
			self.array[row_index][0] = float("inf")
		self.array[self.subset_to_index(("1"+"0"*(self.n_nodes -1)))][0] = 0
		#print self.array

	def solve(self):
		for subproblem_size in range(2,self.n_nodes+1):
			print "subsize", subproblem_size, len(self.subsets_by_size[subproblem_size])
			for subset_id in self.subsets_by_size[subproblem_size]:
				#print subset_id
				destination = self.subset_array[subset_id]

				if not destination == "1"+"0"*(self.n_nodes - 1):

					for dest_idx, bit in enumerate(destination):
						if int(bit) and not dest_idx == 0:
							subset_without_dest = destination[0:dest_idx]+"0"+destination[dest_idx+1::]
							subsetid_without_dest = self.subset_to_index(subset_without_dest)
							#print subset_without_dest
							print subset_id
							#print dest_idx

							recurrence_array = []
							for idx, k in enumerate(subset_without_dest):
								if int(k) and not idx == dest_idx:
									#print idx, dest_idx
									#print subsetid_without_dest
									#print destination, subset_without_dest
									#print self.array[subsetid_without_dest]
									recurrence_array.append(self.array[subsetid_without_dest][idx] + self.cost(idx, dest_idx))


							#recurrence_array = [self.array[subsetid_without_dest][idx] + self.cost(idx, dest_idx) for idx, k in enumerate(subset_without_dest) if int(k) and not idx == dest_idx]
							self.array[subset_id][dest_idx] = min(recurrence_array)
							#self.array[1][dest_idx] = min(recurrence_array)

				#dump the first row of the array, add a new one
				#self.array = [self.array[1],[None for i in range(self.n_nodes)]]
				#self.array[1][0] = float("inf")

		#return self.array
		final_subset_id = self.subsets_by_size[self.n_nodes][0]
		#return self.array[final_subset_id]
		return min([self.array[final_subset_id][j] + self.cost(j,0) for j in range(2,self.n_nodes)])


testgraph_rect = {i : [0,i] for i in range(5)}
for j in range(9,4,-1):
	testgraph_rect[j] = [1,j-5]
print testgraph_rect

testgraph_linear = {i: [0,i] for i in range(4)}
print testgraph_linear

if __name__ == "__main__":
	#x = sorted(all_binary_strings(24))
	#subset_to_integer = {'1'+item[::-1] : int(item,2) for item in all_binary_strings(25 - 1)}
	#print x[0:100]
	graph = ts_reader("tsp.txt")
	#ts = TravelingSalesmanBinary(testgraph_rect)
	ts = TravelingSalesmanBinary(testgraph_rect)
	print "data structures built"
	print ts.solve()