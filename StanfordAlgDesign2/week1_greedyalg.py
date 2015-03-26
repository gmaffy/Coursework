"""Week 1 of Stanford's Algorithms: Design & Analysis II w/
Tim Roughgarden.

Greedy Algorithm design paradigm
Prim's minimum spanning tree Algorithm
"""

#PROBLEM 1
#GREEDY ALGORITHM FOR MINIMIZING WEIGHTED SUM OF COMPLETION TIMES OF TASKS

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
	product of the length and weight of each job. If multiple jobs have the same 
	product, arrange them in increasing order of weight."""
	priority_dict = {}

	for job in job_array:
		product = job.weight * job.length

		if product in priority_dict.keys():
			counter = len(priority_dict[product])
			for idx in range(len(priority_dict[product])): #insert new job in increasing order of weight
				if job.weight < priority_dict[product][idx].weight:
					counter = idx
					break
			#print job.weight, counter
			priority_dict[product].insert(counter, job)
				
		else:
			priority_dict[product] = [job,]

	return priority_dict

def prob1_scheduler(priority_dict):
	"""Input a hash table of {product: (weight, length),...}
	where within a given bin, jobs with equivalent product are sorted
	in increasing order of weight.

	Schedule jobs in decreasing order of weight * length, breaking ties
	by scheduling higher-weight jobs first. Not guaranteed to be correct.
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
	ratio of the weight to length of each job. If multiple jobs have the same 
	product, arrange them in increasing order of weight."""
	priority_dict = {}

	for job in job_array:
		ratio = job.weight / job.length

		if ratio in priority_dict.keys():
			counter = len(priority_dict[ratio])
			for idx in range(len(priority_dict[ratio])): #insert new job in increasing order of weight
				if job.weight < priority_dict[ratio][idx].weight:
					counter = idx
					break
			#print job.weight, counter
			priority_dict[ratio].insert(counter, job)

			#priority_dict[ratio].append(job)
				
		else:
			priority_dict[ratio] = [job,]

	return priority_dict

def prob2_scheduler(priority_dict):
	"""Input a hash table of {product: (weight, length),...}
	where within a given bin, jobs with equivalent product are sorted
	in increasing order of weight.

	Schedule jobs in decreasing order of weight * length, breaking ties
	by scheduling higher-weight jobs first. Guaranteed to be correct.
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

if __name__ == "__main__":

	print "Problem 1: "
	jobs = prob1_reader('jobs.txt')	
	print prob1_scheduler(prob1_prioritydict(jobs))

	print "Problem 2: "
	print prob2_scheduler(prob2_prioritydict(jobs))
