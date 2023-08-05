import numpy as np
import scipy as sp
import nlopt
import math
from qutip import *
import qocttools.math_extra as math_extra
import qocttools.pulses as pulses
import qocttools.solvers as solvers
from time import time as clocktime

"""In this module, we implement the krotov´s algorithm, so we can use it when it´s required.

It´s very important that the pulse class is "Realtime", so the algorithms works fine (mainly for the coestate equation
and the non-linear schrodinger equation). In the case that is not, it´s added a conditional to convert the pulse so the
program is safe to use for every pulse parametrization. Note that no matter the pulse given as an input, the output will 
be always in the 'realtime' parametrization.

In this moments, the function are only checked with "realtime" pulse and "RK4" solver. A work to be done in the future is 
to implement every solver, but for now i think i must concentrate in RK4 and see if all works well.

There is a problem that makes the matrix_element to diverge in the case that we dont re-star the pulse (i need to work to
solve this).
"""

def Krotov (solve_method, H, f_initial, psi0, times, O, S,
                alpha = 2, 
                tolerance = 1E-03, 
                verbose = False, 
                maxeval = 100, 
                interaction_picture = False):
    """ This is the main function on the module.

    We can divide it in 3 main steps (after some initializing):

    1. Resolve a non-linear Schrödingers equation
    2. Checking if the pulse have converged enough
    3. Resolve a linear co-estate equation using the final condition of Schrödinger state
       (basically going backwards)

    Parameters
    ----------
    solve_method:
        string indicating the propagation method
    H0:
        Hamiltonian's time independet part. 
    V:
        Hamiltonian's perturbation component. 
    f_initial:
        pulse class defined in typical_pulse.py, specifically 'Realtime' parametrization
    psi0:
        initial state.
    time:
        array that contain each time step.
    O:
        Target operator that we want to optimice <ψ(T)|O|ψ(T)>
    S:
        Penalty function
    tolerance:
        Precision for the algorithm
    alpha:
        Penalty factor

    Returns
    -------
    pulse
    """
    #Some initalizing
    H0 = H.H0
    V = H.V[0]
    times_inverted = times[::-1]
    f = check_pulse(f_initial, times)
    dim = H0.shape[0]
    obj = psi0.type
    if verbose:  
        print('Object to propagate', obj)
        print('Tolerance', tolerance)
        print('Alpha', alpha)
    
    counter = 0
    #Solving the first lineal schrodinger equation
    t0 = clocktime()
    psi = solvers.solve(solve_method, H, f, psi0, times, 
                        returnQoutput = False, interaction_picture = interaction_picture)
    t1 = clocktime()
    psi_final = psi[-1]
    #print(psi_final)
    if verbose:
        Write_Status (obj, f, psi_final, times, O, S, alpha, dim, t0, t1, counter)

    #Solving the first coestate equation (with time inverted)
    chi = Coestate_eq(solve_method, H, f, psi_final, times_inverted, O, obj,
                      interaction_picture = interaction_picture)
    old_pulse = f
    #print(chi[-1])
    #Once done the initializing we can now jump into the 3 steps mentioned in the head
    #Lets solve the first non-linear equation outside the loop, so the convergence is check when enters the loop
    counter = 1
    t0 = clocktime()
    psi_final, f = non_linear_schr(solve_method, H0, V, f, chi, psi0, times, S,
                                   alpha = alpha,
                                   interaction_picture = interaction_picture)
    t1 = clocktime()
    #print(psi_final)
    if verbose:
        Write_Status (obj, f, psi_final, times, O, S, alpha, dim, t0, t1, counter)

    counter=2
    flag=0
    if verbose:    
        t0 = clocktime()
    
    while not have_converged(old_pulse, f, times, epsilon = tolerance):
        chi = Coestate_eq(solve_method, H, f, psi_final, times_inverted, O, obj,
                          interaction_picture = interaction_picture)
        old_pulse = f
        psi_final, f = non_linear_schr(solve_method, H0, V, f, chi, psi0, times, S,
                                       alpha = alpha,
                                       interaction_picture = interaction_picture)
        if verbose: 
            t1 = clocktime()
            Write_Status (obj, f, psi_final, times, O, S, alpha, dim, t0, t1, counter)
            t0 = clocktime()
        
        counter = counter+1

        if counter >= maxeval:
            print('Maximun number of iterations reached')
            flag=1
            break
    
    if verbose: print("End of optimization")
    return f.u, Write_Status(obj, f, psi_final, times, O, S, alpha, dim, t0, t1, counter, control = flag), flag


