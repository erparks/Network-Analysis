import loader
from scipy.linalg import eigh
import numpy as np

def get_largest_eval(adj):
    evals, evecs = eigh(adj)

    return max(evals)

def get_dynamical_importance(start_eval, adj, i):
    result_adj = np.delete(adj, i, axis=0)
    result_adj = np.delete(result_adj, i, axis=1)

    result_eval = get_largest_eval(result_adj)

    return (start_eval - result_eval)/start_eval

def get_dynamical_importances(adj):
   
    starting_eval = get_largest_eval(adj)

    dis = {}

    for i in range(0, len(adj)):
        dis[i] = get_dynamical_importance(starting_eval, adj, i)

    return dis

def main():
    np.set_printoptions(threshold=np.nan)
    
    adj = loader.get_adj_matrix([2,3,4])

    dis = get_dynamical_importances(adj)
    
    for i, di in dis.items():
        print(i, di)
    

if __name__ == '__main__':
    main()
