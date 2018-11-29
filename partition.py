import networkx as nx
import matplotlib.pyplot as plt
import itertools

def computeNegEdges(constraints):
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
    return graph_components, need_cut

def delete_edges(G, edges):
    for x, y in edges:
        G.remove_edge(x,y)
    return G

def draw(G):
	#nx.draw(G)
	pos = nx.spring_layout(G,k=1,iterations=20)
	nx.draw(G, pos)
	plt.show()

'''
def main():
    test_list = [[1,2,3,4], [2,3,4,5], [3,4,5]]
    negEdges = computeNegEdges(test_list)
    print(negEdges)

if __name__ == '__main__':
    main()
'''