def non_linear_schr(solve_method, H0, V, f, chi, psi0, times, S, alpha = 2,
                    interaction_picture = False):
    """ This function solves the non-linear schrödinger equation that make the step 1 of the krotov´s algorithm.

    The main idea is to solve the ecuation time by time, calculating the pulse
    every time-step. (Must check if is good)

    For now, im just sticking to solve by rk4, but later i think is a good 
    idea that this should be generaliced for cfmagnus4 and cfmagnus2.
    """
    if solve_method == 'rk4':
        return rk4_nonlinear(H0, V, f, chi, Qobj(psi0), times, S, alpha = alpha, 
                             interaction_picture = interaction_picture)

    elif solve_method == 'cfmagnus2':
        raise Exception('cfmagnus2 not implemented yet')
        return cfmagnus2_nonlinear()#Function in progress

    elif solve_method == 'cfmagnus4':
        return cfmagnus4_nonlinear(H0, V, f, chi, Qobj(psi0), times, S, alpha = 2,
                    interaction_picture = interaction_picture)#Function in progress

def Write_Status (obj, f, psi_final, times, O, S, alpha, dim, t0, t1, counter, control = -1):
    if obj == 'oper':
        
        U_target = O.full()
        #gvalue = np.matmul(psi_final.conj().T, U_target).trace()
        gvalue = np.matmul(U_target.conj().T, psi_final).trace()
        gvalue = np.absolute(gvalue)**2 / (dim**2)
    else:
        gvalue = abs(expect(O,Qobj(psi_final)))
        
    if control == -1:
        pvalue = - alpha * sp.integrate.simps( f.fu(times[1:-1]) * f.fu(times[1:-1]) / S(times[1:-1]), times[1:-1] )
        tvalue = gvalue + pvalue
        print("{:d} gvalue = {:f}\tpvalue = {:f}\ttvalue = {:f} ({:f} s)".format(counter, gvalue, pvalue, tvalue, t1-t0))
    else:
        return gvalue

    #.. math::
    #   Coest = O\vert\Psi(t=T)\rangle
    #In the case of having a state propagating, and
    #.. math::                           
    #   \vert B(T)\rangle = Tr [U(T)+*O]*O/d^2
    #in the case of having an operator propagating.
    #The main idea is to solve it as an linear schrödinger equation but
    #*backwards*, so we have to take care of the time and the pulse in order to
    #make this correctly (with *realtime* parametrized pulses only is needed to 
    #invert the time).
    #In principle this should work with any solve_method: rk4, cfm2 or cmf4.



def Coestate_eq(solve_method, H, f, psiF, times, O, obj, interaction_picture = False):
    """This function calculate the coestate equation with the final condition described by

    .. math::
       \\vert\\chi(T)\\rangle = O\\vert \\Psi(t=T)\\rangle

    In the case of having a state propagating, and

    .. math::                           
       \\vert B(T)\\rangle = Tr [U(T)+*O]*O/d^2

    in the case of having an operator propagating.

    The main idea is to solve it as an linear schrödinger equation but
    *backwards*, so we have to take care of the time and the pulse in order to
    make this correctly (with *realtime* parametrized pulses only is needed to 
    invert the time).
    In principle this should work with any solve_method: rk4, cfm2 or cmf4.
    """
    #Calculating the "initial" coestate (actually the final)
    H0 = H.H0
    v = H.V
    if obj == 'oper':
        dim = H0.shape[0]
        U_target = O.full()
        
        #|B(T)>= Tr[U(T)*U_targ^H]*U_targ/d^2
        ini = U_target * np.matmul(U_target.conj().T, psiF).trace() /dim/dim
        #ini = ini * 2
        ini = Qobj(ini)
    
    else:
        #|Coestate(t=T)>=O|ψ(t=T)>  
        ini = O*Qobj(psiF)
        

    #Solving the equation "backwards"
    coestate=solvers.solve(solve_method, H, f, ini, times,
                        returnQoutput = False,
                        interaction_picture = interaction_picture)

    #Returning the coestate "fordwards", so we can operate with it directly
    return coestate[::-1]




def have_converged (old, new, times, epsilon = 1E-06):
    """ This function checks if the algorithm have converged enough. 

    The idea is to check every time of the pulse.

    Parameters
    ----------
    old:
        The pulse before solving the non-linear schrodinger
    new:
        The pulse after solving the non-linear schrodinger
    epsilon:
        The tolerance we have so we can say the pulse have converged enough

    Returns
    -------
    A boolean which is 'True' if every amplitude have converged, and is 'False' if any
    of the amplitudes have not converged enough
    """
    for i in range(times.shape[0]):
        if np.abs(old.fu(times[i])-new.fu(times[i]))>epsilon :
            return False
        if new.fu(times[i]) is np.nan:
            raise Exception('Pulse divergence')
        
    return True

