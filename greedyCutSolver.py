import networkx as nx
import os
import matplotlib.pyplot as plt
import random
import sys
import itertools
import math
import metis
from skeleton.output_scorer import score_output

def main(inputFolder, outputFolder):
	inputs = readInput(inputFolder)
	G = inputs[0]
	G.remove_edges_from(G.selfloop_edges())
	encode = {}
	decode = {}
	labelID = 0
	for node in G.nodes:
		encode[node] = labelID
		decode[labelID] = node
		labelID += 1


	G = nx.relabel_nodes(G, encode)

	for u,v,d in G.edges(data=True):
		d['weight'] = 1
	num_buses = inputs[1]
	if num_buses == 1:
		bus_arrangements = []
		students = []
		for node in G.nodes:
			students.append(decode[node])
		bus_arrangements.append(students)
		writeOutput(bus_arrangements, outputFolder)
		return
	size_bus = inputs[2]
	constraints = inputs[3]
	for i in range(len(constraints)):
		for j in range(len(constraints[i])):
			constraints[i][j] = encode[constraints[i][j]]

	edges_dict = computeRowdyEdges(constraints, G)
	newG = addRowdyEdges(G, edges_dict)
	#Use min-cut algorithm to make the cuts of max size size_buses
	#Recursively partition until we have it num_buses
	#components = partition(newG, num_buses)
	components = new_partition(newG, num_buses, size_bus)
	bus_arrangements = merge(components, num_buses, G, size_bus)
	if bus_arrangements is None:
		return
	for i in range(len(bus_arrangements)):
		for j in range(len(bus_arrangements[i])):
			bus_arrangements[i][j] = decode[bus_arrangements[i][j]]

	# print("Bus Arrangements:")
	# for p in bus_arrangements:
	# 	print(p)
	# print("End")
	if bus_arrangements is None:
		return
	writeOutput(bus_arrangements, outputFolder)


