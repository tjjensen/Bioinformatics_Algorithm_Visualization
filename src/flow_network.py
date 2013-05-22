class NetworkFlow():
	def __init__(nodes, edges, source, sink):
		nodes = dict()
		for name in nodes:
			node = NetworkNode(name)
			nodes[name] = node
		for edge_tuple in edges:
			edge = NetworkEdge(*edge_tuple)
			nodes[edge_tuple[0]].adj.append(edge)



class NetworkNode():
	def __init__(name):
		self.name = name
		self.adj = list()

class NetworkEdge():
	def __init__(tail, head, capacity):
		self.tail = tail
		self.head = head
		self.capacity = capacity
		self.flow = 0