import math
import itertools
import os
import time

def all_binary_strings(length):
	#print sorted(["".join(seq) for seq in itertools.product("01", repeat=length)])
	return ["".join(seq) for seq in itertools.product("01", repeat=length)]

def subsets(mySet):
	"""Take a list of elements and return all permutations of that list,
	including the empty list and the original list."""
	return reduce(lambda z, x: z + [y + [x] for y in z], mySet, [[]])

def ts_reader(filename):
	graph_dict = {}
	with open(filename,'r') as fo:
		for idx, line in enumerate(fo):
			if idx:
				graph_dict[idx-1] = [float(item) for item in line.split()]
	return graph_dict


class TravelingSalesman(object):

	def __init__(self, graph_dict):
		self.graph_dict = graph_dict #hash of node : (x coord, y coord); nodes are indexed from zero
		self.n_nodes = len(self.graph_dict.keys())
		self.build_subsets()
		self.build_array()

	def cost(self, node1, node2):
		"""Return euclidean distance between two nodes"""
		x1, y1 = self.graph_dict[node1]
		x2, y2 = self.graph_dict[node2]
		return math.sqrt((y1-y2)**2 + (x1-x2)**2)
	
	def build_subsets(self):
		self.subset_to_integer = {tuple(sorted(item+[0])) : idx for idx, item in enumerate(subsets([i for i in range(1,self.n_nodes)]))}


		self.integer_to_subset = dict((v, k) for (k, v) in self.subset_to_integer.items())

		# self.subsets_containing_node = {i : [] for i in range(self.n_nodes)} #allows us to know which subsets contain given nodes
		# for subset in self.subset_to_integer.keys():
		# 	for node in subset:
		# 		self.subsets_containing_node[node].append(self.subset_to_integer[subset])
		# del self.subsets_containing_node[0]

		self.subsets_by_size = {i : [] for i in range(1,self.n_nodes+1)} #maps size of subsets : integer IDs of subsets of that size
		for subset in self.subset_to_integer.keys():
			self.subsets_by_size[len(subset)].append(self.subset_to_integer[subset])

	def build_array(self):
		#A will be a 2D array indexed by subsets of nodes that contain 0, and subsets
		#j = {1,2,...,n}
		self.array = [[None for dummy1 in range(self.n_nodes)] for dummy2 in range(len(self.integer_to_subset.keys()))]
		for row_index in range(len(self.integer_to_subset.keys())):
			self.array[row_index][0] = float("inf")
		self.array[self.subset_to_integer[(0,)]][0] = 0

	def solve(self):
		for subproblem_size in range(2,self.n_nodes+1):
			for subset_id in self.subsets_by_size[subproblem_size]:
				for subset in self.integer_to_subset[subset_id]:
					if not subset == 0:
						subset_without_dest = [i for i in self.integer_to_subset[subset_id] if not i == subset]
						subset_without_dest = tuple(subset_without_dest)
						subsetid_without_dest = self.subset_to_integer[subset_without_dest]

						recurrence_array = [self.array[subsetid_without_dest][k] + self.cost(k, subset) for k in subset_without_dest]
						self.array[subset_id][subset] = min(recurrence_array)

		#return self.array
		final_subset_id = self.subsets_by_size[self.n_nodes][0]
		#return self.array[final_subset_id]
		return min([self.array[final_subset_id][j] + self.cost(j,0) for j in range(2,self.n_nodes)])

