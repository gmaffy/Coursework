"""Week 1 of Stanford's Algorithms: Design & Analysis II w/
Tim Roughgarden.

Greedy Algorithm design paradigm
Prim's minimum spanning tree Algorithm
"""

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

class Graph(object):
	"""Undirected graph data structure."""
	def __init__(self):
		self.nodes = set([])
		self.edges = []
		self.edges_by_outnode = {}
		self.best_incoming_edge = {} #store the lowest-cost edge incident to each node

	def add_edge(self, edge):
		"""Edge should be a 3-tuple of (start node, end node, cost)."""
		in_node, out_node, cost = edge
		self.nodes.add(in_node)
		self.nodes.add(out_node)
		self.edges.append(edge)

		if out_node in self.edges_by_outnode.keys():
			self.edges_by_outnode[out_node].append(edge)
		else:
			self.edges_by_outnode[out_node] = [edge,]

		if out_node in self.best_incoming_edge.keys():
			if cost < self.best_incoming_edge[out_node]:
				self.best_incoming_edge[out_node] = cost
		else:
			self.best_incoming_edge[out_node] = cost

def prob3_reader(filename):
	"""Convert a file with the format:
	[number_of_nodes] [number_of_edges]
	[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
	[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
	...

	to an undirected graph useable in Prim's Algorithm."""
	pass


if __name__ == "__main__":

	# d = prob1_prioritydict([Job(10,5), Job(6,1), Job(25,20), Job(7,2), Job(100,95), Job(5,0)])
	# for key in d.keys():
	# 	print key, [i.weight for i in d[key]]

	print "Problem 1: "
	jobs = prob1_reader('jobs.txt')	
	print prob1_scheduler(prob1_prioritydict(jobs))

	print "Problem 2: "
	print prob2_scheduler(prob2_prioritydict(jobs))
