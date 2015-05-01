


class two_sat_graph(object):

	def __init__(self, sat_instance_file):
		self.n_vars, self.edges, self.nodes = self.parse_file(sat_instance_file)
		#self.edges, self.nodes = self.testparse(sat_instance_file)
		self.adjacency_dict()
		print self.n_vars

	def testparse(self, filename):
		edge_list = []
		nodes = []
		with open(filename, 'r') as fo:
			for idx, line in enumerate(fo):
				if not idx:
					pass
				else:
					head, tail = int(line.split()[0]), int(line.split()[1])
					edge_list.append((head, tail))
					nodes.append(head)
					nodes.append(tail)

		return edge_list, list(set(nodes))

	def parse_file(self, filename):
		n_vars = 0
		edges = []
		nodes = []
		with open(filename) as fo:
			for idx, line in enumerate(fo):
				if idx == 0:
					n_vars = int(line.split()[0])
				else:
					a, b = [int(i) for i in line.split()]
					edges.append((-a, b))
					edges.append((-b, a))
					nodes.extend([-a, b, -b, a])

		assert len(edges) == 2 * n_vars
		return n_vars, edges, nodes

	def adjacency_dict(self):
		"""Construct adjacency dict representation of graph, given list of tuples of (tail node, head node)"""
		self.adjacency_dict = {}
		for head, tail in self.edges:
			try:
				self.adjacency_dict[head].append(tail)
			except KeyError:
				self.adjacency_dict[head] = [tail,]

	def get(self, node):
		return self.adjacency_dict[node]

	def reverse_get(self, node):
		"""Return any nodes that have directed edges into the target node.
		Useful for finding strongly connected components."""
		reverse_nodes = []
		for key in self.adjacency_dict.keys():
			if node in self.adjacency_dict[key]:
				reverse_nodes.append(key)
		return reverse_nodes

	def dfs_loop_firstpass(self):
		self.t = 0
		self.finishing_times = [0 for node in self.nodes]
		self.searched = {node : False for node in self.nodes}
		for node in self.nodes:

			if not self.searched[node]:
				self.dfs_kosaraju_rev(node)

		print self.finishing_times

	def dfs_kosaraju_rev(self, node):
		#assert len(searched) == graph.count_nodes() #searched should always be passed in from the enclosing namespace
		self.searched[node] = True
		for outgoing_edge in self.reverse_get(node):
			if not self.searched[outgoing_edge]:
				self.dfs_kosaraju_rev(outgoing_edge)
				
		self.t+=1
		self.finishing_times[self.nodes.index(node)] = self.t

	def dfs_loop_secondpass(self):
		self.leaders = [None for dummy in self.nodes] #indices have same order as nodes in self.nodes
		self.searched = {node : False for node in self.nodes}
		#iterate through nodes in reverse order of finishing time
		for fin_time in range(len(self.nodes), 0, -1):
			node_index = self.finishing_times.index(fin_time)
			node = self.nodes[node_index]
			if not self.searched[node]:
				self.leader = self.nodes[node]
				self.dfs_kosaraju_fwd(node)
		return self.leaders

	def dfs_kosaraju_fwd(self, node):
		self.searched[node] = True
		self.leaders[self.nodes.index(node)] = self.leader
		for outgoing_edge in self.get(node):
			if not self.searched[outgoing_edge]:
				self.dfs_kosaraju_fwd(outgoing_edge)

	def kosaraju_twopass(self):
		"""Compute the sizes of strongly connected components in a directed graph, in descending order"""
		self.dfs_loop_firstpass() #computes magical ordering, stored in self.finishing_times
		self.dfs_loop_secondpass() #uses ordering to assign a leader to each node, stored in self.leaders
		
		#group nodes by their leaders
		self.leader_to_nodes = {}
		for idx, node in enumerate(self.nodes):
			try:
				self.leader_to_nodes[self.leaders[idx]].append(node)
			except KeyError:
				self.leader_to_nodes[self.leaders[idx]] = [node,]

		return self.leader_to_nodes

	def check_feasible(self):
		self.kosaraju_twopass()
		for leader in self.leader_to_nodes.keys():
			for node in self.leader_to_nodes[leader]:
				if -node in self.leader_to_nodes:
					return False
		return True

def multicheck(list_of_filenames):
	bool_string = ""
	for filename in list_of_filenames:
		tsg = two_sat_graph(filename)
		result = tsg.check_feasible()
		if result:
			bool_string += "1"
		else:
			bool_string += "0"
	return bool_string

list_of_filenames = ["2sat1.txt", "2sat2.txt", "2sat3.txt", "2sat4.txt", "2sat5.txt", "2sat6.txt"]
print multicheck(list_of_filenames)

if __name__ == "__main__":
	list_of_filenames = ["2sat1.txt", "2sat2.txt", "2sat3.txt", "2sat4.txt", "2sat5.txt", "2sat6.txt"]
	print multicheck(list_of_filenames)


