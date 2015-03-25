"""Week 1 of Stanford's Algorithms: Design & Analysis II w/
Tim Roughgarden.

Greedy Algorithm design paradigm
Prim's minimum spanning tree Algorithm
"""

#PROBLEM 1
#GREEDY ALGORITHM FOR MINIMIZING WEIGHTED SUM OF COMPLETION TIMES OF TASKS

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
				job_array.append((int(weight), int(length)))
	return job_array

def prob1(job_array):
	"""Input an array of jobs (weight, length).
	Schedule jobs in decreasing order of weight * length, breaking ties
	by scheduling higher-weight jobs first. Not guaranteed to be correct.
	Return sum of weighted completion times of the resulting schedule."""
	


if __name__ == "__main__":
	jobs = prob1_reader('jobs.txt')

