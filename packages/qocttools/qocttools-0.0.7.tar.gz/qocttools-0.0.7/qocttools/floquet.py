## Copyright 2019-present The qocttools developing team
##
## This file is part of qocttools.
##
## qocttools is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## qocttools is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with qocttools.  If not, see <https://www.gnu.org/licenses/>.

import qutip as qt
import numpy as np
import scipy as scp
import scipy.linalg as la
import qocttools.pulses as pulses
from qocttools.math_extra import diff_ridders


def epsi(UT, T):
    # In principle, one needs the eigenvalues. But what if UT cannot be diagonalized?
    # We will use then the Schur decomposition, and use the diagonal elements of the
    # Schur matrix.
    #evals, evecs = la.eig(UT)
    dim = UT.shape[0]
    S, Z = la.schur(UT)
    evals = np.zeros(dim, dtype = complex)
    for l in range(dim):
        evals[l] = S[l, l]
    eargs = np.angle(evals)
    eargs += (eargs <= -np.pi) * (2 * np.pi) + (eargs > np.pi) * (-2 * np.pi)
    epsilon = -eargs / T
    return np.sort(epsilon)


def epsilon(H, T, args = None):
    options = qt.Options(nsteps = 10000)
    #U = qt.propagator(H, T, args = args, options = options)
    ntsteps = 5
    dim = 3
    #print(ntsteps)
    U = (qt.sesolve(H, qt.qeye(dim), np.linspace(0, T, ntsteps), options = options, args = args)).states[-1]
    ualpha, epsilon = qt.floquet_modes(H, T, U = U)
    idx = epsilon.argsort()
    return epsilon[idx]


def epsilon2(H0, H1, H2, Ax, Ay, u, T):
    pulses.pulse_collection_set_parameters([Ax, Ay], u)
    H = [H0, [H1, Ax.f], [H2, Ay.f]]
    return epsilon(H, T)


def epsilon3(H, f, u, T):
    pulses.pulse_collection_set_parameters(f, u)
    if H.function:
        args = { "f": [f[l].fu for l in range(len(f))] }
        H_ = H.H0
    else:
        args = None
        H_ = [H.H0]
        k = 0
        for V in H.V:
            H_.append([V, f[k].f])
            k = k + 1
    return epsilon(H_, T, args = args)


def gradepsilon(H, f, u, T):
    dim = H.dim
    pulses.pulse_collection_set_parameters(f, u)

    if H.function:
        options = qt.Options(nsteps = 10000)
        args = { "f": [f[l].fu for l in range(len(f))] }
        H_ = H.H0
        ntsteps = 5
        U = (qt.sesolve(H_, qt.qeye(dim), np.linspace(0, T, ntsteps), options = options, args = args)).states[-1]
    else:
        args = None
        H0 = H.H0
        Vs = H.V
        H_ = [H.H0]
        k = 0
        for V in H.V:
            H_.append([V, f[k].f])
            k = k + 1
        options = qt.Options(nsteps = 10000)
        U = qt.propagator(H_, T, options = options)

    ualpha, epsilon = qt.floquet_modes(H_, T, U = U)
    idx = epsilon.argsort()
    epsilon = epsilon[idx]
    ualpha_ = [ualpha[j] for j in idx]
    ualpha = ualpha_
    times = np.linspace(0, T, 100)
    dt = times[1]
    ualphat = qt.floquet.floquet_modes_table(ualpha, epsilon, times, H_, T, args = args)

    nu = 0
    for ip in range(len(f)):
        nu = nu + f[ip].nu
    res = np.zeros((dim, nu))

    if H.function:
       Vs_ = []
       for ip in range(len(f)):
           Vs_.append( np.empty(times.shape[0], dtype = qt.Qobj) )
       for j in range(times.shape[0]):
           t = times[j]
           for ip in range(len(f)):
               Vs_[ip][j] = H.V[ip](times[j], args)

    m = 0
    for ip in range(len(f)):
        ft = f[ip]
        if H.function:
            V = Vs_[ip]
        else:
            V = Vs[ip]
        for k in range(f[ip].nu):
            if H.function:
                for alpha in range(dim):
                    res[alpha, m] = 0.5 * (qt.expect(V[0], ualphat[0][alpha]) * ft.dfu(times[0], k) )
                    for j in range(1, times.shape[0]-1):
                        res[alpha, m] = res[alpha, m] + (qt.expect(V[j], ualphat[j][alpha]) * ft.dfu(times[j], k) )
                    res[alpha, m] = res[alpha, m] + 0.5 * (qt.expect(V[j], ualphat[-1][alpha]) * ft.dfu(times[-1], k) )
            else:
                for alpha in range(dim):
                    res[alpha, m] = 0.5 * (qt.expect(V, ualphat[0][alpha]) * ft.dfu(times[0], k) )
                    for j in range(1, times.shape[0]-1):
                        res[alpha, m] = res[alpha, m] + (qt.expect(V, ualphat[j][alpha]) * ft.dfu(times[j], k) )
                    res[alpha, m] = res[alpha, m] + 0.5 * (qt.expect(V, ualphat[-1][alpha]) * ft.dfu(times[-1], k) )
            m = m + 1

    return res * dt/T


