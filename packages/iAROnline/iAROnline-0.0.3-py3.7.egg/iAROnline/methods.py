import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import iar
from numpy import linalg as LA
from numba import njit


@njit
def IAR_OBI(n, y, times, m0 = 0, P0 = 1):
    sigma = 1
    Estima = np.zeros(n)
    Estima[0] = m0
    X_p = np.zeros(n-1)
    loss = np.zeros(n-1)
    RMSE = np.zeros(n-1)
    acum = 0
    mean_RMSE = 0
    for i in range(1,n):
        HH_1 = y[i-1]
        HH   = y[i]
        phi_1 = Estima[i-1] 
        distancia = times[i] - times[i-1]
        if(distancia > 0):
            V = sigma*(1-phi_1**(2*distancia))
            a1 = ((m0/P0) + (((phi_1**(distancia-1))*(HH_1*HH))/V)) * ((1/P0) + (((phi_1**(2*distancia-2))*(HH_1**2))/V))**(-1)
            if(a1 > 1.0 or a1 < 0.0):
                a1 = phi_1
            b1 = ((1/P0) + (((phi_1**(2*distancia-2))*(HH_1**2))/V))**(-1)
            Estima[i] = a1
        elif (distancia == 0):
            Estima[i] = Estima[i-1]
        m0 = a1
        P0 = b1
        X_t = (a1**distancia)*HH_1
        X_p[i-1] = X_t
        loss[i-1] = (HH -  X_t)**2
        acum = acum + loss[i-1]
        RMSE[i-1] = acum/(i)
        mean_RMSE = mean_RMSE + RMSE[i-1]
    mean_RMSE = mean_RMSE/(n-1)
    return Estima, RMSE, mean_RMSE, X_p, loss

    
@njit
def IAR_OBR(n, y, times, m0, P0):
    sd = np.std(y)
    mk = m0
    Pk = P0
    difer = np.diff(times)
    Param = np.zeros(n)
    Param[0] = m0
    VarPar = np.zeros(n)
    VarPar[0] = P0
    Pred = np.zeros(n)
    MSE = np.zeros(n)
    for k in range(1, n):
        sigma2 = (sd**2)*(1-abs(mk**(difer[k-1]))**2)
        Sk = (y[k-1] * Pk * y[k-1]) + sigma2
        Kk = Pk * y[k-1] * (Sk**(-1))
        mk = mk + Kk * (y[k] - y[k-1] * mk**difer[k-1])
        
        if (mk < 0):
            mk = 0.00001
        if (mk >= 1):
            mk = 0.999999
        Pk = Pk - Kk * Sk * Kk
        if (Pk < 0.005):
            Pk = 0.05
        Param[k] = mk
        VarPar[k] = Pk
        Pred[k] = (mk**difer[k-1])*y[k-1]

    acum = (y[1]-Pred[1])**2
    i = 2
    while(i <= n):
        MSE[i-1] = acum/(i-1)
        acum += (y[i]-Pred[i])**2
        i += 1
    mean_MSE = np.mean(MSE[2:])
    return Param, VarPar, Pred, MSE, mean_MSE

@njit
def update_OGD(y, delta, y0, xhat0, L, learning_rate=0.01):
    K = 0
    nabla = -2*(y-xhat0)*y0*(delta)*(L**(delta-1))
    K = L - learning_rate*nabla
    if K >= 1:
        K = 0.99
    elif K <= 0:
        K = 0.01
    return K

@njit
def IAR_OGD(y, st, L, learning_rate=0.01):
    T = len(y)
    L1 = np.zeros(T)
    L1[0] = L
    X_p = np.zeros(T)
    loss = np.zeros(T)
    MSE = np.zeros(T)
    for t in range(1, T):
        X_t = 0
        X_t = X_t + (L1[t-1]**(st[t]-st[t-1]))*y[t-1]
        X_p[t] = X_t
        loss[t] = (y[t] - X_t)**2
        L = update_OGD(y=y[t], delta=st[t]-st[t-1], y0=y[t-1],
                       xhat0=X_t, L=L, learning_rate=learning_rate)
        L1[t] = L

    acum = loss[1]
    i = 1
    while(i < T):
        MSE[i] = acum/i
        i += 1
        acum += loss[i]
        
    
    mean_MSE = np.mean(MSE[1:])
    return L1, loss, X_p, MSE, mean_MSE

@njit
def update_ONS(y, delta, y0, xhat0, L, A, learning_rate=0.01):
    D = 2
    K = 0
    nabla = -2*(y-xhat0)*y0*(delta)*(L**(delta-1))
    A = A + nabla*nabla
    K = L - (1/learning_rate)*(1/A)*nabla
    if K > 1:
        K = 0.9999999999999999999999999999
    elif K < 0:
        K = 0.01
    return A, K

