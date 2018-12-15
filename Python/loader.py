import networkx as nx
import pandas as pd
import numpy as np


def apply_labels(G):
    df = pd.read_csv('../CSV/LONDON_GANG_ATTR.csv')

    attrs = {}

    for i, row in df.iterrows():
        attrs[i] = {'Age':row['Age'], 'Birthplace':row['Birthplace'], 'Residence':row['Residence'], 'Arrests':row['Arrests'], 'Convictions':row['Convictions'], 'Prison':row['Prison'], 'Music':row['Music']}

    nx.set_node_attributes(G, attrs)

    #print(nx.get_node_attributes(G, 'Music'))


def get_adj_matrix(levels=None):
    df = pd.read_csv('../CSV/LONDON_GANG.csv')

    df = df.drop(df.columns[0], axis=1)

    if levels == None:
        print('levels = none')
        levels = [1,2,3,4]

    iA = np.isin(df.values, levels)

    A = np.where(iA, 1, 0)

    return A

def get_graph(levels=None, labels=False):
    G = get_graph_from_adj(get_adj_matrix(levels))

    if labels == False:
        return G

    apply_labels(G)

    return G

def get_graph_from_adj(adj):
    return nx.from_numpy_array(adj)

def main():

    G = get_graph(levels=[2,3,4], labels=False)
    print('All edges: ', len(G.edges()))

    G = get_graph(levels=[3,4])
    print('serious edges: ', len(G.edges()))

    G = get_graph(levels=[2])
    print('petty edges: ', len(G.edges()))

if __name__ == '__main__':
    main()
