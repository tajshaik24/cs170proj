import random
import os
import networkx as nx
from skeleton.output_scorer import score_output
shuffle = random.shuffle


def main(name, iType, counter=0,):
	iname = "all_inputs/" + iType + "/" + name + "/"
	inputs = readInput(iname)
	G = inputs[0]
	num_buses = inputs[1]
	size_bus = inputs[2]
	constraints = inputs[3]
	encode = {}
	decode = {}
	labelID = 0
	for node in G.nodes:
		encode[node] = labelID
		decode[labelID] = node
		labelID += 1

	s = [i for i in range(nx.number_of_nodes(G))]
	shuffle(s)
	bus_arrangements = [[] for i in range(num_buses)]
	for i in range(len(bus_arrangements)):
		x = s.pop()
		bus_arrangements[i].append(x)
	while s:
		busNum = random.randint(0, num_buses - 1)
		if len(bus_arrangements[busNum]) + 1 <= size_bus:
			bus_arrangements[busNum].append(s.pop())
		else:
			continue

	for i in range(len(bus_arrangements)):
		for j in range(len(bus_arrangements[i])):
			bus_arrangements[i][j] = decode[bus_arrangements[i][j]]

	oname = "all_outputs/" + iType + "/"
	writeOutput(bus_arrangements, oname, name, counter)


def readInput(inputFolder):
	graph = nx.read_gml(inputFolder + "graph.gml")
	parameters = open(inputFolder + "parameters.txt")
	num_buses = int(parameters.readline())
	size_bus = int(parameters.readline())
	constraints = []
	for line in parameters:
		line = line[1: -2]
		curr_constraint = [node.replace("'","") for node in line.split(", ")]
		constraints.append(curr_constraint)
	return (graph, num_buses, size_bus, constraints)


def writeOutput(bus_arrangements, folder, name, counter):
	if not os.path.exists(folder):
		os.makedirs(folder)
	file = folder + name + str(counter) + '5.out'
	with open(file, 'w') as f:
		for bus in bus_arrangements:
			f.write("%s\n" % bus)
	f.close()


if __name__ == '__main__':
	main("159")