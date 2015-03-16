"""Array implementation of the heap data structure, supporting
insert and extract-min operations in O(logn) time."""

class MinHeap(object):

	def __init__(self):
		self.array = []
		self.root = None

	def __str__(self):
		return str(self.array)

	def size(self):
		return len(self.array)

	def insert(self, item):
		self.array.append(item) #add item as leftmost leaf
		child_index = len(self.array) - 1
		parent_index = self.get_parent(child_index)
		while not self.check_heap_property(child_index, parent_index): #check whether heap invariant is violated
			self.swap(child_index, parent_index) #if so, bubble the leaf up toward the root
			child_index = parent_index
			parent_index = self.get_parent(child_index)

	def show_min(self):
		"""Similar to extract_min, but simply show the minimum element without removing it."""
		return self.array[0]

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
				if self.array[children_indices[0]] < self.array[children_indices[1]]:
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
			return self.array[child_index] >= self.array[parent_index]

	def heapify(self, l):
		"""O(n) method to load an array into an empty heap."""
		assert len(self.array) == 0 #make sure heap is empty
		self.array = sorted(l)


class MaxHeap(object):
	"""Maximum heap data structure. Identical to MinHeap except for direction of inequalities in extract_max and check_heap_property."""
	def __init__(self):
		self.array = []
		self.root = None

	def __str__(self):
		return str(self.array)

	def size(self):
		return len(self.array)

	def insert(self, item):
		self.array.append(item) #add item as leftmost leaf
		child_index = len(self.array) - 1
		parent_index = self.get_parent(child_index)
		while not self.check_heap_property(child_index, parent_index): #check whether heap invariant is violated
			self.swap(child_index, parent_index) #if so, bubble the leaf up toward the root
			child_index = parent_index
			parent_index = self.get_parent(child_index)

	def show_max(self):
		"""Similar to extract_max, but simply hand the root to the user without removing it."""
		return self.array[0]

	def extract_max(self):
		self.swap(0, len(self.array)-1) #switch the root with the last leaf
		maximum = self.array.pop() #remove the former root from the end of the array so it can be returned
		parent_index = 0
		children_indices = self.get_children(parent_index)
		while not (self.check_heap_property(children_indices[0], parent_index) and self.check_heap_property(children_indices[1], parent_index)):
			#find minimum of two children, assuming both exist
			if children_indices[1] == None: #node has only one child
				max_child = children_indices[0]
			else: #both children exist
				if self.array[children_indices[0]] > self.array[children_indices[1]]:
					max_child = children_indices[0]
				else:
					max_child = children_indices[1]

			#bubble the parent down toward the leaves
			self.swap(parent_index, max_child)
			parent_index = max_child
			children_indices = self.get_children(max_child)
			
		return maximum #hand the root to the user

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
			return self.array[child_index] <= self.array[parent_index]

	def heapify(self, l):
		"""O(n) method to load an array into an empty heap."""
		assert len(self.array) == 0 #make sure heap is empty
		self.array = [i for i in reversed(sorted(l))]

# max = MaxHeap()
# max.insert(0)
# max.insert(1)
# max.insert(2)
# print max
# print max.show_max()
# print max
# print max.extract_max()
# print max