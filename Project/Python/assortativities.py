import loader
import networkx as nx
import matplotlib.pyplot as plt

def get_assorts(G, labels):
    assorts = []

    for label in labels:
        assorts.append(nx.attribute_assortativity_coefficient(G, label))
        print(label, ': ', assorts[-1])

    assorts.append(nx.degree_assortativity_coefficient(G))

    return assorts

def main():
    levels = [2, 3, 4]

    G = loader.get_graph(levels, labels=True)

    labels = ['Age','Birthplace','Residence','Arrests','Convictions','Prison','Music']

    init_assorts = get_assorts(G, labels)

    labels.append('Degree')

    print(init_assorts)

    plt.figure(1)
    plt.subplot(311)
    ax = plt.gca()

    rects = ax.bar(range(len(labels)), init_assorts)
    ax.set_title('Assortativity Coefficent by Attribute for All Crimes')

    ax.set_ylabel('Assortativity Coefficient')
    ax.set_xticklabels([])

    plt.subplot(312)
    ax = plt.gca()
    levels = [3, 4]

    G = loader.get_graph(levels, labels=True)

    labels = ['Age','Birthplace','Residence','Arrests','Convictions','Prison','Music']

    init_assorts = get_assorts(G, labels)

    labels.append('Degree')

    rects = ax.bar(range(len(labels)), init_assorts)
    ax.set_title('Assortativity Coefficent by Attribute for Serious Crimes')
    
    ax.set_ylabel('Assortativity Coefficient')
    ax.set_xticklabels([])

    plt.subplot(313)
    ax = plt.gca()
    levels = [2]

    G = loader.get_graph(levels, labels=True)

    labels = ['Age','Birthplace','Residence','Arrests','Convictions','Prison','Music']

    init_assorts = get_assorts(G, labels)

    labels.append('Degree')

    rects = ax.bar(range(len(labels)), init_assorts)
    ax.set_title('Assortativity Coefficent by Attribute for Petty Crimes')
    ax.set_xlabel('Attribute')
    ax.set_ylabel('Assortativity Coefficient')
    ax.set_xticklabels([''] + labels)

    plt.show()

if __name__ == '__main__':
    main()