@njit
def IAR_ONS(y, st, L):
    T = len(y)
    L1 = np.zeros(T)
    L1[0] = L
    Xmax = np.max(np.abs(y))
    D = 2
    G = 2*(Xmax)**2
    Rate = 0.5*np.minimum(1, 4*D*G)
    A = 1/((Rate**2)*(D**2))
    MSE = np.zeros(T)
    x_p = np.zeros(T)
    loss = np.zeros(T)
    for t in range(0, T):
        x_t = 0
        if t > 0:
            x_t = (L1[t-1]**(st[t]-st[t-1]))*y[t-1]
        x_p[t] = x_t
        loss[t] = (y[t]-x_t)**2
        if t > 0:
            A, L = update_ONS(y=y[t], delta=st[t]-st[t-1],
                              y0=y[t-1], xhat0=x_t, L=L, A=A, learning_rate=Rate)
            L1[t] = L
    
    acum = loss[1]
    i = 1
    while(i < T):
        MSE[i] = acum/i
        i += 1
        acum += loss[i]
    
    mean_MSE = np.mean(MSE[1:])
    return L1, loss, x_p, MSE, mean_MSE

@njit
def IARg_OGD(y, st, L0, learning_rate):
    n = len(y)
    L = np.zeros(2)
    L[1] = L0[1]
    L[0] = y[0]
    Mu = np.zeros(n+1)
    Mu[0] = L[0]
    Phi = np.zeros(n+1)
    Phi[0] = L[1]
    x_p = np.zeros(n)
    loss = np.zeros(n)
    RMSE = np.zeros(n)
    nabla = np.zeros(2)
    for t in range(0,n):
        x_t = 0
        if(t > 0):
            x_t = L[0] + ((L[1]**(st[t]-st[t-1]))*y[t-1])
        x_p[t] = x_t
        loss[t] = (y[t]-x_t)**2
        if(t > 0):
            nabla[0] = -2*(y[t]-x_t)
            DT = st[t]-st[t-1]
            nabla[1] = nabla[0]*y[t-1]*DT*(L[1]**(DT-1))
        L[0] = L[0] - learning_rate*nabla[0]
        L[1] = L[1] - learning_rate*nabla[1]
        if(L[1]>1):
            L[1] = 0.999999999999999
        elif(L[1] < 0):
            L[1] = 0.01
        if(L[0]<0):
            L[0] = 0.01
        Mu[t+1] = L[0]
        Phi[t+1] = L[1]
    acum = 0
    for i in range(0,n):
        acum = acum + loss[i]
        RMSE[i] = (acum/(i+1))**(0.5)
    
    return Mu, Phi, loss, RMSE

@njit
def solve(input):
    output = np.zeros(4)
    det = (input[0]*input[3])-(input[1]*input[2])
    output[0] = input[3]/det
    output[1] = -input[1]/det
    output[2] = -input[2]/det
    output[3] = input[0]/det
    return output

@njit
def IARg_ONS(y, st, L0):
    n = len(y)
    L = np.zeros(2)
    L[1] = L0[1]
    L[0] = y[0]
    L1 = np.zeros(n+1)
    L1[0] = L[0]
    L2 = np.zeros(n+1)
    L2[0] = L[1]
    x_p = np.zeros(n)
    loss = np.zeros(n)
    RMSE = np.zeros(n)
    Xmax = np.max(np.abs(y))
    D = 2*(2**0.5)
    G = D*(Xmax*Xmax)
    Rate = 0.5*min(1/(1),4*D*G)
    Epsilon = 1/((Rate*Rate)*(D*D))

    A = np.zeros(4)
    A[0] = Epsilon
    A[3] = Epsilon
    x_t = 0
    nabla = np.zeros(2)
    tempSolve = np.zeros(4)
    DT = 0
    acum = 0
    for t in range(0,n):
        x_t = 0
        if(t>0):
            x_t = L[0] +((L[1]**(st[t]-st[t-1]))*y[t-1])
        x_p[t] = x_t
        loss[t] = (y[t]-x_t)**2
        if(t>0):
            nabla[0] = -2*(y[t]-x_t)
            DT = st[t] -st[t-1]
            nabla[1] = -2*(y[t]-x_t)*y[t-1]*DT*(L[1]**(DT-1))
        A[0] = A[0]+nabla[0]*nabla[0]
        A[1] = A[1]+nabla[1]*nabla[0]
        A[2] = A[2]+nabla[1]*nabla[0]
        A[3] = A[3]+nabla[1]*nabla[1]
        tempSolve = solve(A)
        L[0] = L[0]-(1/Rate)*(tempSolve[0]*nabla[0]+tempSolve[1]*nabla[1])
        L[1] = L[1]-(1/Rate)*(tempSolve[2]*nabla[0]+tempSolve[3]*nabla[1])
        if(L[1]>1):
            L[1] = 0.99999999999999999999
        elif(L[1] < 0):
            L[1] = 0.01
        if(L[0]<0.0):
            L[0] = 0.01
        L1[t+1] = L[0]
        L2[t+1] = L[1]
        acum = acum + loss[t]
        RMSE[t] = (acum/(t+1))**0.5
    return loss, RMSE, L1, L2
