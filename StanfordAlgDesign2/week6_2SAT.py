
class two_sat_graph(object):

	def __init__(self, sat_instance_file):
		self.n_vars, self.edges, self.nodes = self.parse_file(sat_instance_file)

	def parse_file(self, filename):
		n_vars = 0
		edges = []
		nodes = []
		with open(filename) as fo:
			for idx, line in enumerate(fo):
				if idx == 0:
					n_vars = int(line.split()[0])
				else:
					a, b = [int(i) for i in line.split()]
					edges.append((-a, b))
					edges.append((-b, a))
					nodes.extend([-a, b, -b, a])

		assert len(edges) == 2 * n_vars
		return n_vars, edges, nodes

if __name__ == "__main__":
	tsg = two_sat_graph("2sat1.txt")
	print tsg.edges[0:100]
	print tsg.nodes[0:50]

