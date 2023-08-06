import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import iar
from numpy import linalg as LA
from numba import njit

def IARPhi_sample(phi, n, st):
    Sigma = np.zeros((n, n))
    for i in range(0, n):
        d = st[i] - st[i:n]
        Sigma[i, i:n] = phi[i]**abs(d)
        Sigma[i:n, i] = Sigma[i, i:n]
    val, vec = LA.eig(Sigma)
    A = np.matmul(np.matmul(vec, np.diag(np.sqrt(val))), np.transpose(vec))
    e = np.random.normal(size = n)
    y = np.dot(A,e)
    return y, st