def check_pulse (f, times):
    """ This function checks if the pulse parametrization is *realtime*.

    If it is not, it convert the pulse
    into *realtime* parametrization.
    """
    if f.type =='realtime':
        return f
    
    elif f.type =='fourier':
        ut = f.fu(times)
        ft = pulses.pulse("realtime", times[-1], u = ut)
        print('Initial pulse is in Fourier parametrization, changed into Realtime.')
        return ft

    elif f.type =='user_defined':
        ut = f.fu(times)
        ft = pulses.pulse("realtime", times[-1], u = ut)
        print('Initial pulse is in user_defined parametrization, changed into Realtime.')
        return ft

    else:
        raise Exception('The pulse is not well defined')

def rk4_nonlinear(H0, V, f, chi, psi0, times, S, alpha = 2,
                  interaction_picture = False):
    """ This function solves the nonlinear schordinger equation using rk4 as the integrator algorithm.

    It is a modification of the function rk4solver in the solvers module of 
    qocttools, so it can solve a slightly different equation and it can return the new state 
    and the new pulse.
    """
    if type(H0) is not qutip.qobj.Qobj:
        raise TypeError

    u_new=[]
    h0 = H0.full()
    v = V.full()
    dt = times[1]-times[0]
    dim = H0.shape[0]

    #What are we propagating?
    if psi0.type == 'oper':
        psi = psi0.full()
        y = np.zeros((2, dim, dim), dtype = complex)
        y[0] = psi
        y[1] = chi[0].copy()
        obj = 'oper'
    else:
        psi = psi0.full()[:, 0]
        y = np.zeros((2, dim), dtype = complex)
        y[0] = psi
        y[1] = chi[0].copy()
        obj = 'ket'


    def nlf(t, y):
        psi = y[0]
        chi = y[1]
        fy = y.copy()
        if interaction_picture:
            vi = solvers.intoper(v, np.diag(h0), t)
            if obj == 'ket' :
                V_Matrix_Element = np.vdot(chi, np.matmul(vi, psi))
            elif obj == 'oper':
                V_Matrix_Element = np.matmul(chi.conj().T, np.matmul(vi, psi)).trace()
            fpsi = - 1j * (S(t) * V_Matrix_Element.imag / alpha) * np.matmul(vi, psi)
            fchi = - 1j * f.fu(t) * np.matmul(vi, chi)
        else:
            vi = v.copy()
            if obj == 'ket' :
                V_Matrix_Element = np.vdot(chi, np.matmul(vi, psi))
            elif obj == 'oper':
                V_Matrix_Element = np.matmul(chi.conj().T, np.matmul(vi, psi)).trace()
            fpsi = - 1j * np.matmul(h0 + (S(t) * V_Matrix_Element.imag / alpha) * vi, psi)
            fchi = - 1j * np.matmul(h0 + f.fu(t) * vi, chi)

        fy[0] = fpsi
        fy[1] = fchi
        return fy

    if obj == 'ket' :
        V_Matrix_Element = np.vdot(chi[0], np.matmul(v, psi))
    elif obj == 'oper':
        V_Matrix_Element = np.matmul(chi[0].conj().T, np.matmul(v, psi)).trace()
    
    u_new.append(S(0) * V_Matrix_Element.imag / alpha)

    for j in range(times.size-1):
        y = math_extra.rk4(y, nlf, times[j], dt)

        psi_ = y[0]
        chi_ = y[1]

        if interaction_picture:
            vi = solvers.intoper(v, np.diag(h0), times[j+1])
        else:
            vi = v.copy()
    
        if obj == 'ket' :
            V_Matrix_Element = np.vdot(chi_, np.matmul(vi, psi_))
        elif obj == 'oper':
            V_Matrix_Element = np.matmul(chi_.conj().T, np.matmul(vi, psi_)).trace()
        
        u_new.append(S(times[j+1]) * V_Matrix_Element.imag / alpha)
    
    #Creating the new pulse
    f_new = pulses.pulse("realtime", times[-1], u = np.array(u_new))
    
    return psi_, f_new

def cfmagnus2_nonlinear(H0, V, f, chi, psi, times, alpha = 2):
    """ This function solves the nonlinear schordinger equation using cfmagnus2 as the integrator algorithm.
    """
    