class TravelingSalesmanBinary(TravelingSalesman):

	def __init__(self, graph_dict, filename):
		self.graph_dict = graph_dict #hash of node : (x coord, y coord); nodes are indexed from zero
		self.n_nodes = len(self.graph_dict.keys())
		self.build_subsets()
		self.build_cost_dict()
		#self.build_array(filename)

	def build_subsets(self):
		#self.subset_to_integer = {'1'+item[::-1] : int(item,2) for item in all_binary_strings(self.n_nodes - 1)}
		self.subset_array = []
		formatting = '{0:'+str(self.n_nodes-2)+'b}'
		#print 2**(self.n_nodes-1)
		for int10 in range(2**(self.n_nodes - 2)):
			bin = formatting.format(int10)
			if len(bin.split()[0]) < self.n_nodes - 2:
				bin = '0'*(self.n_nodes - 2 - len(bin.split()[0])) + bin.split()[0]
			self.subset_array.append('11'+bin[::-1])

		print "subarray", len(self.subset_array)

		#print self.subset_array[0:100]
		#self.integer_to_subset = dict((v, k) for (k, v) in self.subset_to_integer.items())
		self.subsets_by_size = {i : [] for i in range(1,self.n_nodes+1)} #maps size of subsets : integer IDs of subsets of that size
		for subset in self.subset_array:
			#print subset, subset.count("1"), self.subset_to_index(subset)
			self.subsets_by_size[subset.count("1")].append(self.subset_to_index(subset))

		#print self.subset_array
		#print self.subsets_by_size

	def build_cost_dict(self):
		self.cost_dict = {}
		for node1 in range(self.n_nodes):
			self.cost_dict[node1] = []
			for node2 in range(self.n_nodes):
				self.cost_dict[node1].append(self.cost(node1, node2))

	def subset_to_index(self, subset):
		binary = subset[2::]
		binary = binary[::-1]
		integer = int(binary, 2)
		#print 'binint', binary, integer
		return integer

	def build_array(self, filename):
		#A will be a 2D array indexed by subsets of nodes that contain 0, and subsets
		#j = {1,2,...,n}
		counter = 0
		with open(filename, 'w') as fo:
			while counter < len(self.subset_array):
				if counter == 0:
					line = [str(counter),'0']
				else:
					line = [str(counter),"inf"]
				while len(line) < self.n_nodes+1:
					line.append("NaN")
				#print line
				fo.write("\t".join(line))
				fo.write('\n')
				counter += 1

	def add_to_array(self, item):
		try:
			self.array.keys()[0]
		except:
			self.array = {}

		if item == 0:
			line = [0, self.cost(0,1)]
		else:
			line = [float('inf')]
		while len(line) < self.n_nodes:
				line.append("NaN")
		self.array[item] = line


	def solve3(self):
		"""Rather than caching results in a file, simply store the previous subproblem only."""
		#print self.subsets_by_size
		#create initial array
		#print self.subset_array[4516448]
		#print 4516448 in self.subsets_by_size[11]
		self.add_to_array(0)
		cycletime = time.time()

		for subproblem_size in range(3, self.n_nodes+1):
			print subproblem_size, len(self.subsets_by_size[subproblem_size]), time.time() - cycletime
			#for i in self.subsets_by_size[subproblem_size]:
				#print self.subset_array[i]

			cycletime = time.time()
			#go back through the subsets
			for subset_id in self.subsets_by_size[subproblem_size]:
				self.add_to_array(subset_id)

				subset = self.subset_array[subset_id]
				
				#return self.array
				for j, bit in enumerate(subset):
						
						if not j==0 and not j==1 and int(bit):
							
							minimum = float("inf")
							subset_without_j = subset[0:j]+"0"+subset[j+1::]
							subset_without_j_id = self.subset_to_index(subset_without_j)


							for k, bit in enumerate(subset_without_j):
								if int(bit) and not k==j:
									
									try:
										current = float(self.array[subset_without_j_id][k]) + self.cost_dict[k][j]
									except:
										current = self.cost_dict[k][j]
										print "error caught: key", subproblem_size, subset_without_j_id, k
									
									if current < minimum:
										minimum = current

							self.array[self.subset_to_index(subset)][j] = minimum
			#print self.array
			for subset_id in self.subsets_by_size[subproblem_size - 1]:
				del self.array[subset_id]


			#put the lines back into the file - not all are actually needed, can work this out later

			#return

		final_subset_id = self.subsets_by_size[self.n_nodes][0]
		
		minimum = float("inf")
		#return self.array
		#print self.array			
		for j in range(2,self.n_nodes):
			try: 
				float(self.array[final_subset_id][j])				
				if self.array[final_subset_id][j] + self.cost(j,0) < minimum:
					minimum = self.array[final_subset_id][j] + self.cost(j,0)
			except TypeError:
				pass
		
		return minimum		

	def solve2(self, filename):
		self.build_array(filename)
		#build the initial array
		# with open(filename, 'w') as fo:
		# 	line = [str(0)]
		# 	while len(line) < self.n_nodes+1:
		# 		line.append("NaN")
		# 	fo.write("\t".join(line))
		# 	fo.write("\n")

		#iterate through subproblem sizes
		for subproblem_size in range(2, self.n_nodes+1):
			print subproblem_size


			for subset_id in self.subsets_by_size[subproblem_size]:
				#now have an integer index representing the subset
				subset = self.subset_array[subset_id]

				if not subset == "1"+"0"*(self.n_nodes - 1):

					lines_to_extract.append(subset_id)

					#find position of j's and the subsets without j
					j_indices = []
					subsets_without_j = []

					for idx, bit in enumerate(subset):

						if idx!=0 and int(bit):
							j_indices.append(idx) #keep track of j
							subset_without_j = subset[0:idx]+"0"+subset[idx+1::] #remove j from the current subset
							subsets_without_j.append(subset_without_j)
							lines_to_extract.append(self.subset_to_index(subset_without_j)) #need A[S-{j}][k]

					sub_dict[subset] = (j_indices, subsets_without_j)

			#pull out the lines we need
			line_dict = {}

			ftemp = open("tempfile.txt", "w")
			with open(filename, 'r') as fo:
				for line in fo:
					if int(line.split()[0]) in lines_to_extract:
						line_dict[int(line.split()[0])] = line.split()[1::]
					else:
						ftemp.write(line)
			ftemp.close()


			subproblems_to_delete = set([])
			#go back through the subsets
			for subset_id in self.subsets_by_size[subproblem_size]:

				subset = self.subset_array[subset_id]
				
				if not subset == "1" + "0"*(self.n_nodes - 1):
					
					for j, bit in enumerate(subset):
						
						if j!=0 and int(bit):
							
							minimum = float("inf")
							subset_without_j = subset[0:j]+"0"+subset[j+1::]
							subset_without_j_id = self.subset_to_index(subset_without_j)

							subproblems_to_delete = subproblems_to_delete.union(set([subset_without_j_id]))

							for k, bit in enumerate(subset_without_j):
								if int(bit) and not k==j:
									
									current = float(line_dict[subset_without_j_id][k]) + self.cost(k,j)
									
									if current < minimum:
										minimum = current

							line_dict[self.subset_to_index(subset)][j] = str(minimum)

			#put the lines back into the file - not all are actually needed, can work this out later
			for to_del in subproblems_to_delete:
				del line_dict[to_del]
			
			ftemp = open("tempfile.txt", "a")
			for index in line_dict.keys():
				line = line_dict[index]
				str_line = "\t".join(line)
				str_line = str(index)+'\t'+str_line
				ftemp.write(str_line)
				ftemp.write("\n")
			ftemp.close()
			os.remove(filename)
			for tfilename in os.listdir("."):
				if tfilename.startswith("temp"):
					os.rename(tfilename, filename)
			#return

		final_subset_id = self.subsets_by_size[self.n_nodes][0]
		
		minimum = float("inf")
		with open(filename, 'r') as fo:
			for idx, line in enumerate(fo):
				if int(line.split()[0]) == final_subset_id:
					
					target_line = line.split()
					target_line = target_line[1::]
					
					for j in range(2,self.n_nodes):
						
						if float(target_line[j]) + self.cost(j,0) < minimum:
							minimum = float(target_line[j]) + self.cost(j,0)
		
		return minimum


testgraph_rect = {i : [0,i] for i in range(5)}
for j in range(9,4,-1):
	testgraph_rect[j] = [1,j-5]
#print testgraph_rect

testgraph_linear = {i: [0,i] for i in range(4)}
#print testgraph_linear

graph = ts_reader("tsp.txt")
#ts = TravelingSalesmanBinary(testgraph_rect)
ts = TravelingSalesmanBinary(graph, "memo.txt")
print "data structures built"
print ts.solve3()