def writeOutput(bus_arrangements, folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
	file = folder + '.out'
	with open(file, 'w') as f:
		for bus in bus_arrangements:
			f.write("%s\n" % bus)
	f.close()


def computeRowdyEdges(constraints, G):
    edge_weights = {}
    for x in constraints:
        length = len(x)
        all_edges = list(itertools.combinations(x, 2))
        for edge in all_edges:
        	if not G.has_edge(edge[0], edge[1]):
        		edge_weights[edge] = -1
        	else:
	            if(edge in edge_weights):
	                edge_weights[edge] = max(edge_weights.get(edge), -1/length)
	            else:
	                edge_weights[edge] = -1/(length)
    return edge_weights
	
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


def addRowdyEdges(G, edges):
	l = []
	for k, v in edges.items():
		l.append((k[0], k[1], v))
	G.add_weighted_edges_from(l)
	return G

def new_partition(G, num_buses, size_bus):
	graph_components = {}
	edgecuts = ()
	parts = ()
	nodes_subgraph = []
	cut_size = num_buses
	while True:
		(edgecuts, parts) = metis.part_graph(G, cut_size)
		nodes_subgraph = [[] for _ in range(max(parts) + 1)]
		for i, p in enumerate(parts):
			nodes_subgraph[p].append(i)
		nodes_subgraph = list(filter(lambda x: len(x) > 0, nodes_subgraph))
		if len(nodes_subgraph) == num_buses:
			break
		elif len(nodes_subgraph) >= 0.5*num_buses:
			nodes_subgraph.sort(key=lambda x: len(x))
			while len(nodes_subgraph) < num_buses:
				bigComp = nodes_subgraph.pop()
				sub_g = nx.Graph(G.subgraph(bigComp))
				if nx.number_connected_components(sub_g) > 1:
					cComps = list(nx.connected_components(sub_g))
					cComps = [list(a) for a in cComps]
					cComps.sort(key=lambda x: len(x))
					bigG = cComps.pop()
					sub_g = nx.Graph(sub_g.subgraph(bigG))
					for m in cComps:
						nodes_subgraph.append(m)
				parts = partition(sub_g, size_bus)
				for k, v in parts.items():
					nodes_subgraph.append(list(k.nodes()))
				nodes_subgraph.sort(key=lambda x: len(x))
			break
		cut_size -= 1

	for i in nodes_subgraph:
		sub_graph = G.subgraph(i)
		if nx.number_of_nodes(sub_graph) > size_bus:
			recursive_part = new_partition_helper(sub_graph, 2, size_bus)
			if recursive_part is not None:
				for k in recursive_part:
					graph_components[k[0]] = k[1]
			else:
				sub_g = nx.Graph(sub_graph)
				recursive_part = partition(sub_g, size_bus)
				for k, v in recursive_part.items():
					graph_components[k] = v
		else:
			graph_components[sub_graph] = nx.number_of_nodes(sub_graph)
	return graph_components

def new_partition_helper(G, num_buses, size_bus):
	graph_components = []
	nodes = list(G.nodes)
	cut_size = num_buses
	nodes_subgraph = []
	parts = None
	ran = 0
	while True:
		(edgecuts, parts) = metis.part_graph(G, cut_size)
		nodes_subgraph = [[] for _ in range(max(parts) + 1)]
		for i in range(len(parts)):
			lnum = parts[i]
			vertex = nodes[i]
			nodes_subgraph[lnum].append(vertex)
		nodes_subgraph = [x for x in nodes_subgraph if len(x) > 0]
		if len(nodes_subgraph) > 1:
			break
		cut_size -=1
		ran += 1
		if cut_size == 1 or ran > 4:
			return None

	for i in nodes_subgraph:
		sub_graph = G.subgraph(i)
		if nx.number_of_nodes(sub_graph) > size_bus:
			r_comps = new_partition_helper(sub_graph, 2, size_bus)
			for s in r_comps:
				graph_components.append(s)
		else:
			graph_components.append([sub_graph, nx.number_of_nodes(sub_graph)])
	return graph_components



def partition(G, capacity):
    graph_components = {}
    need_cut = []
    cut_set = nx.minimum_edge_cut(G)
    G = delete_edges(G, cut_set) 
    sub_graphs = [graph for graph in nx.connected_component_subgraphs(G)]
    for i in sub_graphs:
    	graph_components[i] = nx.number_of_nodes(i)
    	if(graph_components[i] > capacity):
    		need_cut.append(i)
    while(need_cut):
        graph_components.pop(need_cut[0])
        big_graph = need_cut.pop(0)
        cut_set = nx.minimum_edge_cut(big_graph)
        big_graph = delete_edges(big_graph, cut_set) 
        sub_big_graph = [graph for graph in nx.connected_component_subgraphs(big_graph)]
        for i in sub_big_graph:
            graph_components[i] = nx.number_of_nodes(i)
            if(graph_components[i] > capacity):
                need_cut.append(i)
    return graph_components

def delete_edges(G, edges):
    for x, y in edges:
        G.remove_edge(x,y)
    return G


def merge(comp_dict, k, G, bus_size):
	sorted_comp = sorted(comp_dict.items(), key=lambda kv: kv[1])
	gidMap = {}
	gID = 0

	#Map Graph ID to list of tuples (gID, sumEdgesWeight)
	#sorted_comp = [['GID', (GraphObject, SizeofGraph)], ...]
	
	length = len(sorted_comp)
	connections = [[0 for i in range(length)] for j in range(length)]
	sd = []
	for i in sorted_comp:
		i[0].graph['id'] = gID
		gidMap[str(gID)] = i[0]
		sd.append([str(gID), (i[0], i[1])])
		gID += 1

	
	sorted_comp = sd


	for a in sorted_comp:
		for b in sorted_comp:
			if a is not b and connections[a[1][0].graph['id']][b[1][0].graph['id']] is not None:
				w = 0
				for i in list(a[1][0].nodes):
					for j in list(b[1][0].nodes):
						if G.has_edge(i, j):
							w += G[i][j]['weight']
				connections[a[1][0].graph['id']][b[1][0].graph['id']] = w
				connections[b[1][0].graph['id']][a[1][0].graph['id']] = w
	
	buses = []
	while len(sorted_comp) != k:
		minComp = sorted_comp.pop(0)
		minID = minComp[0]
		otherID = findBestMerge(minID, sorted_comp, minComp[1][1], bus_size, connections)

		
		if otherID == '':
			sorted_comp.insert(0, minComp)
			toDistribute = []
			while len(sorted_comp) > k:
				splitter = sorted_comp.pop(0)
				minComps = splitter[0].split('+')
				for j in minComps:
					toDistribute += list(gidMap[j].nodes)
			
			buses = [[] for i in range(k)]
			for j in range(len(sorted_comp)):
				ids = sorted_comp[j][0].split('+')
				nodes = []
				for i in ids:
					nodes += list(gidMap[i].nodes)
				buses[j] = nodes

			added = [sorted_comp[i][1][1] for i in range(len(sorted_comp))]
			while toDistribute:
				node = toDistribute.pop()
				index = random.randint(0, len(sorted_comp) - 1)
				while added[index] + 1 > bus_size:
					index = random.randint(0, len(sorted_comp) - 1)
				buses[index].append(node)
				added[index] += 1



					
			return buses
		
		sorted_comp = list(filter(lambda x: x[0] != otherID, sorted_comp))
		
		minComps = minID.split('+')
		otherComps = otherID.split('+')
		minNodes = sum([nx.number_of_nodes(gidMap[a]) for a in minComps])
		otherNodes = sum([nx.number_of_nodes(gidMap[a]) for a in otherComps])
		
		sorted_comp.append([minID + "+" + otherID, (minComp[1][0], minNodes + otherNodes)])
		sorted_comp.sort(key=lambda x: x[1][1])


	for bus in sorted_comp:
		ids = bus[0].split('+')
		nodes = []
		for i in ids:
			nodes += list(gidMap[i].nodes)
		buses.append(nodes)

	return buses


def findBestMerge(gID, sList, numGNodes, capacity, connections):
	ids = gID.split('+')
	ids = [int(a) for a in ids]
	best = -math.inf
	otherID = ''
	for x in sList:
		if x[0] != str(gID):
			oID = x[0]
			comps = oID.split('+')
			comps = [int(b) for b in comps]
			edgeSum = 0
			for i in ids:
				for j in comps:
					edgeSum += connections[i][j]
			if numGNodes + x[1][1] <= capacity and edgeSum > best:
				best = edgeSum
				otherID = oID
	return otherID

def draw(G):
	#nx.draw(G)
	pos = nx.spring_layout(G,k=1,iterations=20)
	nx.draw(G, pos)
	labels = nx.get_edge_attributes(G,'weight')
	#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
	nx.draw_networkx_labels(G, pos=pos)
	plt.show()


# if __name__ == '__main__':
# 	iname = "all_inputs/small/"
# 	oname = "all_outputs/small/"

# 	a = []
# 	b = []
# 	for x in os.listdir(iname)[:40]:
# 		x = x + "/"
# 		try:
# 			main(iname+x, oname+x)
# 			a.append(iname+x)
# 			b.append(oname+x+".out")
# 		except:
# 			continue
# 	scores = []
# 	for i in range(len(a)):
# 		try:
# 			score, msg = score_output(a[i], b[i])
# 			scores.append(score)
# 			print(msg)
# 		except:
# 			continue
# 	print("Average is: ", sum(scores)/len(scores))

if __name__ == '__main__':
	iname = "all_inputs/small/"
	oname = "all_outputs/small/"

	files = list(os.walk(iname))[0][1]
	scores = []
	files.sort()
	for f in files:
		print(f)
		main(iname + f + "/", oname + f + "/")
		score, msg = score_output(iname + "/" + f + "/", oname + f + "/.out")
		print(msg)
		print("Score: ", score*100, "%")
		try:
			if score >= 0:
				scores.append(score)
		except:
			continue
	print("Average: ", sum(scores)/len(scores))
	print(len(files))
	print(len(scores))


# if __name__ == '__main__':
# 	iname = "all_inputs/small/325/"
# 	oname = "all_outputs/small/325/"
# 	main(iname, oname)
# 	score, msg = score_output(iname, oname + ".out")
# 	print(msg)
# 	print("Score: ", score*100, "%")