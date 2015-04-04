import itertools

class Node(object):

	def __init__(self, data = None, leader = None):
		self.data = data
		self.leader = leader
		self.cc_size = 1
		if not self.leader: #if no leader is provided, node is itself a leader
			self.leader = self


class UnionFind(object):

	def __init__(self):
		self.array = [] #container for nodes, where the node's id is its index
		self.cc_count = 0

	def add_node(self, node):
		self.array.append(node)
		self.cc_count += 1

	def find(self, node_index):
		return self.array[node_index]

	def union(self, node1_idx, node2_idx):
		"""Merege the CCs containing node1 and node2"""

		node1, node2 = self.array[node1_idx], self.array[node2_idx]

		if node1.leader.cc_size > node2.leader.cc_size:
			large_leader, small_leader = node1.leader, node2.leader
		else:
			large_leader, small_leader = node2.leader, node1.leader

		large_leader.cc_size = large_leader.cc_size + small_leader.cc_size

		for node in self.array:
			if node.leader == small_leader:
				node.leader = large_leader
				node.cc_size = large_leader.cc_size
			elif node.leader == large_leader:
				node.cc_size = large_leader.cc_size

		self.recompute_cc_count()

	def recompute_cc_count(self):
		distinct_leaders = set([])
		for node in self.array:
			distinct_leaders.add(node.leader)
		self.cc_count = len(distinct_leaders)

class Edge(object):
	def __init__(self, node1, node2, cost):
		self.node1 = node1
		self.node2 = node2 
		self.cost = cost

def problem1_reader(filename):
	edges = []
	with open(filename, 'r') as fo:
		for idx, line in enumerate(fo):
			if not idx==0:
				node1, node2, cost = [int(i) for i in line.split()]
				edges.append(Edge(node1, node2, cost))

	return edges

def hashify(edge_list):
	edge_dict = {}
	for edge in edge_list:
		if edge.cost in edge_dict.keys():
			edge_dict[edge.cost].append((edge.node1, edge.node2))
		else:
			edge_dict[edge.cost] = [(edge.node1, edge.node2),]
	return edge_dict

def greedy_k_clustering(k, edge_dict, node_count, union_find):

	#load all nodes into union find
	for i in range(node_count):
		union_find.add_node(Node())
	
	while union_find.cc_count > k-1:

		#find the lowest-cost edge
		cheapest_cost = min(edge_dict.keys())
		#print cheapest_cost

		#choose an edge from the cheapest bin
		node1, node2 = edge_dict[cheapest_cost].pop(0)
		if len(edge_dict[cheapest_cost]) == 0: #if this bin is now empty, delete it
			del edge_dict[cheapest_cost]
		
		#check to make sure nodes are not in same CC
		if not union_find.array[node1-1].leader == union_find.array[node2-1].leader:
			if union_find.cc_count == k: #determine maximum distance: by definition, maximum distance is the next edge we would have added
				return cheapest_cost
			else:
				union_find.union(node1-1, node2-1)


	

# edge_dict = hashify(problem1_reader("clustering1.txt"))
# union_find = UnionFind()

# print greedy_k_clustering(4,edge_dict,500, union_find), "max distance"

###################################################
#################### PROBLEM 2 ####################
###################################################

#need to generate all binary strings with 1 or 2 bits of length 24
def kbits(n, k):
	"""Generate the n choose k binary strings of length n with
	k ones and n-k zeroes."""
	result = []
	for bits in itertools.combinations(range(n), k):
		s = ['0'] * n
		for bit in bits:
			s[bit] = '1'
		result.append(''.join(s))
	return result

#read in problem 2 nodes
def problem2_reader(filename):
	node_list = []
	with open(filename) as fo:
		for idx, line in enumerate(fo):
			if not idx == 0:
				node_list.append(''.join(line.split()))
	return node_list

def load_union_find(node_list):
	node_list = set(node_list)
	node_to_id = {}
	for idx, item in enumerate(node_list):
		node_to_id[item] = idx

	union_find = UnionFind()
	for i in range(len(node_list)):
		union_find.add_node(Node())

	return node_to_id, union_find

#need to map actual nodes to node indicies
def build_edge_dict(node_list):

	bit_length = len(node_list[0])
	binary_strings_1 = kbits(bit_length,1)
	binary_strings_2 = kbits(bit_length,2)

	formatting = '{0:'+str(bit_length)+'b}'

	edge_dict = {1: [], 2: []}

	node_set = set(node_list) #sets have amortized lookup O(1) vs. O(n) for lists

	for idx, node in enumerate(node_set):
		#print idx, len(edge_dict[1]), len(edge_dict[2])

		#check for hamming distance 1
		for binary in binary_strings_1:
			new_string = int(node,2) ^ int(binary,2)

			new_string = formatting.format(new_string)
			if new_string in node_set:
				edge_dict[1].append((node, new_string))

			#check for hamming distance 2
		for binary in binary_strings_2:
			new_string = int(node,2) ^ int(binary,2)
			new_string = formatting.format(new_string)
			if new_string in node_set:
				edge_dict[2].append((node, new_string))

	return edge_dict



def problem_2(edge_dict, union_find, node_to_id):
	while True:

		#find the lowest-cost edge
		cheapest_cost = min(edge_dict.keys())
		#print cheapest_cost

		#choose an edge from the cheapest bin
		node1, node2 = edge_dict[cheapest_cost].pop(0)
		if len(edge_dict[cheapest_cost]) == 0: #if this bin is now empty, delete it
			del edge_dict[cheapest_cost]
		
		#check to make sure nodes are not in same CC
		if not union_find.array[node_to_id[node1]].leader == union_find.array[node_to_id[node2]].leader:
			if not edge_dict: #determine maximum distance: by definition, maximum distance is the next edge we would have added
				return union_find.cc_count
			else:
				union_find.union(node_to_id[node1], node_to_id[node2])

FILENAME = "clustering_test_small.txt"
node_list = problem2_reader(FILENAME)
print node_list
node_to_id, union_find = load_union_find(node_list)
print node_to_id
edge_dict = build_edge_dict(node_list)
print edge_dict
print problem_2(edge_dict, union_find, node_to_id)

#################
### TEST CODE ###
#################

# uf = UnionFind()
# for i in range(10):
# 	uf.add_node(Node())

# for i in range(10):
# 	print uf.array[i].cc_size

# print ""
# print uf.cc_count

# print "" 
# uf.union(1,2)

# for i in range(10):
# 	print uf.array[i].cc_size

# print ""
# print uf.cc_count

# print ""
# uf.union(0,1)

# for i in range(10):
# 	print uf.array[i].cc_size

# print ""
# print uf.cc_count

# print ""
# uf.union(0,8)

# for i in range(10):
# 	print uf.array[i].cc_size

# print ""
# print uf.cc_count
