import math
import itertools
import os

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
		self.build_array(filename)

	def build_subsets(self):
		#self.subset_to_integer = {'1'+item[::-1] : int(item,2) for item in all_binary_strings(self.n_nodes - 1)}
		self.subset_array = []
		formatting = '{0:'+str(self.n_nodes-1)+'b}'
		#print 2**(self.n_nodes-1)
		for int10 in range(2**(self.n_nodes - 1)):
			bin = formatting.format(int10)
			if len(bin.split()[0]) < self.n_nodes - 1:
				bin = '0'*(self.n_nodes - 1 - len(bin.split()[0])) + bin.split()[0]
			self.subset_array.append('1'+bin[::-1])

		#print self.subset_array[0:100]
		#self.integer_to_subset = dict((v, k) for (k, v) in self.subset_to_integer.items())
		self.subsets_by_size = {i : [] for i in range(1,self.n_nodes+1)} #maps size of subsets : integer IDs of subsets of that size
		for subset in self.subset_array:
			#print subset, subset.count("1"), self.subset_to_index(subset)
			self.subsets_by_size[subset.count("1")].append(self.subset_to_index(subset))

		#print self.subset_array
		#print self.subsets_by_size

	def subset_to_index(self, subset):
		binary = subset[1::]
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


	def solve2(self, filename):

		#iterate through subproblem sizes
		for subproblem_size in range(2, self.n_nodes+1):

			lines_to_extract = []
			sub_dict = {}

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

			#go back through the subsets
			for subset_id in self.subsets_by_size[subproblem_size]:

				subset = self.subset_array[subset_id]
				print subset
				if not subset == "1" + "0"*(self.n_nodes - 1):
					
					for j, bit in enumerate(subset):
						
						if j!=0 and int(bit):
							print j
							minimum = float("inf")
							subset_without_j = subset[0:j]+"0"+subset[j+1::]
							subset_without_j_id = self.subset_to_index(subset_without_j)

							for k, bit in enumerate(subset_without_j):
								if int(bit) and not k==j:
									print k

									current = float(line_dict[subset_without_j_id][k]) + self.cost(k,j)
									print current
									if current < minimum:
										minimum = current

							line_dict[self.subset_to_index(subset)][j] = str(minimum)

			#put the lines back into the file - not all are actually needed, can work this out later
			print line_dict
			
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



				



	def solve(self, filename):
		for subproblem_size in range(2,self.n_nodes+1):
			print subproblem_size
			dest_dict = {}
			relevant_lines = []
			
			for subset_id in self.subsets_by_size[subproblem_size]:
				relevant_lines.append(subset_id)
				#print subset_id
				subset = self.subset_array[subset_id]

				if not subset == "1"+"0"*(self.n_nodes - 1):

					subsets_without_j = [subset[0:j_idx]+"0"+subset[j_idx+1::] for j_idx, bit in enumerate(subset) if int(bit) and not j_idx == 0]
					j_indices = [j_idx for j_idx, bit in enumerate(subset) if int(bit) and not j_idx == 0]
					subsetids_without_j = [self.subset_to_index(subset_without_j) for subset_without_j in subsets_without_j]
					subsets_without_j, j_indices, subsetids_without_j = [i for i in reversed(subsets_without_j)], [i for i in reversed(j_indices)], [i for i in reversed(subsetids_without_j)]
					relevant_lines.extend(subsetids_without_j)

				dest_dict[subset] = (subsets_without_j, j_indices, subsetids_without_j)


			#at this point, have all subsets pointing to their sublocations
			#now, can pull out the relevant lines from the file

			file_dict = {}
			ftemp = open('tempfile.txt', 'w')
			with open(filename, 'r') as fo:
				for line in fo:
					idx = int(line.split()[0])
					if idx in relevant_lines:
						processed_line = line.split()
						file_dict[idx] = line.split()[1::]
					else:
						ftemp.write(line)
			ftemp.close()

			to_add_back = []

			for original in reversed(sorted(dest_dict.keys())):
				current_row_id = self.subset_to_index(original)
				current_row = file_dict[current_row_id]
				
				subsets_without_j, j_indices, subsetids_without_j = dest_dict[original]

				for ID, subset in enumerate(subsets_without_j):
					recurrence = (float('inf'), None, None)
					for k, kbit in enumerate(subset):
						if kbit and not k==j_indices[ID]:

							j_idx = j_indices[ID]
							data = file_dict[subsetids_without_j[ID]]
							current_recurrence = float(data[k])+self.cost(k, j_idx)

							if current_recurrence < recurrence[0]:
								recurrence = (current_recurrence, ID, j_indices[ID])

					current_row[recurrence[2]] = str(recurrence[0])
					if len(current_row) < self.n_nodes + 1:
						current_row = [str(current_row_id)]+current_row
				to_add_back.append('\t'.join(current_row))
				

			with open('tempfile.txt','a') as fo:
				for r in to_add_back:
					fo.write(r)
					fo.write('\n')

			os.remove(filename)
			for tfilename in os.listdir("."):
				if tfilename.startswith("temp"):
					os.rename(tfilename, filename)


		
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
print testgraph_rect

testgraph_linear = {i: [0,i] for i in range(4)}
print testgraph_linear

if __name__ == "__main__":
	#x = sorted(all_binary_strings(24))
	#subset_to_integer = {'1'+item[::-1] : int(item,2) for item in all_binary_strings(25 - 1)}
	#print x[0:100]
	graph = ts_reader("tsp.txt")
	#ts = TravelingSalesmanBinary(testgraph_rect)
	ts = TravelingSalesmanBinary(testgraph_rect, "memo.txt")
	print "data structures built"
	print ts.solve2("memo.txt")