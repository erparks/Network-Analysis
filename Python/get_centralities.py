import loader
from  dynamical_importance import get_dynamical_importances
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import operator
from heapq import nlargest

def format_tuple(t):
    return str(t[0]) + ', ' + str(round(t[1], 4))


def update_edges(g, edge1, edge2):
    k = g.copy()

    k.remove_edge(edge1[0], edge1[1])
    k.remove_edge(edge2[0], edge2[1])

    k.add_edge(edge1[0], edge2[0])
    k.add_edge(edge1[1], edge2[1])

    return k

def diff_edges(g, edge1, edge2):
    #if we selected an edge pair that would make no change
    if edge1[0] == edge2[0] or edge1[0] == edge2[1] or edge1[1] == edge2[0] or edge1[1] == edge2[1]:
        return False

    #if we selected an edge pair that would make a multigraph
    if g.has_edge(edge1[0], edge2[0]) or g.has_edge(edge1[1], edge2[1]):
        return False

    return True

def get_percentiles(true, null_model):
    nodes = []
    p25s = []
    p75s = []
    base = []

    for node, cent in null_model.items():

        nodes.append(int(node))


        #get differnce from average
        avg = sum(cent)/len(cent)
        base.append(true[node] - avg)
        #print(node, ' difference: ', str(true[node] - avg))

        #get individual differences
        diffs = []
        for value in cent:
            diffs.append(true[node] - value)

        diffsArr = np.array(diffs)
        m25th = np.percentile(diffsArr, 25)
        m75th = np.percentile(diffsArr, 75)

        #print('25th: ' + str(m25th) + ' 75th ' + str(m75th))

        p25s.append(m25th)
        p75s.append(m75th)


    #Sort the centralities by node number
    ps = zip(nodes, p25s, base, p75s)
    ps = sorted(ps, key = lambda p: p[0])

    return ps

def plot(ps, type, values, level):
    #plt.figure()

    snodes = []
    s25th = []
    sbase= []
    s75th = []
    for n, t, b, s in ps:
        snodes.append(n)
        s25th.append(t)
        sbase.append(b)
        s75th.append(s)



    plt.plot(snodes, sbase, 'o-')
    plt.fill_between(snodes, s25th, s75th, alpha=0.25)
    plt.hlines(0, 0, 54, linestyles='dashed')

    for node in values[:3]:

        plt.annotate(str(node[0]), xy=(str(node[0]), sbase[node[0]]))

    # plt.annotate('Node 0', xy=(0, sbase[0]))
    # plt.annotate('Node 6', xy=(6, sbase[6]))
    # plt.annotate('Node 11', xy=(11, sbase[11]))

    plt.ylabel(type+ ' $\Delta$')
    plt.title('Difference in ' + type + ' vs. Null Model for ' + level + ' Crimes')

def get_centralities(graphs_in_null_model, G, adj, level):
        nodes = len(G.nodes())

        #Get centralities in real graph
        init_di = get_dynamical_importances(adj)
        init_h = nx.harmonic_centrality(G)
        init_h = dict(map(lambda kv: (kv[0], kv[1]/(nodes-1)), init_h.items()))

        init_b = nx.betweenness_centrality(G)
        init_d = {}

        #convert degree view into dict
        for x, y in G.degree():
            init_d[x] = y


        gs = []
        harmonic_centralities = {}
        between_centralities = {}
        dynamical_importance = {}




        #Generate null model centralities
        for i in range(0, graphs_in_null_model):

            if i % 50 == 0:
                print(i)

            #get centralities
            h = nx.harmonic_centrality(G)
            h = dict(map(lambda kv: (kv[0], kv[1]/(nodes-1)), h.items()))

            b = nx.betweenness_centrality(G)
            d = get_dynamical_importances(nx.to_numpy_matrix(G))

            #store centralities
            for k, v in h.items():
                harmonic_centralities.setdefault(k, []).append(v)

            for k, v in b.items():
                between_centralities.setdefault(k, []).append(v)

            for k, v in b.items():
                dynamical_importance.setdefault(k, []).append(v)

            #update graph
            edges = list(G.edges())
            edge1 = random.choice(edges)
            edge2 = random.choice(edges)

            while(not diff_edges(G, edge1, edge2)):
                edge2 = random.choice(edges)

            k = update_edges(G, edge1, edge2)

            gs.append(k)

            G = k


        h_ps = get_percentiles(init_h, harmonic_centralities)
        b_ps = get_percentiles(init_b, between_centralities)
        di_ps = get_percentiles(init_di, dynamical_importance)



        #
        sorted_h  = sorted(init_h.items(),  key=operator.itemgetter(1),  reverse=True)
        sorted_b  = sorted(init_b.items(),  key=operator.itemgetter(1),  reverse=True)
        sorted_di = sorted(init_di.items(), key=operator.itemgetter(1),  reverse=True)
        sorted_d  = sorted(init_d.items(),  key=operator.itemgetter(1),  reverse=True)

        plt.figure(1)
        plt.subplot(311)
        plot(di_ps, 'Dynamical Importance', sorted_di, level)
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off

        plt.subplot(312)
        plot(h_ps, 'Harmonic Centrality', sorted_h, level)
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        plt.subplot(313)
        plot(b_ps, 'Betweenness Centrality', sorted_b, level)

        plt.xlabel('Node Number')
        plt.show()

def main():

    graphs_in_null_model = 1000



    # levels = [2, 3, 4]
    #
    # adj = loader.get_adj_matrix(levels)
    #
    # G = loader.get_graph_from_adj(adj)
    #
    # get_centralities(graphs_in_null_model, G, adj, 'All')


    levels = [3, 4]

    adj = loader.get_adj_matrix(levels)

    G = loader.get_graph_from_adj(adj)

    get_centralities(graphs_in_null_model, G, adj, 'Serious')



    levels = [2]

    adj = loader.get_adj_matrix(levels)

    G = loader.get_graph_from_adj(adj)

    get_centralities(graphs_in_null_model, G, adj, 'Petty')




    # show = 10

    #for h, b, di, d in zip(sorted_h[:show], sorted_b[:show], sorted_di[:show], sorted_d[:show]):
        # print('(' + format_tuple(di) + ') & (' + format_tuple(h)  + ') & (' + format_tuple(b) + ') & (' + format_tuple(d)  +')\\\\' )
        # print('\hline')
    # print('Dynamical Importance\tHarmonic Centrality\tBetweenness Centrality\tDegree Centrality')
    # for h, b, di, d in zip(sorted_h[:show], sorted_b[:show], sorted_di[:show], sorted_d[:show]):
    #     print('(' + format_tuple(di) + ')\t(' + format_tuple(h)  + ')\t(' + format_tuple(b) + ')\t(' + format_tuple(d)  +')' )

if __name__ == '__main__':
    main()
