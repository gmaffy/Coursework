"""UCSD Bioinformatics Algorithms Part II,
Week 1: Finding Mutations in the Genome."""

class Trie(object):

	"""Directed tree structure to represent a collection of strings.
	Contains a root node with indegree zero. Edges are labeled with
	characters and nodes are given arbitrary integer labels (0,1,...,n).
	Each edge leading from a given node is distinct.

	When trieify is called on a list of strings, that list of strings is
	given a trie representation such that each path from root to leaf
	spells a string in the list by concatenating the edges."""

	def __init__(self):
		self.nodes = []
		self.root = None

	def trieify(list_of_strings):
		pass

