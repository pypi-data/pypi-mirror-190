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

import numpy as np
import qocttools.math_extra as math_extra
import qocttools.floquet as floquet
import qutip as qt

"""This module contains the Target class, and associated procedures.

"""

class Target:
    """The class that holds the definition of the target

    ...

    Parameters
    ----------
    targettype: string
        The code admits the following types of characters: ...
    """
    def __init__(self, targettype, 
                 Fyu = None,
                 dFdy = None,
                 dFdu = None,
                 Pu = None,
                 operator = None,
                 Utarget = None,
                 alpha = None,
                 S = None,
                 targeteps = None,
                 T = None,
                 fepsilon = None,
                 dfdepsilon = None):
        self.targettype = targettype
        if targettype == 'generic':
            self.Fyu_ = Fyu
            self.dFdy_ = dFdy
            self.operator = operator
            self.S = S
            self.alpha = alpha
        elif targettype == 'expectationvalue':
            self.Pu = Pu
            if isinstance(operator, list):
                self.operator = []
                for i in range(len(operator)):
                    self.operator.append(operator[i].copy())
            else:
                self.operator = [operator.copy()]
            self.alpha = alpha
            self.S = S
        elif targettype == 'evolutionoperator':
            self.Pu = Pu
            if isinstance(Utarget, list):
                self.Utarget = []
                for i in range(len(Utarget)):
                    self.Utarget.append(Utarget[i].copy())
            else:
                self.Utarget = [Utarget.copy()]
            self.operator = operator
            self.S = S
            self.alpha = alpha
        elif targettype == 'floquet':
            if targeteps is not None:
                self.targeteps = targeteps.copy()
            else:
                self.targeteps = None
            self.T = T
            self.operator = operator
            self.S = S
            self.alpha = alpha
            self.fepsilon_ = fepsilon
            self.dfdepsilon_ = dfdepsilon
        self.dFdu = dFdu


    def Fyu(self, y, u):
        """The functional F of the trayectory y that is to be maximized
        
        It may also be an explicit function of the control parameters u.

        Parameters
        ----------
        y : qutip.result 
            The trajectory of the quantum system
        u : ndarray
            The control parameters that were used to generate the trajectory.

        Returns
        -------
        float:
            The value of the target functional.
        """
        if self.targettype == 'generic':
            return self.Fyu_(y, u)

        if self.targettype == 'floquet':
            Fval = 1.0
            if not isinstance(y, list):
                UTset_ = [y]
            else:
                UTset_ = y
            nst = len(UTset_)
            dim = UTset_[0].dims[0][0]
            epsilon = np.zeros([nst, dim])
            for k in range(len(UTset_)):
                epsilon[k, :] = floquet.epsi(UTset_[k].full(), self.T)
            return self.f(epsilon)

        elif self.targettype == 'expectationvalue':
            if isinstance(y, list):
                ntgs = len(y)
                x = 0.0
                for j in range(len(y)):
                    x = x + qt.expect(self.operator[j], y[j])
            else:
                ntgs = 1
                x = qt.expect(self.operator[0], y)
            x = x / ntgs
            if self.Pu is not None:
                x = x + self.Pu(u)
            return x

        elif self.targettype == 'evolutionoperator':
            if isinstance(y, list):
                ntgs = len(y)
                x = 0.0
                for j in range(ntgs):
                    dim = y[j].shape[0]
                    x = x + (1/dim**2) * (np.absolute(math_extra.frobenius_product(self.Utarget[j], y[j])))**2
                x = x / ntgs
                return x
            else:
                dim = y.shape[0]
                return (1/dim**2)*(np.absolute(math_extra.frobenius_product(self.Utarget[0], y)))**2

    def dFdy(self, y, u):
        """Derivative of the target functional wrt the quantum trajectory.

        Right now, it in fact assumes that the functional only depends on the final
        state of the quantum trajectory. This functional derivative is used to determine
        the boundary condition used in the definition of the costate.

        Parameters
        ----------
        y: qutip.Qobj or list of qutip.Qobj
           The state of the system at the final time of the propagation
        u: ndarray
           The control parameters

        Returns
        -------
        qutip.Qobj or list of qutip.Qobj
           The derivative of F with respect to the quantum state.
        """
        if self.targettype == 'generic':
            return self.dFdy_(y, u)

        if self.targettype == 'floquet':
            if not isinstance(y, list):
                UTset_ = [y]
            else:
                UTset_ = y
            nst = len(UTset_)
            dim = UTset_[0].dims[0][0]
            epsilon = np.zeros([nst, dim])
            delta = 1.0e-4
            dfdy = []
            for k in range(len(UTset_)):
                dfdy.append(np.zeros([dim, dim], dtype = complex))
                UT = UTset_[k].full()
                epsilon[k, :] = floquet.epsi(UT, self.T)
                for i in range(dim):
                    for j in range(dim):
                        # Compute here dfdy[k][i, j]
                        UTp = UT.copy()
                        UTp[i, j] = UTp[i, j] + delta
                        epsilonp = floquet.epsi(UTp, self.T)
                        UTm = UT.copy()
                        UTm[i, j] = UTm[i, j] - delta
                        epsilonm = floquet.epsi(UTm, self.T)
                        dx = (epsilonp-epsilonm) / (2*delta)

                        UTp = UT.copy()
                        UTp[i, j] = UTp[i, j] + 1j*delta
                        epsilonp = floquet.epsi(UTp, self.T)
                        UTm = UT.copy()
                        UTm[i, j] = UTm[i, j] - 1j*delta
                        epsilonm = floquet.epsi(UTm, self.T)
                        dy = (epsilonp-epsilonm) / (2*delta)

                        d = 0.5 * (dx + 1j*dy)
                        #d = dx

                        for m in range(dim):
                            dfdy[k][i, j] += self.dfdepsilon(epsilon)[k, m] * d[m]

                dfdy[k] = qt.Qobj(dfdy[k])
            return dfdy

        elif self.targettype == 'expectationvalue':
            if isinstance(y, list):
                dF = []
                ntgs = len(y)
                for j in range(len(y)):
                    if y[j].isket:
                        dF.append(self.operator[j] * y[j] / ntgs)
                    else:
                        dF.append(0.5 * self.operator[j] / ntgs)
                return dF
            else:
                if y.isket:
                    return self.operator[0]*y
                else:
                    return 0.5 * self.operator[0]

        elif self.targettype == 'evolutionoperator':
            if isinstance(y, list):
                dF = []
                ntgs = len(y)
                for j in range(ntgs):
                    dim = y[j].shape[0]
                    dF.append( (1/dim**2) * math_extra.frobenius_product(self.Utarget[j], y[j])*self.Utarget[j] / ntgs)
                return dF
            else:
                dim = y.shape[0]
                return (1/dim**2) * math_extra.frobenius_product(self.Utarget[0], y)*self.Utarget[0]


    def f(self, eps):
        if self.fepsilon_ is not None:
            return self.fepsilon_(eps)
        cte = 1.0
        fval = 0.0
        nkpoints = eps.shape[0]
        targete = self.targeteps
        dim = eps.shape[1]
        fval = 0.0
        for k in range(nkpoints):
            for alpha in range(dim):
                fval = fval - cte * (eps[k, alpha] - targete[k, alpha])**2
        return fval


    def dfdepsilon(self, eps):
        if self.dfdepsilon_ is not None:
            return self.dfdepsilon_(eps)
        cte = 1.0
        nkpoints = eps.shape[0]
        targete = self.targeteps
        dim = eps.shape[1]
        dfval = np.zeros((nkpoints, dim))
        for k in range(nkpoints):
            for alpha in range(dim):
                dfval[k, alpha] = - 2.0 * cte * (eps[k, alpha]-targete[k, alpha])
        return dfval
