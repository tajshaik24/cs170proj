import networkx as nx
import os
import matplotlib.pyplot as plt

def main():
	# G = parseGraph('graphs')
	G = randomGraph()
	numComponents = nx.number_connected_components(G)
	connComponents = nx.connected_components(G)

	print(numComponents)


def parseGraph(folder_name):
	graph = nx.read_gml(folder_name + "/graph.gml")
	return graph

def randomGraph():
	G = nx.gnp_random_graph(50, 0.2)
	nx.draw(G)
	plt.show()
	return G



if __name__ == '__main__':
    main()