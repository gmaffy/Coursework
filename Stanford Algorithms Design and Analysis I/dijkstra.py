"""Implementation of Dijkstra's Shortest Path Algorithm (1959) to find the lowest-cost path
between a source vertex and all other vertices in a graph. Each edge has an associated
non-negative weight or cost."""


##############################################
############## DATA STRUCTURES ###############
##############################################

class DijkstraMinHeap(object):
	"""Heap data structure to hold information relevant to Dijkstra's shortest path algorithm.
	Object stored in heap are two-element pairs of (node, distance from source)."""
	def __init__(self):
		self.array = [] #list of (node, distance from source)
		self.root = None

	def __str__(self):
		return str(self.array)

	def insert(self, item):
		self.array.append(item) #add item as leftmost leaf
		child_index = len(self.array) - 1
		parent_index = self.get_parent(child_index)
		while not self.check_heap_property(child_index, parent_index): #check whether heap invariant is violated
			self.swap(child_index, parent_index) #if so, bubble the leaf up toward the root
			child_index = parent_index
			parent_index = self.get_parent(child_index)

	def extract_min(self):
		self.swap(0, len(self.array)-1) #switch the root with the last leaf
		minimum = self.array.pop() #remove the former root from the end of the array so it can be returned
		parent_index = 0
		children_indices = self.get_children(parent_index)
		while not (self.check_heap_property(children_indices[0], parent_index) and self.check_heap_property(children_indices[1], parent_index)):
			#find minimum of two children, assuming both exist
			if children_indices[1] == None: #node has only one child
				min_child = children_indices[0]
			else: #both children exist
				if self.array[children_indices[0]][1] < self.array[children_indices[1]][1]:
					min_child = children_indices[0]
				else:
					min_child = children_indices[1]

			#bubble the parent down toward the leaves
			self.swap(parent_index, min_child)
			parent_index = min_child
			children_indices = self.get_children(min_child)
			
		return minimum #hand the root to the user

	def get_parent(self, child_index):
		"""Given index of child node, return index of parent node. If the child node
		is the root, return None."""
		if child_index == 0:
			return None
		else:
			return int(child_index/2.0)

	def get_children(self, parent_index):
		children = (2*parent_index+1, 2*parent_index+2)
		if children[0] >= len(self.array):
			return (None, None)
		elif children[1] >= len(self.array):
			return (2*parent_index+1,None)
		else:
			return children

	def swap(self, idx1, idx2):
		new_item_1 = self.array[idx2]
		self.array[idx2] = self.array[idx1]
		self.array[idx1] = new_item_1

	def check_heap_property(self, child_index, parent_index):
		"""Check that the heap invariant is not violated for a pair of indices for child and parent nodes."""
		if child_index == None or parent_index == None:
			return True
		else:
			return self.array[child_index][1] >= self.array[parent_index][1]

	def heapify(self, l):
		"""O(n) method to load an array into an empty heap."""
		assert len(self.array) == 0 #make sure heap is empty
		self.array = sorted(l)


##############################################
####### WEIGHTED GRAPH REPRESENTATION ########
##############################################

class WeightedGraph(object):
	"""Input dictionary keyed with nodes of graph. Values are themselves dictionaries keyed with the
	target node of that node's edges, with values as the weight of that edge."""
	def __init__(self, graph_dict):
		self.nodes = list(graph_dict.keys())
		self.dict = graph_dict

	def get_neighbors(self, vertex):
		return self.dict[vertex].keys()

	def get_weight(self, start_node, target_node):
		return self.dict[start_node][target_node]

def text_to_weightedgraph(filename):

	file_list = []
	with open(filename, 'r') as fo:
		for line in fo:
			file_list.append(line.split())

	graph_dict = {}
	for line in file_list:
		node = int(line.pop(0))
		edges = {}
		for edge in line:
			edges[int(edge[0:edge.index(',')])] = int(edge[edge.index(',')+1::]) #{target node: weight}
		graph_dict[node] = edges

	return WeightedGraph(graph_dict)


##############################################
################## DIJKSTRA ##################
##############################################

def dijkstra(graph, source, arbitrary_maximum = 1000000):
	"""Straightforward O(mn) implementation of Dijkstra's shortest-path algorithm.
	Returns array of distances from source vertex to all other vertices in a weighted
	graph. Distance is arbitrarily set if no path exists."""

	dist_dict = {source: 0} #distance of source to self is 0

	for node in graph.nodes:
		if node != source:
			dist_dict[node] = arbitrary_maximum

	to_explore = [source,]

	while to_explore:
		current = to_explore.pop(0)

		for neighbor in graph.get_neighbors(current):



				alt = dist_dict[current] + graph.get_weight(current, neighbor)

				if alt < dist_dict[neighbor]:
					dist_dict[neighbor] = alt

					to_explore.append(neighbor)

	return dist_dict


def dijkstra_heap(graph, source, arbitrary_maximum = 1000000):
	"""Heap-based implementation of Dijkstra's shortest path algorithm.
	O(m+nlogn) time due to fast extract_min enabled by heap."""
	dist_dict = {source : 0}
	for node in graph.nodes:
		if node != source:
			dist_dict[node] = arbitrary_maximum

	priority_queue = DijkstraMinHeap()
	priority_queue.insert([source, dist_dict[source]]) #place source node as root of min heap

	while priority_queue.array:
		current = priority_queue.extract_min()[0]

		for neighbor in graph.get_neighbors(current):

			alt = dist_dict[current] + graph.get_weight(current, neighbor)

			if alt < dist_dict[neighbor]:
				dist_dict[neighbor] = alt

				priority_queue.insert([neighbor, dist_dict[neighbor]])

	return dist_dict


##############################################
#################### MAIN ####################
##############################################

if __name == __main__:
	wg = text_to_weightedgraph('dijkstraData.txt')
	print dijkstra(wg, 1)
	print dijkstra_heap(wg, 1)