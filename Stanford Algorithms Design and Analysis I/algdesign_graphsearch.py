"""Code for Week 4 of Stanford Algorithms: Design & Analysis I:
Graph search and Kosaraju's Two-Pass Algorithm.

Assumes adjacency list representation of graph, encapsulated
as an AdjacencyGraph object as defined in algdesign_graphcontract."""

###################################################

import algdesign_graphcontract as gc

###################################################

class Queue(object):
	"""FIFO array data structure"""
	def __init__(self, array = []):
		self.array = array

	def empty(self):
		return len(self.array) == 0

	def enqueue(self, item):
		self.array.append(item)

	def dequeue(self):
		if not self.empty():
			return self.array.pop(0)
		else:
			print "Queue is empty"

###################################################


###################################################
############ BREADTH-FIRST ALGORITHMS #############
###################################################

def bfs(graph, start_node):
	"""Iterative breadth-first search algorithm. Requires a FIFO queue
	data structure. Nodes of graph must be consecutive positive integers [1,n].
	All nodes of graph must be listed as keys in the graph dictionary.
	Returns list of nodes reachable from start node"""
	searched = [False for dummy in range(graph.count_nodes())]
	search_queue = Queue()
	search_queue.enqueue(start_node)
	while not search_queue.empty():
		current_node = search_queue.dequeue()
		#print current_node
		searched[current_node-1] = True #current_node - 1 b/c array is indexed from 0 but nodes are indexed from 1
		for outgoing_edge in graph.get(current_node):
			if not searched[outgoing_edge-1]:
				search_queue.enqueue(outgoing_edge)
				searched[outgoing_edge-1] = True
	return [idx+1 for idx in range(len(searched)) if searched[idx]]

def bfs_shortestpath(graph, start_node):
	"""Use BFS to find the shortest path between start node and all other nodes.
	Returns list of path lengths from start node to all other nodes."""
	dist = [0 if e+1 == start_node else float('inf') for e in range(graph.count_nodes())]
	searched = [False for dummy in range(graph.count_nodes())]
	search_queue = Queue()
	search_queue.enqueue(start_node)
	while not search_queue.empty():
		current_node = search_queue.dequeue()
		searched[current_node-1] = True #current_node - 1 b/c array is indexed from 0 but nodes are indexed from 1
		for outgoing_edge in graph.get(current_node):
			if not searched[outgoing_edge-1]:
				search_queue.enqueue(outgoing_edge)
				searched[outgoing_edge-1] = True
				dist[outgoing_edge-1] = dist[current_node-1]+1
	return dist

def find_undirected_CCs(graph, explored = []):
	"""Use BFS to find all connected components in an undirected graph.
	Return list of lists of nodes, where each list of nodes is a connected
	componenet of the graph."""
	if not explored:
		explored = [False for dummy in range(graph.count_nodes())]
	cc_list = []
	for idx, node in enumerate(explored):
		if not node:
			new_cc = bfs(graph, idx+1)
			cc_list.append(new_cc)
			for item in new_cc:
				explored[item-1] = True
	return cc_list

###################################################
############# DEPTH-FIRST ALGORITHMS ##############
###################################################

def dfs(graph, start_node, searched = []):
	"""Recursive depth-first search algorithm. Requires a LIFO stack
	data structure. Returns list of nodes accessible from start node."""
	#print start_node
	if not searched:
		searched = [False for dummy in range(graph.count_nodes())]

	searched[start_node-1] = True
	for outgoing_edge in graph.get(start_node):
		if not searched[outgoing_edge-1]:
			dfs(graph, outgoing_edge, searched)

	return [idx+1 for idx in range(len(searched)) if searched[idx]]

def dfs_modified(graph, start_node, searched = [], topology = [], current_label = 0):
	"""Special version of DFS to be used for topological sort."""
	#no return value needed since we are only modifying provided lists
	searched[start_node-1] = True
	for outgoing_edge in graph.get(start_node):
		if not searched[outgoing_edge-1]:
			dfs_modified(graph, outgoing_edge, searched, topology, current_label-1)
	topology[start_node - 1] = current_label
	current_label -= 1

def dfs_topological(graph):
	"""Returns the topological ordering of nodes in a DAG, where n is the first node
	in the sequence and 1 is the final node."""
	searched = [False for dummy in range(graph.count_nodes())]
	topology = [None for dummy in range(graph.count_nodes())]
	current_label = graph.max_node()
	for idx, node in enumerate(searched):
		if not node:
			dfs_modified(graph, idx+1, searched, topology, current_label)
	return topology

###################################################
########## KOSARAJU'S TWO-PASS ALGORITHM ##########
###################################################

t, s = 0, None

def dfs_loop(graph):
	global t
	global s
	


def dfs_kosaraju_rev(graph, node, searched = [], leader = []):
	if not searched:
		searched = [False for dummy in range(graph.count_nodes())]
	leader[node-1] = node
	pass


###################################################

test_graph = gc.AdjacencyGraph({1: [2,3], 2: {4, 5}, 3: [6, 7], 4: [], 5: [], 6: [], 7 : [], 8: [9], 9: [8], 10: [], 11: [12], 12: [11, 13], 13: [12]})
print bfs(test_graph, 1)
print dfs(test_graph, 1)
print bfs_shortestpath(test_graph, 1)
print find_undirected_CCs(test_graph)

test_dag = gc.AdjacencyGraph({1: [3], 2: [5], 3: [2], 4: [], 5: [4]})
print dfs_topological(test_dag)