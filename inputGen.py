import networkx as nx
import os
import matplotlib.pyplot as plt
import random

def main():
	#G = parseGraph('graphs')
	G = randomGraph()
	numComponents = nx.number_connected_components(G)
	connComponents = list(nx.connected_components(G))
	connComponents = [list(S) for S in connComponents]

	print(connComponents)

	# Assuming the following paramters for now:
	# 50 students
	# k = 5 buses
	# s = 15 children per bus capacity
	# Therefore, rowdy groups can be of size 2 to 15
	rowdyGroups = []
	for _ in range(75):
		group = []
		for _ in range(random.randint(2, 15)):
			j = random.randint(0, numComponents - 1)
			component = connComponents[j]
			k = random.randint(0, len(component) - 1)
			group.append(component[k])
		group = sorted(group)
		if group not in rowdyGroups:
			rowdyGroups.append(group)

	print(len(rowdyGroups), " rowdy groups generated!")
	print(numComponents, " connected components in the graph.")
	print("The rowdy groups are: ")
	for x in rowdyGroups:
		print(x)


def parseGraph(folder_name):
	graph = nx.read_gml(folder_name + "/names.gml")
	return graph

def randomGraph():
	A = nx.gnp_random_graph(20, 0.35)
	B = nx.gnp_random_graph(15, 0.25)
	C = nx.gnp_random_graph(10, 0.15)
	D = nx.gnp_random_graph(5, 0.20)
	graphs = [A, B, C, D]
	G = nx.union_all(graphs, rename = ('A', 'B', 'C', 'D'))
	G = nx.convert_node_labels_to_integers(G, first_label=1)
	return G

def draw(G):
	#nx.draw(G)
	pos = nx.spring_layout(G,k=1,iterations=20)
	nx.draw(G, pos)
	plt.show()



if __name__ == '__main__':
    main()