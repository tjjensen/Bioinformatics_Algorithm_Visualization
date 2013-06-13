class FlowNetwork():
	def __init__(self, nodes, edges, source, sink):
		self.source = source
		self.sink = sink
		self.nodes = dict()
		self.edges = list()
		for name in nodes:
			node = NetworkNode(name)
			self.nodes[name] = node
		for edge_tuple in edges:
			edge = NetworkEdge(*edge_tuple)
			self.nodes[edge_tuple[0]].adj.append(edge_tuple[1])
			self.edges.append(edge)

	def stepwise_ford_fulkerson(self, stack):
		if len(stack) == 0:
			return None
		current_node, path, current_flow = stack.pop()
		current_node = self.nodes[current_node]
		if current_node.name == self.sink:
			for edge in path:
				edge.flow += current_flow
			return True
		for adj_node in current_node.adj:
			current_edge = self.get_edge(current_node.name, adj_node)
			if current_edge in path:
				continue
			allowed_flow = current_edge.capacity - current_edge.flow
			current_flow = min(allowed_flow, current_flow)
			if current_flow > 0:
				current_path = list(path)
				current_path.append((current_edge))
				stack.append((adj_node, current_path, current_flow))
		return False

	def get_edge(self, tail, head):
		for edge in self.edges:
			if edge.tail == tail and edge.head == head:
				return edge

	def get_inital_stack(self):
		stack = list()
		stack.append((self.source, list(), float('inf')))
		return stack

	def get_steps(self):
		steps = list()
		stack = self.get_inital_stack()
		steps.append((stack[-1][0], self.get_flows()))
		while True:
			next = self.stepwise_ford_fulkerson(stack)
			if next is None:
				break
			elif next:
				stack = self.get_inital_stack()
			if stack:
				steps.append((stack[-1][0], self.get_flows()))
		return steps

	def get_flows(self):
		flows = list()
		for edge in self.edges:
			flows.append((edge.tail, edge.head, edge.flow))
		return flows

	def __str__(self):
		return_str = '\n{0}\n{1}'.format(self.nodes, self.edges)
		return return_str

class NetworkNode():
	def __init__(self, name):
		self.name = name
		self.adj = list()

	def __repr__(self):
		return '{0} {1}'.format(self.name, self.adj)

class NetworkEdge():
	def __init__(self, tail, head, capacity):
		self.tail = tail
		self.head = head
		self.capacity = int(capacity)
		self.flow = 0

	def __repr__(self):
		return '{0} {1} {2} {3}'.format(self.tail, self.head, self.capacity, self.flow)


def main():
	nodes = ('s', 't', 'a', 'b', 'c', 'd', 'e', 'f')
	edges = (('s', 'a', 5), ('s', 'b', 3), ('a', 'c', 4), ('b', 'c', 3), ('c', 't', 4))
	netflow = FlowNetwork(nodes, edges, 's', 't')
	print netflow
	
	stack = netflow.get_inital_stack()
	steps = netflow.get_steps()
	print steps
	return
	while True:
		next = netflow.stepwise_ford_fulkerson(stack)
		if next is None:
			break
		elif next:
			stack = netflow.get_inital_stack()
		print stack
	print netflow

if __name__ == '__main__':
	main()