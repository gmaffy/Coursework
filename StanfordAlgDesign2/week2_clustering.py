
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

def greedy_k_clustering(k, edge_dict, node_count):

	#load all nodes into union find
	union_find = UnionFind()
	for i in range(node_count):
		union_find.add_node(Node())
	
	while union_find.cc_count > k:

		#find the lowest-cost edge
		cheapest_cost = min(edge_dict.keys())

		#choose an edge from the cheapest bin
		node1, node2 = edge_dict[cheapest_cost].pop()
		if len(edge_dict[cheapest_cost]) == 0: #if this bin is now empty, delete it
			del edge_dict[cheapest_cost]

		#check to make sure nodes are not in same CC
		if not union_find.array[node1-1].leader == union_find.array[node2-1].leader:
			union_find.union(node1-1, node2-1)

edge_dict = hashify(problem1_reader("clustering1.txt"))
print len(edge_dict)
print min(edge_dict.keys())

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
