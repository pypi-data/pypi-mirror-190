#cython: boundscheck=False, wraparound=False, nonecheck=True, cdivision = True

import numpy as np
from libc.math cimport sin, cos, sqrt


def fe(double t, double T, int M, double [:] u):
    cdef int k
    cdef double y, w
    cdef double pi = np.pi
    y = u[0] / sqrt(T)
    for k in range(M):
        w = 2*(k+1)*pi/T
        y += (2/sqrt(T)) * (u[2*k+1]*sin(w*t) +
                            u[2*k+2]*cos(w*t))
    return y


def dfe(double t, double T, int M, double [:] u, int m):
    cdef int m2
    cdef double w
    cdef double pi = np.pi
    if(m == 0):
        return 1.0/sqrt(T)
    elif(m % 2 == 0):
        m2 = int(m/2)
        w = 2*m2*np.pi/T
        return (2/sqrt(T)) * cos(w*t)
    else:
        m2 = int((m+1)/2)
        w = 2*m2*np.pi/T
        return (2/sqrt(T)) * sin(w*t)


def fourierexpansion(t, double T, int nu, double [:] u):
    cdef int M, j
    M = int((nu-1)/2)
    cdef double [:] ts
    cdef double [:] yy
    if isinstance(t, float):
        return fe(t, T, M, u)
    else:
        ts = t
        yt = np.zeros(t.shape[0])
        yy = yt
        for j in range(t.shape[0]):
            yy[j] = fe(ts[j], T, M, u)
        return yt



def dfourierexpansion(t, double T, int nu, double [:] u, int m):
    cdef int M, j
    M = int((nu-1)/2)
    cdef double [:] ts
    cdef double [:] yy
    if isinstance(t, float):
        return dfe(t, T, M, u, m)
    else:
        ts = t
        yt = np.zeros(t.shape[0])
        yy = yt
        for j in range(t.shape[0]):
            yy[j] = dfe(ts[j], T, M, u, m)
        return yt