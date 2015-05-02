import math
import time

class two_opt_solver(object):

	def __init__(self, filename):
		self.start = time.time()
		self.parse_filename(filename)
		self.calc_distance()
		self.n_nodes = len(self.nodes_to_coords)
		

	def parse_filename(self, filename):
		self.nodes_to_coords = {}
		#generate dictionary of distances and list of nodes
		with open(filename, 'r') as fo:
			for idx, line in enumerate(fo):
				if not idx:
					pass
				else:
					x, y = float(line.split()[0]), float(line.split()[1])
					self.nodes_to_coords[idx-1] = (x, y)

	def cost(self, node1, node2):
		"""Return euclidean distance between two nodes"""
		x1, y1 = self.nodes_to_coords[node1]
		x2, y2 = self.nodes_to_coords[node2]
		return math.sqrt((y1-y2)**2 + (x1-x2)**2)

	def calc_distance(self):
		try:
			self.nodes_to_coords

			self.dist_dict = {}
			self.tour = []
			for node1 in self.nodes_to_coords.keys():
				self.tour.append(node1)
				self.dist_dict[node1] = {}
				for node2 in self.nodes_to_coords.keys():
					if not node1 == node2:
						self.dist_dict[node1][node2] = self.cost(node1, node2)
			self.tour.append(0)

		except NameError:
			print "Must load TSP instance file with parse_filename() first!"


	def find_path_length(self, path):
		pathlen = 0
		for idx in range(len(path)-1):
			pathlen += self.dist_dict[path[idx]][path[idx+1]]
		return pathlen

		#given a path (list of nodes starting and ending with zero)
		#return the total path length 

	def two_opt_swap(self, path, i, k):
		assert i != 0
		assert i != len(path) - 1 # do not swap the depot
		dec = 0
		new_path = []
		for idx, item in enumerate(path):
			if idx < i:
				new_path.append(item)
			elif idx > k:
				new_path.append(item)
			else:
				new_path.append(path[k - dec])
				dec += 1
		return new_path

	def optimize(self, tolerance = 1000):
		#tolerance = number of rounds allowed with no improvement before return
		improve = 0
		tour = self.tour
		best_distance = self.find_path_length(tour)
		while improve < tolerance:

			for i in range(1,self.n_nodes-1):
				for k in range(i+1, self.n_nodes):
					new_tour = self.two_opt_swap(tour, i, k)
					#print new_tour
					if self.find_path_length(new_tour) < best_distance:
						best_distance = self.find_path_length(new_tour)
						#print best_distance
						tour = new_tour
						improve = 0
					else:
						improve += 1
		self.tour = new_tour
		print time.time() - self.start
		return best_distance



tos = two_opt_solver("tsp.txt")
print tos.optimize()
print tos.tour

