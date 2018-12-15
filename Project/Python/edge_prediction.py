import loader
import networkx as nx
import random
import math

def edges_not_in(G):
    I = []
    node_count = len(G.nodes())

    for u in range(node_count):
        for v in range(node_count):
            if u == v: continue

            if not G.has_edge(u, v):
                I.append((u, v))
    return I

def split_edges(G):
    edges = list(G.edges())
    edge_count = len(edges)

    probe_set = []
    probe_set_size = int(0.1 * edge_count)

    for i in range(probe_set_size):
        p_edge = random.choice(edges)

        G.remove_edge(p_edge[0], p_edge[1])
        edges.remove(p_edge)
        probe_set.append(p_edge)

    return probe_set

def common_neighbors(G, Ep, I):
    cn_Ep = []
    cn_I = []

    for edge in Ep:
        cn_Ep.append(len(list(nx.common_neighbors(G, edge[0], edge[1]))))

    for edge in I:
        cn_I.append(len(list(nx.common_neighbors(G, edge[0], edge[1]))))

    return cn_Ep, cn_I

def adamic_adar(G, Ep, I):
    aa_Ep = []
    aa_I = []

    for edge in Ep:
        score = 0
        for node in list(nx.common_neighbors(G, edge[0], edge[1])):
            score += 1/(math.log(G.degree(node)))

        aa_Ep.append(score)

    for edge in I:
        score = 0
        for node in list(nx.common_neighbors(G, edge[0], edge[1])):
            score += 1/(math.log(G.degree(node)))

        aa_I.append(score)

    return aa_Ep, aa_I

def resource_allocation(G, Ep, I):
    ra_Ep = []
    ra_I = []

    for edge in Ep:
        score = 0
        for node in list(nx.common_neighbors(G, edge[0], edge[1])):
            score += 1/(G.degree(node))

        ra_Ep.append(score)

    for edge in I:
        score = 0
        for node in list(nx.common_neighbors(G, edge[0], edge[1])):
            score += 1/(G.degree(node))

        ra_I.append(score)

    return ra_Ep, ra_I

def accuracy(Ep, I, n):
    acc = 0

    for round in range(n):
        Ep_r = random.choice(Ep)
        I_r = random.choice(I)

        if Ep_r > I_r:
            acc += 1
        elif Ep_r == I_r:
            acc += 0.5

    return acc / n;

def run_predictions(levels, n, iterations):
    cn_accuracy = []
    aa_accuracy = []
    ra_accuracy = []

    #Get graph
    G = loader.get_graph(levels)

    I = edges_not_in(G)

    for i in range(iterations):

        #Divide edges
        Ep = split_edges(G)

        #Score all edges
        cn_Ep, cn_I = common_neighbors(G, Ep, I)
        aa_Ep, aa_I = adamic_adar(G, Ep, I)
        ra_Ep, ra_I = resource_allocation(G, Ep, I)

        cn_accuracy.append(accuracy(cn_Ep, cn_I, n))
        aa_accuracy.append(accuracy(aa_Ep, aa_I, n))
        ra_accuracy.append(accuracy(ra_Ep, ra_I, n))

        #Restore Graph
        G.add_edges_from(Ep)

    # print('Common Neighbors accruacy:    ' + str(sum(cn_accuracy)/iterations))
    # print('Adamic-Adar index accruacy:   ' + str(sum(aa_accuracy)/iterations))
    # print('Resource Allocation accruacy: ' + str(sum(ra_accuracy)/iterations))

    return str(sum(cn_accuracy)/iterations), str(sum(aa_accuracy)/iterations), str(sum(ra_accuracy)/iterations)

def main():
    n = 100
    iterations = 100

    print("****** All levels of co-offending: ******")
    cna, aaa, raa = run_predictions([2, 3, 4], n, iterations)

    print("****** Serious crimes only: ******")
    cns, aas, ras = run_predictions([3, 4], n, iterations)

    print("****** Petty crimes only: ******")
    cnp, aap, rap = run_predictions([2], n, iterations)

    print('\tAll\tSerious\tPetty')
    print('CN\t', cna, '\t', cns, '\t', cnp)
    print('AA\t', aaa, '\t', aas, '\t', aap)
    print('RA\t', raa, '\t', ras, '\t', rap)

if __name__ == '__main__':
    main()
