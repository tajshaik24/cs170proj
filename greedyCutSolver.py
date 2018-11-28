import networkx as nx
import os
import matplotlib.pyplot as plt
import random
import sys
import itertools

def main():
	inputs = readInput("/all_inputs/small/104")
	G = inputs[0]
	num_buses = inputs[1]
	size_bus = inputs[2]
	constraints = inputs[3]
	edges_dict = computeRowdyEdges(constraints)
	newG = addRowdyEdges(G, edges_dict)
	#Use min-cut algorithm to make the cuts of max size size_buses
	#Recursively partition until we have it num_buses

def computeRowdyEdges(constraints):
    edge_weights = {}
    for x in constraints:
        length = len(x)
        all_edges = list(itertools.combinations(x, 2))
        for edge in all_edges:
            if(edge in edge_weights):
                edge_weights[edge] = max(edge_weights.get(edge), -1/length)
            else:
                edge_weights[edge] = -1/length
    return edge_weights
	
def readInput(input_folder):
	graph = nx.read_gml(input_folder + "/graph.gml")
    parameters = open(input_folder + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [node.replace("'","") for node in line.split(", ")]
        constraints.append(curr_constraint)
    return (graph, num_buses, size_bus, constraints)


def addRowdyEdges(G, edges):
	l = []
	for k, v in d.items():
		l.append((k[0], k[1], v))
	G.add_weighted_edges_from(l)
	return l












if __name__ == '__main__':
    main()