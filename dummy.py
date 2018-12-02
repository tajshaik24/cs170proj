import random
import os
import networkx as nx
from skeleton.output_scorer import score_output
shuffle = random.shuffle

def main():
	iname = "all_inputs/large/1067/"
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
		while len(bus_arrangements[i]) < size_bus and len(s) != 0: 
			x = s.pop()
			bus_arrangements[i].append(x)
	while s:
		busNum = random.randint(0, num_buses - 1)
		bus_arrangements[busNum].append(s.pop())

	for i in range(len(bus_arrangements)):
		for j in range(len(bus_arrangements[i])):
			bus_arrangements[i][j] = decode[bus_arrangements[i][j]]

	oname = "all_outputs/large/"
	writeOutput(bus_arrangements, oname, "1067")
	score, msg = score_output(iname, oname + str(1067) + ".out")
	print(msg)
	print("Score: ", score*100, "%")


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


def writeOutput(bus_arrangements, folder, name):
	if not os.path.exists(folder):
		os.makedirs(folder)
	file = folder + name +'.out'
	with open(file, 'w') as f:
		for bus in bus_arrangements:
			f.write("%s\n" % bus)
	f.close()


if __name__ == '__main__':
	main()