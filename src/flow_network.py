class FlowNetwork():

	def __init__(self, nodes, edges, source, sink):
		self.source = source
		self.sink = sink
		self.nodes = dict()
		self.edges = list()
		self.rev_edges = list()
		for name in nodes:
			node = NetworkNode(name)
			self.nodes[name] = node
		for edge_tuple in edges:
			edge = NetworkEdge(edge_tuple[0], edge_tuple[1], edge_tuple[2], True)
			redge = NetworkEdge(edge_tuple[1], edge_tuple[0], 0, False)
			edge.rev_edge = redge
			redge.rev_edge = edge
			self.nodes[edge_tuple[0]].adj.append(edge_tuple[1])
			self.nodes[edge_tuple[1]].adj.append(edge_tuple[0])
			self.edges.append(edge)
			self.rev_edges.append(redge)

	def stepwise_ford_fulkerson(self, stack):
		if len(stack) == 0:
			return None
		current_node, path, current_flow = stack.pop()
		current_node = self.nodes[current_node]
		if current_node.name == self.sink:
			for edge in path:
				edge.flow += current_flow
				edge.rev_edge.flow -= current_flow
			return True
		edges = list()
		for adj_node in current_node.adj:
			edges += self.get_edge(current_node.name, adj_node)
		
		for current_edge in edges[::-1]:
			if current_edge in path:
				continue
			allowed_flow = current_edge.capacity - current_edge.flow
			new_flow = min(allowed_flow, current_flow)
			if new_flow > 0:
				current_path = list(path)
				current_path.append((current_edge))
				stack.append((current_edge.head, current_path, new_flow))
		return False

	def get_edge(self, tail, head):
		edges = list()
		for edge in self.edges + self.rev_edges:
			if edge.tail == tail and edge.head == head:
				edges.append(edge)
		return edges

	def get_inital_stack(self):
		stack = list()
		stack.append((self.source, list(), float('inf')))
		return stack

	def get_steps(self):
		steps = list()
		stack = self.get_inital_stack()
		steps.append((stack[-1][0], self.get_flows(), self.get_flow()))
		while True:
			next = self.stepwise_ford_fulkerson(stack)
			if next is None:
				break
			elif next:
				stack = self.get_inital_stack()
			if stack:
				steps.append((stack[-1][0], self.get_flows(), self.get_flow()))
		return steps

	def get_flow(self):
		flow = 0
		for edge in self.edges:
			if edge.head == self.sink:
				flow += edge.flow
		return flow
	def get_flows(self):
		flows = list()
		for edge in self.edges + self.rev_edges:
			flows.append((edge.tail, edge.head, edge.flow, edge.capacity, edge.forward))
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
	def __init__(self, tail, head, capacity, forward):
		self.tail = tail
		self.head = head
		self.capacity = int(capacity)
		self.flow = 0
		self.forward = forward

	def __repr__(self):
		return '{0} {1} {2} {3} {4}'.format(self.tail, self.head, self.forward, self.capacity, self.flow)


def main():	
	nodes = ('a', 'b', 'c', 'd')
	edges = (('a', 'b', 1000), ('b', 'c', 1), ('b', 'd', 1000), ('a', 'c', 1000), ('c', 'd', 1000))
	netflow = FlowNetwork(nodes, edges, 'a', 'd')
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