def cfmagnus4_nonlinear(H0, V, f, chi, psi0, time, S, alpha = 2,
                        interaction_picture = False, cops = None):
    """ This function solves the nonlinear schordinger equation using cfmagnus4 as the integrator algorithm.
    """
    if type(H0) is not qutip.qobj.Qobj:
        raise TypeError

    u_new = []
    h0 = H0.full()
    dt = time[1]-time[0]
    dim = H0.shape[0]

    if psi0.type == 'oper':
        psi = psi0.full()
        obj = 'oper'
    else:
        psi = psi0.full()[:, 0]
        obj = 'ket'

    a1 = (3.0-2.0*np.sqrt(3.0))/12.0
    a2 = (3.0+2.0*np.sqrt(3.0))/12.0
    c1 = 0.5 - np.sqrt(3.0)/6.0
    c2 = 0.5 + np.sqrt(3.0)/6.0

    if obj == 'ket':
        V_Matrix_Element = np.vdot(chi[0], np.matmul(V.full(), psi))
   
    else:
        V_Matrix_Element = np.matmul(chi[0].conjugate().T, np.matmul(V.full(), psi)).trace()

    u_new.append(S(0) * V_Matrix_Element.imag / alpha)
    for j in range(time.size-1):
        t1 = time[j] + c1*dt
        t2 = time[j] + c2*dt
        if interaction_picture:
            # We will assume that H0 is diagonal on entry.
            M1 = np.zeros_like(h0)
            M2 = np.zeros_like(h0)
            #for k in range(len(V)):
            vi1 = solvers.intoper(V.full(), np.diag(h0), t1)
            vi2 = solvers.intoper(V.full(), np.diag(h0), t2)
            
            if obj == 'ket':
                V_Matrix_Element_1 = np.vdot(chi[j], np.matmul(vi1, psi))
                V_Matrix_Element_2 = np.vdot(chi[j], np.matmul(vi2, psi))

            else:
                V_Matrix_Element_1 = np.matmul(chi[j].conjugate().T, np.matmul(vi1, psi)).trace()
                V_Matrix_Element_2 = np.matmul(chi[j].conjugate().T, np.matmul(vi2, psi)).trace()

            #u_new.append(S(time[t])*)

            M1 = M1 + a1 * S(t1) * V_Matrix_Element_1.imag / alpha * vi1 + a2 * S(t2) * V_Matrix_Element_2.imag / alpha * vi2
            M2 = M2 + a2 * S(t1) * V_Matrix_Element_1.imag / alpha * vi1 + a1 * S(t2) * V_Matrix_Element_2.imag / alpha * vi2


        else:
            M1 = (a1 + a2) * h0
            M2 = (a1 + a2) * h0
            #for k in range(len(V)):
            
            M1 = M1 + a1 * S(t1) * V_Matrix_Element.imag / alpha * V.full() + a2 * S(t2) * V_Matrix_Element.imag / alpha * V.full()
            M2 = M2 + a2 * S(t1) * V_Matrix_Element.imag / alpha * V.full() + a1 * S(t2) * V_Matrix_Element.imag / alpha * V.full()

        M = M2
        psi = solvers.exppsi(2*M, cops, dt/2, psi)
        M = M1
        psi = solvers.exppsi(2*M, cops, dt/2, psi)

        #Saving Values
        if obj == 'ket':
            V_Matrix_Element = np.vdot(chi[j+1], np.matmul(V.full(), psi))
            
        else:
            V_Matrix_Element = np.matmul(chi[j+1].conjugate().T, np.matmul(V.full(), psi)).trace()
        
        u_new.append(S(time[j+1]) *V_Matrix_Element.imag / alpha)



    #Creating the new pulse
    f_new=pulses.pulse("realtime", time[-1], u = np.array(u_new))
    
    return psi, f_new


def coestate_interpolator(chi, times, coestate_flag, solve_method):
    """ This function interpolates the value of the coestate.

    In this way, we can solve properly the non-linear Schrodinger equation with the rk4 and cfmagnus4 integrators.
    This function returns the value of the coestate in the time that´s required
    """
    #We separate coestate_flag into int number (i), and decimal number (flag)
    flag, i = math.modf(coestate_flag)
    i=int(i)
    #If coestate_flag is an int number it´s not needed to interpolate
    if flag == 0:
        return chi[i]
    
    else:
        #Lets see if it´s solve by rk4 or cfmagnus4
        if solve_method == 'rk4':
            #If it´s rk4 and coestate_flag is not an int, neccesary we are in the case were we need to get the coestate in t+dt*0,5
            t_obj=times[i]+(times[i+1]-times[i])/2
            return chi[i]+(chi[i+1]-chi[i])/(times[i+1]-times[i])*(t_obj-times[i])

        elif solve_method == 'cfmagnus4':  
            return
        else:
            raise Exception('Don´t know propagation method')
