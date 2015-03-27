"""Week 1 of Stanford's Algorithms: Design & Analysis II w/
Tim Roughgarden.

Greedy Algorithm design paradigm
Prim's minimum spanning tree Algorithm
"""

import random

#PROBLEM 1
#SUBOPTIMAL GREEDY ALGORITHM FOR MINIMIZING WEIGHTED SUM OF COMPLETION TIMES OF TASKS


class Job(object):

	def __init__(self, weight, length):
		self.weight = weight
		self.length = length

def prob1_reader(filename):
	"""Read in file of format:
	[number_of_jobs]
	[job_1_weight] [job_1_length]
	[job_2_weight] [job_2_length]
	...
	"""
	job_array = []
	with open(filename, 'r') as fo:
		for idx, line in enumerate(fo):
			if not idx==0:
				weight, length = line.split()
				job_array.append(Job(int(weight), int(length)))
	return job_array

def prob1_prioritydict(job_array):
	"""Given an array of Job objects, load them into a hash table keyed by the
	difference of the weight and length of each job. If multiple jobs have the same 
	difference, arrange them in increasing order of weight."""
	priority_dict = {}

	for job in job_array:
		difference = job.weight - job.length

		if difference in priority_dict.keys():
			counter = 0
			for idx in range(len(priority_dict[difference])): #insert new job in increasing order of weight
				if job.weight > priority_dict[difference][idx].weight:
					counter = idx + 1
					#print job.weight, counter, priority_dict[difference][idx].weight
					#break
			#print job.weight, counter
			priority_dict[difference].insert(counter, job)
				
		else:
			priority_dict[difference] = [job,]

	return priority_dict

def prob1_scheduler(priority_dict):
	"""Input a hash table of {difference: (weight, length),...}
	where within a given bin, jobs with equivalent difference are sorted
	in increasing order of weight.

	Schedule jobs in decreasing order of difference, breaking ties
	by scheduling higher-weight jobs first. Not guaranteed to be optimal.
	Return sum of weighted completion times of the resulting schedule."""
	completion_time = 0
	running_sum = 0

	while priority_dict:

		current_bin = max(priority_dict.keys())

		while priority_dict[current_bin]:

			current_job = priority_dict[current_bin].pop()

			completion_time += current_job.length
			running_sum += completion_time * current_job.weight

		del priority_dict[current_bin]

	return running_sum


#PROBLEM 2
#OPTIMAL GREEDY ALGORITHM FOR MINIMIZING WEIGHTED SUM OF COMPLETION TIMES OF TASKS

def prob2_prioritydict(job_array):
	"""Given an array of Job objects, load them into a hash table keyed by the
	ratio of the weight and length of each job. If multiple jobs have the same 
	ratio, arrange them in increasing order of weight."""
	priority_dict = {}

	for job in job_array:
		ratio = job.weight / float(job.length)

		if ratio in priority_dict.keys():
			counter = 0
			for idx in range(len(priority_dict[ratio])): #insert new job in increasing order of weight
				if job.weight > priority_dict[ratio][idx].weight:
					counter = idx + 1
					#print job.weight, counter, priority_dict[ratio][idx].weight
					#break
			#print job.weight, counter
			priority_dict[ratio].insert(counter, job)
				
		else:
			priority_dict[ratio] = [job,]

	return priority_dict

def prob2_scheduler(priority_dict):
	"""Input a hash table of {ratio: (weight, length),...}
	where within a given bin, jobs with equivalent ratios are sorted
	in increasing order of weight.

	Schedule jobs in decreasing order of ratio, breaking ties
	by scheduling higher-weight jobs first. Not guaranteed to be optimal.
	Return sum of weighted completion times of the resulting schedule."""
	completion_time = 0
	running_sum = 0

	while priority_dict:

		current_bin = max(priority_dict.keys())

		while priority_dict[current_bin]:

			current_job = priority_dict[current_bin].pop()

			completion_time += current_job.length
			running_sum += completion_time * current_job.weight

		del priority_dict[current_bin]

	return running_sum

#PROBLEM 3
#PRIM'S ALGORITHM FOR COMPUTING A MINIMUM SPANNING TREE OF AN UNDIRECTED GRAPH

class WeightedUndirectedEdge(object):
	def __init__(self, node1, node2, cost):
		self.node1 = node1
		self.node2 = node2
		self.cost = cost


class UndirectedGraph(object):

	def __init__(self):
		self.nodes = set([])
		self.hash_by_node = {}
		self.hash_by_cost = {}

	def __str__(self):
		return str(self.hash_by_cost)

	def add_edge(self, edge):
		self.nodes.add(edge.node1)
		self.nodes.add(edge.node2)

		if edge.node1 in self.hash_by_node.keys():
			self.hash_by_node[edge.node1].append((edge.node2, edge.cost))
		else:
			self.hash_by_node[edge.node1] = [(edge.node2, edge.cost),]

		if edge.node2 in self.hash_by_node.keys():
			self.hash_by_node[edge.node2].append((edge.node1, edge.cost))
		else:
			self.hash_by_node[edge.node2] = [(edge.node1, edge.cost),]

		if edge.cost in self.hash_by_cost.keys():
			self.hash_by_cost[edge.cost].append((edge.node1, edge.node2))
		else:
			self.hash_by_cost[edge.cost] = [(edge.node1, edge.node2),]

def prob3_reader(filename):
	"""Convert a file with the format:
	[number_of_nodes] [number_of_edges]
	[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
	[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
	...

	to an undirected graph useable in Prim's Algorithm."""
	graph = UndirectedGraph()

	with open(filename, 'r') as fo:
		for idx, line in enumerate(fo):
			if not idx == 0:
				node1, node2, cost = line.split()
				node1, node2, cost = int(node1), int(node2), int(cost)
				current_edge = WeightedUndirectedEdge(node1, node2, cost)
				graph.add_edge(current_edge)

	return graph

def prims_naive(undir_graph):
	"""O(mn) implementation of Prim's minimum spanning tree algorithm."""

	first_node = random.choice(list(graph.nodes))
	nodes_seen = set([first_node])

	tree = [first_node,]
	total_cost = 0

	while not nodes_seen == graph.nodes:

		#find cheapest edge with one node in nodes_seen and one not
		lowest_cost = float("inf")
		current_node = None
		for cost in graph.hash_by_cost.keys():
			for edge in graph.hash_by_cost[cost]:
				if cost < lowest_cost and (edge[0] in nodes_seen and not edge[1] in nodes_seen):
					lowest_cost = cost
					current_node = edge[1]
				elif cost < lowest_cost and (edge[1] in nodes_seen and not edge[0] in nodes_seen):
					lowest_cost = cost
					current_node = edge[0]
		nodes_seen.add(current_node)
		total_cost += lowest_cost
		tree.append(current_node)

	return total_cost




if __name__ == "__main__":

	# d = prob1_prioritydict([Job(10,5), Job(6,1), Job(25,20), Job(7,2), Job(100,95), Job(5,0)])
	# for key in d.keys():
	# 	print key, [i.weight for i in d[key]]

	print "Problem 1: "
	jobs = prob1_reader('jobs.txt')	
	print prob1_scheduler(prob1_prioritydict(jobs))

	print "Problem 2: "
	print prob2_scheduler(prob2_prioritydict(jobs))

	print "Problem 3: "
	graph = prob3_reader("prims_edges.txt")
	print prims_naive(graph)