def vectortodm(rhovec):
    dim = round(np.sqrt(rhovec.shape[0]))
    return qt.vector_to_operator(qt.Qobj(rhovec, dims = [[[dim], [dim]], [1]]))


def dmtovector(rho):
    """
    Transforms a Qobj density matrix object into a Qobj vector

    Parameters
    ----------
    rho : Qobj
         Density matrix

    Returns
    -------
    Qobj
        A Qobj vector containing the vectorized version of the input density matrix

    """
    dim = rho.dims[0][0]
    #return qt.Qobj(qt.operator_to_vector(rho), dims = [[4], [1]])
    return qt.Qobj(qt.operator_to_vector(rho), dims = [[dim**2], [1]])


#def fourier_steady_state2(T, ntsteps, L0, LVlist, nu = None, dgt = None):
def fourier_steady_state2(T, ntsteps, L, f, nu = None, dgt = None):
    compute_gradient = False
    if nu is not None:
        compute_gradient = True

    L0 = L.H0.full()
    LVlist = []
    for k in range(len(L.V)):
        LVlist.append([L.V[k].full(), f[k].f])

    nv = len(LVlist)
    #print("nv = {}".format(nv))
    if compute_gradient:
        if len(nu) != nv or len(dgt) != nv:
            raise Exception("The lengths of nu and dgt should be equal to the length of LVlist")
        Nu = sum(nu)
        #print("Nu = {}".format(Nu))

    LV = []
    gt = []
    for h in range(nv):
        LV.append(LVlist[h][0])
        gt.append(LVlist[h][1])

    times = np.linspace(0, T, ntsteps+1)
    dt = times[1]

    dim = L0.shape[0]
    d = round(np.sqrt(dim))
    #print("dim = {}".format(L0.shape[0]))
    #print("d = {}".format(d))

    #gfunc = np.zeros(ntsteps)
    gfunc = np.zeros([nv, ntsteps])
    if compute_gradient:
        gradg = np.zeros([Nu, ntsteps])
    #for j in range(ntsteps):
    #    gfunc[j] = gt(times[j], None)
    #    for k in range(nu):
    #        gradg[k, j] = dgt(times[j])[k]
    for h in range(nv):
        for j in range(ntsteps):
            gfunc[h, j] = gt[h](times[j], None)
            if compute_gradient:
                l = 0
                for h in range(nv):
                    for k in range(nu[h]):
                        gradg[l, j] = dgt[h](times[j])[k]
                        l = l + 1
    
    lind = np.zeros([dim, dim, ntsteps], dtype = complex)
    for alpha in range(dim):
        for beta in range(dim):
            for j in range(ntsteps):
                #lind[alpha, beta, j] = L0[alpha, beta] + gt(times[j], None) * LV[alpha, beta]
                lind[alpha, beta, j] = L0[alpha, beta] #+ gt(times[j], None) * LV[alpha, beta]
                for h in range(nv):
                    lind[alpha, beta, j] = lind[alpha, beta, j] + gt[h](times[j], None) * LV[h][alpha, beta]

    if compute_gradient:
        dlind = np.zeros([Nu, dim, dim, ntsteps], dtype = complex)
        l = 0
        for h in range(nv):
            for k in range(nu[h]):
                for alpha in range(dim):
                    for beta in range(dim):
                        for j in range(ntsteps):
                            dlind[l, alpha, beta, j] = dgt[h](times[j])[k] * LV[h][alpha, beta]
                l = l + 1
                
    ws = np.zeros(ntsteps, dtype = float)
    for m in range((ntsteps)//2):
        ws[m] = (2.0*np.pi/T) * m
    for m in range((ntsteps)//2, ntsteps):
        ws[m] = (2.0*np.pi/T) * (m-ntsteps)

    lindw = np.zeros([dim, dim, ntsteps], dtype = complex)
    for alpha in range(dim):
        for beta in range(dim):
            lindw[alpha, beta, :] = scp.fft.fft(lind[alpha, beta, :]) / (ntsteps)

    #sparsity = 1.0 - ( np.count_nonzero(lindw) / float(lindw.size))
    #print("Sparsity = {}".format(sparsity))

    if compute_gradient:
        dlindw = np.zeros([Nu, dim, dim, ntsteps], dtype = complex)
        for k in range(Nu):
            for alpha in range(dim):
                for beta in range(dim):
                    dlindw[k, alpha, beta, :] = scp.fft.fft(dlind[k, alpha, beta, :]) / (ntsteps)

    def kdelta(i, j):
        if i == j:
            return 1
        else:
            return 0

    def tracef(x):
        tr = 0.0
        for j in range(d):
            tr = tr + x[j*(d+1)*ntsteps: j*(d+1)*ntsteps+ntsteps].sum()
        return tr

    fdim = dim * ntsteps
    lindb = np.zeros([fdim, fdim], dtype = complex)
    for i in range(fdim):
        alpha = i // ntsteps
        n = i % ntsteps
        for j in range(fdim):
            beta = j // ntsteps
            m = j % ntsteps
            lindb[i, j] = lindw[alpha, beta, n-m] - 1j * ws[m] * kdelta(i, j)
    #sparsity = 1.0 - ( np.count_nonzero(lindb) / float(lindb.size))
    #print("Sparsity (2) = {}".format(sparsity))

    if compute_gradient:
        dlindb = np.zeros([Nu, fdim, fdim], dtype = complex)
        for k in range(Nu):
            for i in range(fdim):
                alpha = i // ntsteps
                n = i % ntsteps
                for j in range(fdim):
                    beta = j // ntsteps
                    m = j % ntsteps
                    dlindb[k, i, j] = dlindw[k, alpha, beta, n-m]
        #sparsity = 1.0 - ( np.count_nonzero(dlindb) / float(dlindb.size))
        #print("Sparsity (3) = {}".format(sparsity))
            
    b = scp.linalg.null_space(lindb)
    bw = b.reshape([dim, ntsteps])
    bt = np.zeros([dim, ntsteps], dtype = complex)
    for alpha in range(dim):
        bt[alpha, :] = scp.fft.ifft(bw[alpha, :]) * ntsteps
    rho0__ = bt[:, 0]
    rho0 = vectortodm(rho0__)
    trace = rho0.tr()
    trace2 = tracef(b)
    b = b / trace2
    bt = bt / trace2
    rho0 = rho0 / rho0.tr()

    if compute_gradient:

        rhs = np.zeros([dim*ntsteps, Nu], dtype = complex)
        for k in range(Nu):
            rhs[:, k] = - np.matmul(dlindb[k, :, :], b)[:, 0]
        x, residuals, rank, svs = np.linalg.lstsq(lindb, rhs, rcond = None)
        #print('rank = {}'.format(rank))

        for k in range(Nu):
            x[:, k] = x[:, k] - tracef(x[:, k]) * b[:, 0]

        xw = np.zeros([Nu, dim, ntsteps], dtype = complex)
        for k in range(Nu):
            xw[k, :, :] = x[:, k].reshape([dim, ntsteps])

        xt = np.zeros([Nu, dim, ntsteps], dtype = complex)
        for k in range(Nu):
            for alpha in range(dim):
                xt[k, alpha, :] = scp.fft.ifft(xw[k, alpha, :]) * ntsteps

    if compute_gradient:
        return bt, xt, x
    else:
        return bt


class Nessopt:
    """
    Optimization of NESSs
    """
    #def __init__(self, target_operator, T, nts, L0, LVlist, glist):
    def __init__(self, target_operator, T, nts, L, glist):
        self.target_operator = target_operator
        self.avector = dmtovector(target_operator).full()[:, 0]
        self.T = T
        self.nts = nts
        self.glist = glist
        self.L = L
        self.L0 = L.H0.full()
        self.LVlist = []
        for k in range(len(L.V)):
            self.LVlist.append([L.V[k].full(), glist[k].f])

    def Afunc(self, y):
        return (1/self.T) * np.vdot(y, self.avector).real

    def F(self, y):
        times = np.linspace(0, self.T, self.nts+1)
        integrand = np.zeros(self.nts+1)
        for j in range(self.nts):
            integrand[j] = self.Afunc(y[:, j])
        integrand[self.nts] = integrand[0]
        return scp.integrate.simps(integrand, times)

    def Fdy(self, dy):
        nu = dy.shape[0]
        nts = dy.shape[2]
        times = np.linspace(0, self.T, nts+1)
        integrand = np.zeros([nu, nts+1])
        for l in range(nu):
            for j in range(nts):
                integrand[l, j] = self.Afunc(dy[l, :, j])
            integrand[l, nts] = self.Afunc(dy[l, :, 0])
        return np.array( [ scp.integrate.simps(integrand[l, :], times) for l in range(nu)] )

    def G(self, u):
        pulses.pulse_collection_set_parameters(self.glist, u)
        y0 = fourier_steady_state2(self.T, self.nts, self.L, self.glist)
        return self.F(y0)

    def gradG(self, u):
        g1 = self.glist[0]
        g2 = self.glist[1]
        pulses.pulse_collection_set_parameters(self.glist, u)
        y0, drhostdu, dy_ = fourier_steady_state2(self.T, self.nts, self.L, self.glist,
                                                  nu = [g1.nu, g2.nu],
                                                  dgt = [g1.gradf, g2.gradf])
        Fy0 = self.F(y0)
        gradG = self.Fdy(drhostdu)
        return Fy0, gradG

    def dGdu_fd(self, u, m, delta = 0.01):
        pulses.pulse_collection_set_parameters(self.glist, u)
        def f(x):
            u0 = u.copy()
            u0[m] = x
            return self.G(u0)
        val, err = diff_ridders(f, u[m], delta)
        pulses.pulse_collection_set_parameters(self.glist, u)
        return val

    def gradG_fd(self, u):
        p = u.shape[0]
        dGdunum = np.zeros(p)
        for m in range(p):
            dGdunum[m] = self.dGdu_fd(u, m)
        return dGdunum

    def make_G(self):
        def Gfunction(u, grad = None):
            g1 = self.glist[0]
            g2 = self.glist[1]
            pulses.pulse_collection_set_parameters([g1, g2], u)
            # if (grad is not None):
            #     if grad.size > 0:
            #         Gu, grad[:] = self.gradG(u)
            #         pulses.pulse_collection_set_parameters([g1, g2], u)
            #     print("Exitinng Gfunction with gradient")
            #     return Gu
            if (grad is not None) and (grad.size > 0):
                Gu, grad[:] = self.gradG(u)
                pulses.pulse_collection_set_parameters([g1, g2], u)
                return Gu
            else:
                return self.G(u)
        return Gfunction
