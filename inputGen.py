import networkx as nx
import os
import matplotlib.pyplot as plt
import random
import sys

SEED = 123456789

def main():
	flags = sys.argv
	if '-s' in flags:
		makeInput(50, 5, 15, 'small')
	if '-m' in flags:
		makeInput(500, 25, 30, 'medium')
	if '-l' in flags:
		makeInput(1000, 50, 75, 'large')


# Parameters
# n: Number of children
# k: Number of buses
# s: Bus capacity
def makeInput(n, k, s, folder):
	G = randomGraph(n)
	numComponents = nx.number_connected_components(G)
	connComponents = list(nx.connected_components(G))
	# Converting connected components from Sets to Lists
	connComponents = [list(S) for S in connComponents]

	# Deciding how many rowdy groups based on number of children
	if n <= 50:
		numRowdy = 75
	elif n <= 500:
		numRowdy = 750
	elif n <= 2000:
		numRowdy = 1500
	rowdyGroups = generateRowdy(numComponents, connComponents, numRowdy, s)

	if not os.path.exists(folder):
		os.mkdir(folder)
	path = folder + '/graph.gml'
	nx.write_gml(G, path)

	file = folder + '/parameters.txt'
	with open(file, 'w') as f:
		f.write(str(k) + '\n')
		f.write(str(s) + '\n')
		for x in rowdyGroups:
			f.write("%s\n" % x)
	f.close()





def generateRowdy(numComponents, connComponents, numGroups, s):
	rowdyGroups = []
	a = 0
	while a != numGroups:
		group = []
		i = 0
		# We can have rowdy groups of size 2 to capacity of one bus (s)
		toAdd = random.randint(2, s)
		while i != toAdd:
			# Get a random connected component
			j = random.randint(0, numComponents - 1)
			component = connComponents[j]
			# Get a random node in the component
			k = random.randint(0, len(component) - 1)
			node = component[k]
			# Check to make sure this node is not already in the rowdy group
			if node not in group:
				group.append(component[k])
				i += 1
		# Convert rowdy group nodes to ints 
		group = [int(x) for x in group]
		# Sort the elements of rowdy group to make it easier to check equality
		group = sorted(group)
		# Convert nodes back to string for input requirements
		group = [str(x) for x in group]
		# Check to see if this rowdy group has already been created
		if group not in rowdyGroups:
			rowdyGroups.append(group)
			a += 1

	# print(len(rowdyGroups), " rowdy groups generated!")
	# print(numComponents, " connected components in the graph.")
	# print("The rowdy groups are: ")
	# for x in rowdyGroups:
	# 	print(x)

	return rowdyGroups


def randomGraph(n):
	graphs = []
	# TODO: Allow flexibility in inputs
	if n == 50:
		subNodes = [15, 15, 10, 5, 5]
		edgeProbs = [0.35, 0.30, 0.40, 0.35, 0.45]
		numSubGraphs = len(subNodes)
	elif n == 500:
		subNodes = [75, 75, 75, 50, 50, 50, 50, 25, 25, 25]
		edgeProbs = [0.35, 0.30, 0.40, 0.35, 0.45, 0.3, 0.2, 0.35, 0.3, 0.4]
		numSubGraphs = len(subNodes)
	elif n == 1000:
		subNodes = [100, 100]
		subNodes.extend([75 for i in range(4)])
		subNodes.extend([25 for i in range(5)])
		subNodes.extend([15 for i in range(15)])
		subNodes.extend([10 for i in range(15)])
		numSubGraphs = len(subNodes)
		edgeProbs = [random.uniform(0.2, 0.45) for i in range(numSubGraphs)]
	for i in range(numSubGraphs):
		A = nx.gnp_random_graph(subNodes[i], edgeProbs[i])
		graphs.append(A)
	G = nx.disjoint_union_all(graphs)
	G = nx.convert_node_labels_to_integers(G, first_label=1)
	G = nx.relabel_nodes(G, lambda x: str(x))
	return G

def draw(G):
	#nx.draw(G)
	pos = nx.spring_layout(G,k=1,iterations=20)
	nx.draw(G, pos)
	plt.show()



if __name__ == '__main__':
    main()