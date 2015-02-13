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
	All nodes of graph must be listed as keys in the graph dictionary."""
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
	"""Use BFS to find the shortest path between start node and all other nodes."""
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
	"""Use BFS to find all connected components in an undirected graph."""
	if not explored:
		explored = [False for dummy in range(graph.count_nodes())]

	pass



###################################################
############# DEPTH-FIRST ALGORITHMS ##############
###################################################

def dfs(graph, start_node, searched = []):
	"""Recursive depth-first search algorithm. Requires a LIFO stack
	data structure."""
	#print start_node
	if not searched:
		searched = [False for dummy in range(graph.count_nodes())]

	searched[start_node-1] = True
	for outgoing_edge in graph.get(start_node):
		if not searched[outgoing_edge-1]:
			dfs(graph, outgoing_edge, searched)
	return [idx+1 for idx in range(len(searched)) if searched[idx]]


###################################################

test_graph = gc.AdjacencyGraph({1: [2,3], 2: {4, 5}, 3: [6, 7], 4: [], 5: [], 6: [], 7 : []})
print bfs(test_graph, 1)
print dfs(test_graph, 1)
print bfs_shortestpath(test_graph, 1)