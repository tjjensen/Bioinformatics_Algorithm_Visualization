import random
import math

def lloyd(k, points):
	x_min, x_max = getXrange(points)
	y_min, y_max = getYrange(points)
	centers = list()
	associations = list()
	
	prev_error = float('inf')

	centers.append(list())
	for i in range(k):
		centers[-1].append((random.uniform(x_min, x_max), random.uniform(y_min, y_max)))

	association = getAssociation(points, centers[-1])
	associations.append(association)

	while True:
		new_cluster = getClusters(points, associations[-1])
		new_association = getAssociation(points, new_cluster)
		centers.append(new_cluster)
		associations.append(new_association)
		if new_association ==  associations[-2]:
			break
	return centers, associations

def getClusters(points, associations):
	cluster = list()
	for i in set(associations):
		s = [0.0,0.0]
		n = 0.0
		for j, point in enumerate(points):
			if associations[j] == i:
				s[0] += point[0]
				s[1] += point[1]
				n += 1
		s[0] = s[0] / n
		s[1] = s[1] / n
		cluster.append((s[0], s[1]))
	return cluster

def dist(p1, p2):
	return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def getAssociation(points, centers):
	association = list()
	for point in points:
		d = float('inf')
		index = -1
		for i, center in enumerate(centers):
			if dist(point, center) < d:
				d = dist(point, center)
				index = i
		association.append(index)
	return association

def getXrange(points):
	minx = float('inf')
	maxx = float('-inf')
	for point in points:
		if point[0] < minx:
			minx = point[0]
		if point[0] > maxx:
			maxx= point[0]
	return (minx, maxx)

def getYrange(points):
	miny = float('inf')
	maxy = float('-inf')
	for point in points:
		if point[1] < miny:
			miny = point[1]
		if point[1] > maxy:
			maxy= point[1]
	return (miny, maxy)

def main():
	k=2
	points = [(0,0), (1,0), (2,0), (1,2),(2,2), (3,2)]
	c, a = lloyd(k, points)
	print c
	print a

if __name__ == '__main__':
	main()
