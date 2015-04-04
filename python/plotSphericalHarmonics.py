# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Copyright ANDRÉS PÉREZ LÓPEZ, January 2014
contact@andresperezlopez.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            AMBISONICS ENCODING SIMULATIONS

Following code provides some visualization tools for ambisonics encoding, up to 3rd order

Conventions used:
    - elevation defined as theta [-pi/2,pi/2]
    - azimut defined as phi [0,2*pi]
    - encoding with N3D coefficients
    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from numpy import *
import matplotlib.pyplot as plt
from matplotlib import animation


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
functions to calculate spherical harmonics coefficients up to 3rd order 

use of 3D Normalized Coefficients (N3D)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def nullOrder(theta,phi):
    """
    calculate zero order spherical harmonics
    """
    W=ones(max(size(theta),size(phi)))
    
    return W

def firstOrder(theta,phi):
    """
    calculate first order spherical harmonics
    """
    X=sqrt(3.)*cos(theta)*cos(phi)
    Y=sqrt(3.)*cos(theta)*sin(phi)
    Z=sqrt(3.)*sin(theta)
    
    return X,Y,Z

def secondOrder(theta,phi):
    """
    calculate second order spherical harmonics
    """
    V=sqrt(5.)*sqrt(3.)/2.*sin(2.*phi)*(cos(theta)**2.)
    T=sqrt(5.)*sqrt(3.)/2.*sin(phi)*sin(2.*theta)
    R=sqrt(5.)*(3.*(sin(theta)**2.)-1.)/2
    S=sqrt(5.)*sqrt(3.)/2.*cos(phi)*sin(2*theta)
    U=sqrt(5.)*sqrt(3.)/2.*cos(2.*phi)*(cos(theta)**2.)
    
    return V,T,R,S,U
    
def thirdOrder(theta,phi):
    """
    calculate third order spherical harmonics
    """
    Q=sqrt(7.)*sqrt(5./8.)*sin(3.*phi)*(cos(theta)**3.)
    O=sqrt(7.)*sqrt(15.)/2.*sin(2.*phi)*sin(theta)*cos(theta)**2.
    M=sqrt(7.)*sqrt(3./8.)*sin(phi)*cos(theta)*(5.*sin(theta)**2.-1.)
    K=sqrt(7.)*sin(theta)*(5.*sin(theta)**2.-3.)/2.
    L=sqrt(7.)*sqrt(3./8.)*cos(phi)*cos(theta)*(5.*sin(theta)**2.-1.)
    N=sqrt(7.)*sqrt(15.)/2.*cos(2.*phi)*sin(theta)*cos(theta)**2.
    P=sqrt(7.)*sqrt(5./8.)*cos(3.*phi)*cos(theta)**3.
    
    return Q,O,M,K,L,N,P
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
functions to help with computing and plotting
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def isZero(x):
    """
    test if all components of the given array are zero
    """
    if all(x==zeros(x.size)):
        ans=True
    else: 
        ans=False
        
    return ans
    
def separateSign(x):
    """
    given a ndarray, split it into two arrays, for positive and negative values respectively;
    negative array is further multiplied for -1
    
    this function is useful for polar representations
    """
    condition=[x<0,x>=0]
    #positive array
    choice_pos=[0,x]
    pos=select(condition,choice_pos)
    #negative array
    choice_neg=[negative(x),0]
    neg=select(condition,choice_neg)
    
    return pos,neg
    
def plotSeparate(phi,x):
    """
    test if all components of the given array are zero
    """
    x_pos,x_neg=separateSign(x)
    if not(isZero(x_pos)):    
        plt.plot(phi,x_pos,'b')
    if not(isZero(x_neg)):    
        plt.plot(phi,x_neg,'r')
    return
        
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
functions to plot spherical harmonics
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def plotHarmonics(step=1000,theta=0):
    """
    plot a polar representation of the 3D spherical harmonics up to 3rd order
    
    Parameters:
        step: number of points to calculate (default:1000)
        theta: elevation angle of the plane (default:0 rads - horizontal plane )
    """
    #plot parameters
    phi=arange(0,2*pi,2*pi/step)
    theta=ones(step)*theta
    
    #encoding values
    W=              nullOrder(theta,phi)
    X,Y,Z=          firstOrder(theta,phi)
    V,T,R,S,U=      secondOrder(theta,phi)
    Q,O,M,K,L,N,P=  thirdOrder(theta,phi)

    #plot
    # order 0
    plt.subplot(474,polar=True)        
    plotSeparate(phi,W)
    # order 1
    plt.subplot(4,7,10,polar=True)
    plotSeparate(phi,Y)
    plt.subplot(4,7,11,polar=True)
    plotSeparate(phi,Z)
    plt.subplot(4,7,12,polar=True)
    plotSeparate(phi,X)
    #order 2
    plt.subplot(4,7,16,polar=True)
    plotSeparate(phi,V)
    plt.subplot(4,7,17,polar=True)
    plotSeparate(phi,T)
    plt.subplot(4,7,18,polar=True)
    plotSeparate(phi,R)
    plt.subplot(4,7,19,polar=True)
    plotSeparate(phi,S)
    plt.subplot(4,7,20,polar=True)
    plotSeparate(phi,U)
    #order 3
    plt.subplot(4,7,22,polar=True)
    plotSeparate(phi,Q)
    plt.xlabel('m=-3')
    plt.subplot(4,7,23,polar=True)
    plotSeparate(phi,O) 
    plt.xlabel('m=-2')
    plt.subplot(4,7,24,polar=True)
    plotSeparate(phi,M)
    plt.xlabel('m=-1')
    plt.subplot(4,7,25,polar=True)
    plotSeparate(phi,K)
    plt.xlabel('m=0')
    plt.subplot(4,7,26,polar=True)
    plotSeparate(phi,L)
    plt.xlabel('m=1')
    plt.subplot(4,7,27,polar=True)
    plotSeparate(phi,N)
    plt.xlabel('m=2')
    plt.subplot(4,7,28,polar=True)
    plotSeparate(phi,P)
    plt.xlabel('m=3')
    
    return

    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
def plotPointSource(step=1000,theta=0,theta_s=0,phi_s=0):
    """
    plot a polar representation of a puntual source encoded with 3D spherical harmonics up to 3rd order
    
    Parameters:
        step: number of points to calculate (default:1000)
        theta: elevation angle of the plane (default:0 rads - horizontal plane)
        theta_s: source's elevation angle 
        phi_s: source's azimuth angle
    """
    #plot parameters
    phi=arange(0,2*pi,2*pi/step)
    theta=ones(step)*theta
    
    #encoding values
    W=              nullOrder(theta,phi)
    X,Y,Z=          firstOrder(theta,phi)
    V,T,R,S,U=      secondOrder(theta,phi)
    Q,O,M,K,L,N,P=  thirdOrder(theta,phi)
    
    #source coefficients
    W_s=                            nullOrder(theta_s,phi_s)
    X_s,Y_s,Z_s=                    firstOrder(theta_s,phi_s)
    V_s,T_s,R_s,S_s,U_s=            secondOrder(theta_s,phi_s)
    Q_s,O_s,M_s,K_s,L_s,N_s,P_s=    thirdOrder(theta_s,phi_s)

    #plot
    # order 0
    plt.subplot(474,polar=True)        
    plotSeparate(phi,W*W_s)
    # order 1
    plt.subplot(4,7,10,polar=True)
    plotSeparate(phi,Y*Y_s)
    plt.subplot(4,7,11,polar=True)
    plotSeparate(phi,Z*Z_s)
    plt.subplot(4,7,12,polar=True)
    plotSeparate(phi,X*X_s)
    #order 2
    plt.subplot(4,7,16,polar=True)
    plotSeparate(phi,V*V_s)
    plt.subplot(4,7,17,polar=True)
    plotSeparate(phi,T*T_s)
    plt.subplot(4,7,18,polar=True)
    plotSeparate(phi,R*R_s)
    plt.subplot(4,7,19,polar=True)
    plotSeparate(phi,S*S_s)
    plt.subplot(4,7,20,polar=True)
    plotSeparate(phi,U*U_s)
    #order 3
    plt.subplot(4,7,22,polar=True)
    plotSeparate(phi,Q*Q_s)
    plt.xlabel('m=-3')
    plt.subplot(4,7,23,polar=True)
    plotSeparate(phi,O*O_s) 
    plt.xlabel('m=-2')
    plt.subplot(4,7,24,polar=True)
    plotSeparate(phi,M*M_s)
    plt.xlabel('m=-1')
    plt.subplot(4,7,25,polar=True)
    plotSeparate(phi,K*K_s)
    plt.xlabel('m=0')
    plt.subplot(4,7,26,polar=True)
    plotSeparate(phi,L*L_s)
    plt.xlabel('m=1')
    plt.subplot(4,7,27,polar=True)
    plotSeparate(phi,N*N_s)
    plt.xlabel('m=2')
    plt.subplot(4,7,28,polar=True)
    plotSeparate(phi,P*P_s)
    plt.xlabel('m=3')
    
    return


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def plotPointSourceMoving(step=100,theta=0,theta_s=0):
    """
    plot a polar representation of a circle-moving puntual source encoded with 3D spherical harmonics up to 3rd order
    
    Parameters:
        step: number of points to calculate (default:1000)
        theta: elevation angle of the plane (default:0 rads - horizontal plane)
        theta_s: source's elevation angle 
    """
    
    #adapted from http://matplotlib.org/1.3.1/examples/animation/simple_anim.html
    
    #plot parameters
    phi=arange(0,2*pi,2*pi/step)
    theta=ones(step)*theta
    global phi_s #initial value
    phi_s=0
    
    y_lim=5 #max amplitude value
    
    #encoding values
    W=              nullOrder(theta,phi)
    X,Y,Z=          firstOrder(theta,phi)
    V,T,R,S,U=      secondOrder(theta,phi)
    Q,O,M,K,L,N,P=  thirdOrder(theta,phi)
    
    #source coefficients
    W_s=                            nullOrder(theta_s,phi_s)
    X_s,Y_s,Z_s=                    firstOrder(theta_s,phi_s)
    V_s,T_s,R_s,S_s,U_s=            secondOrder(theta_s,phi_s)
    Q_s,O_s,M_s,K_s,L_s,N_s,P_s=    thirdOrder(theta_s,phi_s)

    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure(figsize=(20,10))
    
    ax4=fig.add_subplot(474,polar=True)
    ax4.set_ylim(0,y_lim)
    line4a, = ax4.plot([], [], color='b')
    line4b, = ax4.plot([], [],color='r')
    line4c, = ax4.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')
    
    ax10=fig.add_subplot(4,7,10,polar=True)
    ax10.set_ylim(0,y_lim)
    line10a, = ax10.plot([], [], color='b')
    line10b, = ax10.plot([], [],color='r')
    line10c, = ax10.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')    
    
    ax11=fig.add_subplot(4,7,11,polar=True)
    ax11.set_ylim(0,y_lim)
    line11a, = ax11.plot([], [], color='b')
    line11b, = ax11.plot([], [],color='r')
    line11c, = ax11.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    
    ax12=fig.add_subplot(4,7,12,polar=True)
    ax12.set_ylim(0,y_lim)
    line12a, = ax12.plot([], [], color='b')
    line12b, = ax12.plot([], [],color='r')
    line12c, = ax12.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    
    ax16=fig.add_subplot(4,7,16,polar=True)
    ax16.set_ylim(0,y_lim)
    line16a, = ax16.plot([], [], color='b')
    line16b, = ax16.plot([], [],color='r')
    line16c, = ax16.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   

    ax17=fig.add_subplot(4,7,17,polar=True)
    ax17.set_ylim(0,y_lim)
    line17a, = ax17.plot([], [], color='b')
    line17b, = ax17.plot([], [],color='r')
    line17c, = ax17.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    
    ax18=fig.add_subplot(4,7,18,polar=True)
    ax18.set_ylim(0,y_lim)
    line18a, = ax18.plot([], [], color='b')
    line18b, = ax18.plot([], [],color='r')
    line18c, = ax18.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   

    ax19=fig.add_subplot(4,7,19,polar=True)
    ax19.set_ylim(0,y_lim)
    line19a, = ax19.plot([], [], color='b')
    line19b, = ax19.plot([], [],color='r')
    line19c, = ax19.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   

    ax20=fig.add_subplot(4,7,20,polar=True)
    ax20.set_ylim(0,y_lim)
    line20a, = ax20.plot([], [], color='b')
    line20b, = ax20.plot([], [],color='r')
    line20c, = ax20.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   

    ax22=fig.add_subplot(4,7,22,polar=True)
    ax22.set_ylim(0,y_lim)
    line22a, = ax22.plot([], [], color='b')
    line22b, = ax22.plot([], [],color='r')
    line22c, = ax22.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    plt.xlabel('m=-3')

    ax23=fig.add_subplot(4,7,23,polar=True)
    ax23.set_ylim(0,y_lim)
    line23a, = ax23.plot([], [], color='b')
    line23b, = ax23.plot([], [],color='r')
    line23c, = ax23.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    plt.xlabel('m=-2')

    ax24=fig.add_subplot(4,7,24,polar=True)
    ax24.set_ylim(0,y_lim)
    line24a, = ax24.plot([], [], color='b')
    line24b, = ax24.plot([], [],color='r')
    line24c, = ax24.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    plt.xlabel('m=-1')

    ax25=fig.add_subplot(4,7,25,polar=True)
    ax25.set_ylim(0,y_lim)
    line25a, = ax25.plot([], [], color='b')
    line25b, = ax25.plot([], [],color='r')
    line25c, = ax25.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    plt.xlabel('m=0')

    ax26=fig.add_subplot(4,7,26,polar=True)
    ax26.set_ylim(0,y_lim)
    line26a, = ax26.plot([], [], color='b')
    line26b, = ax26.plot([], [],color='r')
    line26c, = ax26.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    plt.xlabel('m=1')

    ax27=fig.add_subplot(4,7,27,polar=True)
    ax27.set_ylim(0,y_lim)
    line27a, = ax27.plot([], [], color='b')
    line27b, = ax27.plot([], [],color='r')
    line27c, = ax27.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    plt.xlabel('m=2')
    
    ax28=fig.add_subplot(4,7,28,polar=True)
    ax28.set_ylim(0,y_lim)
    line28a, = ax28.plot([], [], color='b')
    line28b, = ax28.plot([], [],color='r')
    line28c, = ax28.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
    plt.xlabel('m=3')


    # initialization function: plot the background of each frame
    def init():
        #initialize empty lines        
        line4a.set_data([], [])
        line4b.set_data([], [])
        line4c.set_data([], [])
        line10a.set_data([], [])
        line10b.set_data([], [])
        line10c.set_data([], [])
        line11a.set_data([], [])
        line11b.set_data([], [])
        line11c.set_data([], [])
        line12a.set_data([], [])
        line12b.set_data([], [])
        line12c.set_data([], [])
        line16a.set_data([], [])
        line16b.set_data([], [])
        line16c.set_data([], [])
        line17a.set_data([], [])
        line17b.set_data([], [])
        line17c.set_data([], [])
        line18a.set_data([], [])
        line18b.set_data([], [])
        line18c.set_data([], [])
        line19a.set_data([], [])
        line19b.set_data([], [])
        line19c.set_data([], [])
        line20a.set_data([], [])
        line20b.set_data([], [])
        line20c.set_data([], [])
        line22a.set_data([], [])
        line22b.set_data([], [])
        line22c.set_data([], [])
        line23a.set_data([], [])
        line23b.set_data([], [])
        line23c.set_data([], [])
        line24a.set_data([], [])
        line24b.set_data([], [])
        line24c.set_data([], [])
        line25a.set_data([], [])
        line25b.set_data([], [])
        line25c.set_data([], [])
        line26a.set_data([], [])
        line26b.set_data([], [])
        line26c.set_data([], [])
        line27a.set_data([], [])
        line27b.set_data([], [])
        line27c.set_data([], [])
        line28a.set_data([], [])
        line28b.set_data([], [])
        line28c.set_data([], [])
    
    # animation function.  This is called sequentially
    def animate(i):
        global phi_s
        phi_s =2*pi*i/250 
        source_position=4

        X_s,Y_s,Z_s=                    firstOrder(theta_s,phi_s)
        V_s,T_s,R_s,S_s,U_s=            secondOrder(theta_s,phi_s)
        Q_s,O_s,M_s,K_s,L_s,N_s,P_s=    thirdOrder(theta_s,phi_s)
    
        w_pos,w_neg=separateSign(W*W_s)
        line4a.set_data(phi, w_pos)
        line4b.set_data(phi, w_neg)
        line4c.set_data([phi_s],[source_position]) 

        y_pos,y_neg=separateSign(Y*Y_s)
        line10a.set_data(phi, y_pos)
        line10b.set_data(phi, y_neg)
        line10c.set_data([phi_s],[source_position]) 
        z_pos,z_neg=separateSign(Z*Z_s)
        line11a.set_data(phi, z_pos)
        line11b.set_data(phi, z_neg)
        line11c.set_data([phi_s],[source_position]) 
        x_pos,x_neg=separateSign(X*X_s)
        line12a.set_data(phi, x_pos)
        line12b.set_data(phi, x_neg)
        line12c.set_data([phi_s],[source_position]) 
        
        v_pos,v_neg=separateSign(V*V_s)
        line16a.set_data(phi, v_pos)
        line16b.set_data(phi, v_neg)
        line16c.set_data([phi_s],[source_position]) 
        t_pos,t_neg=separateSign(T*T_s)
        line17a.set_data(phi, t_pos)
        line17b.set_data(phi, t_neg)
        line17c.set_data([phi_s],[source_position]) 
        r_pos,r_neg=separateSign(R*R_s)
        line18a.set_data(phi, r_pos)
        line18b.set_data(phi, r_neg)
        line18c.set_data([phi_s],[source_position]) 
        s_pos,s_neg=separateSign(S*S_s)
        line19a.set_data(phi, s_pos)
        line19b.set_data(phi, s_neg)
        line19c.set_data([phi_s],[source_position]) 
        u_pos,u_neg=separateSign(U*U_s)
        line20a.set_data(phi, u_pos)
        line20b.set_data(phi, u_neg)
        line20c.set_data([phi_s],[source_position]) 
        
        q_pos,q_neg=separateSign(Q*Q_s)
        line22a.set_data(phi, q_pos)
        line22b.set_data(phi, q_neg)
        line22c.set_data([phi_s],[source_position]) 
        o_pos,o_neg=separateSign(O*O_s)
        line23a.set_data(phi, o_pos)
        line23b.set_data(phi, o_neg)
        line23c.set_data([phi_s],[source_position]) 
        m_pos,m_neg=separateSign(M*M_s)
        line24a.set_data(phi, m_pos)
        line24b.set_data(phi, m_neg)
        line24c.set_data([phi_s],[source_position]) 
        k_pos,k_neg=separateSign(K*K_s)
        line25a.set_data(phi, k_pos)
        line25b.set_data(phi, k_neg)
        line25c.set_data([phi_s],[source_position]) 
        l_pos,l_neg=separateSign(L*L_s)
        line26a.set_data(phi, l_pos)
        line26b.set_data(phi, l_neg)
        line26c.set_data([phi_s],[source_position]) 
        n_pos,n_neg=separateSign(N*N_s)
        line27a.set_data(phi, n_pos)
        line27b.set_data(phi, n_neg)
        line27c.set_data([phi_s],[source_position]) 
        p_pos,p_neg=separateSign(P*P_s)
        line28a.set_data(phi, p_pos)
        line28b.set_data(phi, p_neg)
        line28c.set_data([phi_s],[source_position]) 
        
        return line4a,line4b,line4c, line10a,line10b,line10c, line11a,line11b,line11c, line12a,line12b,line12c, line16a,line16b,line16c, line17a,line17b,line17c, line18a,line18b,line18c, line19a,line19b,line19c, line20a,line20b,line20c, line22a,line22b,line22c, line23a,line23b,line23c, line24a,line24b,line24c, line25a,line25b,line25c, line26a,line26b,line26c, line27a,line27b,line27c, line28a,line28b,line28c,
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    # interval= time between calculations in ms
    # frames=  each frames iterations, start again
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=200, interval=20, blit=True)

    
    return anim #in order to work from ipython
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def plotPointSourceMovingFirst(step=1000,theta=0):
    """
    plot a polar representation in the horizontal plane of a circle-moving puntual source,
    encoded with only first order 3D spherical harmonics
    - narrow line: individual components
    - broad line: addition of all components 

    Parameters:
        step: number of points to calculate (default:1000)
        theta: elevation angle of the plane (default:0 rads - horizontal plane)
    """
    
    #adapted from http://matplotlib.org/1.3.1/examples/animation/simple_anim.html
    
    #plot parameters
    phi=arange(0,2*pi,2*pi/step)
    theta=ones(step)*theta
    phi_s=0
    theta_s=0
    
    #encoding values
    X,Y,Z=          firstOrder(theta,phi)
    
    #source coefficients
    X_s,Y_s,Z_s=   firstOrder(theta_s,phi_s)

    # First set up the figure, the axis, and the plot element we want to animate

    fig = plt.figure(figsize=(20,10))
    ax = plt.axes(polar=True)
    ax.set_ylim(0,5)
    
    lineXa, = ax.plot([], [], color='b')
    lineXb, = ax.plot([], [], color='r')
    lineYa, = ax.plot([], [], color='b')
    lineYb, = ax.plot([], [], color='r') 
    line1a, = ax.plot([], [], color='b',lw=3)
    line1b, = ax.plot([], [],color='r',lw=3)
    
    line_c, = ax.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')
    
  
    # initialization function: plot the background of each frame
    def init():
        #initialize empty lines: line_a positive values, line_b negative values, line_c point source
        lineXa.set_data([], [])
        lineXb.set_data([], [])
        lineYa.set_data([], [])
        lineYb.set_data([], [])
        line1a.set_data([], [])
        line1b.set_data([], [])
        line_c.set_data([], [])

    
    # animation function.  This is called sequentially
    def animate(i):
        global phi_s
        phi_s =2*pi*i/200 
        source_position=4

        X_s,Y_s,Z_s=firstOrder(theta_s,phi_s)
        
        first=(X*X_s)+(Y*Y_s)
    
        x_pos,x_neg=separateSign(X*X_s)
        lineXa.set_data(phi, x_pos)
        lineXb.set_data(phi, x_neg)
        y_pos,y_neg=separateSign(Y*Y_s)
        lineYa.set_data(phi, y_pos)
        lineYb.set_data(phi, y_neg)
        first_pos,first_neg=separateSign(first) 
        line1a.set_data(phi,first_pos)
        line1b.set_data(phi,first_neg)
        
        line_c.set_data([phi_s], [source_position])
    

        return lineXa,lineXb, lineYa,lineYb, line1a,line1b,line_c
        
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    # interval= time between calculations in ms
    # frames=  each frames iterations, start again
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=200, interval=20, blit=True)

    
    return anim
    
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def plotPointSourceMovingSecond(step=1000,theta=0):
    """
    plot a polar representation in the horizontal plane of a circle-moving puntual source,
    encoded with only second order 3D spherical harmonics
    - narrow line: individual components
    - broad line: addition of all components 

    Parameters:
        step: number of points to calculate (default:1000)
        theta: elevation angle of the plane (default:0 rads - horizontal plane)
    """
    
    #adapted from http://matplotlib.org/1.3.1/examples/animation/simple_anim.html
    
    #plot parameters
    phi=arange(0,2*pi,2*pi/step)
    theta=ones(step)*theta
    phi_s=0
    theta_s=0
    
    #encoding values
    V,T,R,S,U=      secondOrder(theta,phi)
    
    #source coefficients
    V_s,T_s,R_s,S_s,U_s = secondOrder(theta_s,phi_s)

    # First set up the figure, the axis, and the plot element we want to animate

    fig = plt.figure(figsize=(20,10))
    ax = plt.axes(polar=True)
    ax.set_ylim(0,7)
    
    lineVa, = ax.plot([], [], color='b')
    lineVb, = ax.plot([], [], color='r')
    lineRa, = ax.plot([], [], color='b')
    lineRb, = ax.plot([], [], color='r') 
    lineUa, = ax.plot([], [], color='b')
    lineUb, = ax.plot([], [], color='r') 
    line2a, = ax.plot([], [], color='b',lw=3)
    line2b, = ax.plot([], [], color='r',lw=3)
    
    line_c, = ax.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')
    
  
    # initialization function: plot the background of each frame
    def init():
        #initialize empty lines: line_a positive values, line_b negative values, line_c point source
        lineVa.set_data([], [])
        lineVb.set_data([], [])
        lineRa.set_data([], [])
        lineRb.set_data([], [])
        lineUa.set_data([], [])
        lineUb.set_data([], [])
        line2a.set_data([], [])
        line2b.set_data([], [])
        line_c.set_data([], [])

    
    # animation function.  This is called sequentially
    def animate(i):
        global phi_s
        phi_s =2*pi*i/200 
        source_position=6

        V_s,T_s,R_s,S_s,U_s = secondOrder(theta_s,phi_s)
        
        # we take only non-zero coefficients
        second=(V*V_s)+(R*R_s)+(U*U_s)
    
        v_pos,v_neg=separateSign(V*V_s)
        lineVa.set_data(phi, v_pos)
        lineVb.set_data(phi, v_neg)
        r_pos,r_neg=separateSign(R*R_s)
        lineRa.set_data(phi, r_pos)
        lineRb.set_data(phi, r_neg)
        u_pos,u_neg=separateSign(U*U_s)
        lineUa.set_data(phi, u_pos)
        lineUb.set_data(phi, u_neg)        
        second_pos,second_neg=separateSign(second) 
        line2a.set_data(phi,second_pos)
        line2b.set_data(phi,second_neg)
        
        line_c.set_data([phi_s], [source_position])
    

        return lineVa,lineVb, lineRa,lineRb, lineUa,lineUb, line2a,line2b,line_c
        
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    # interval= time between calculations in ms
    # frames=  each frames iterations, start again
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=200, interval=20, blit=True)

    
    return anim
    
    
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def plotPointSourceMovingThird(step=1000,theta=0):
    """
    plot a polar representation in the horizontal plane of a circle-moving puntual source,
    encoded with only third order 3D spherical harmonics
    - narrow line: individual components
    - broad line: addition of all components 

    Parameters:
        step: number of points to calculate (default:1000)
        theta: elevation angle of the plane (default:0 rads - horizontal plane)
    """
    
    #adapted from http://matplotlib.org/1.3.1/examples/animation/simple_anim.html
    
    #plot parameters
    phi=arange(0,2*pi,2*pi/step)
    theta=ones(step)*theta
    phi_s=0 
    theta_s=0
    
    #encoding values
    Q,O,M,K,L,N,P=  thirdOrder(theta,phi)
    
    #source coefficients
    Q_s,O_s,M_s,K_s,L_s,N_s,P_s = thirdOrder(theta_s,phi_s)

    # First set up the figure, the axis, and the plot element we want to animate

    fig = plt.figure(figsize=(20,10))
    ax = plt.axes(polar=True)
    ax.set_ylim(0,9)
    
    lineQa, = ax.plot([], [], color='b')
    lineQb, = ax.plot([], [], color='r')
    lineMa, = ax.plot([], [], color='b')
    lineMb, = ax.plot([], [], color='r') 
    lineLa, = ax.plot([], [], color='b')
    lineLb, = ax.plot([], [], color='r') 
    linePa, = ax.plot([], [], color='b')
    linePb, = ax.plot([], [], color='r') 
    line3a, = ax.plot([], [], color='b',lw=3)
    line3b, = ax.plot([], [], color='r',lw=3)
    
    line_c, = ax.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')
    
  
    # initialization function: plot the background of each frame
    def init():
        #initialize empty lines: line_a positive values, line_b negative values, line_c point source
        lineQa.set_data([], [])
        lineQb.set_data([], [])
        lineMa.set_data([], [])
        lineMb.set_data([], [])
        lineLa.set_data([], [])
        lineLb.set_data([], [])
        linePa.set_data([], [])
        linePb.set_data([], [])
        line3a.set_data([], [])
        line3b.set_data([], [])
        line_c.set_data([], [])

    
    # animation function.  This is called sequentially
    def animate(i):
        global phi_s
        phi_s =2*pi*i/200 
        source_position=8

        Q_s,O_s,M_s,K_s,L_s,N_s,P_s = thirdOrder(theta_s,phi_s)
        # we take only non-zero coefficients
        third=(Q*Q_s)+(M*M_s)+(L*L_s)+(P*P_s)
    
        q_pos,q_neg=separateSign(Q*Q_s)
        lineQa.set_data(phi, q_pos)
        lineQb.set_data(phi, q_neg)
        m_pos,m_neg=separateSign(M*M_s)
        lineMa.set_data(phi, m_pos)
        lineMb.set_data(phi, m_neg)
        l_pos,l_neg=separateSign(L*L_s)
        lineLa.set_data(phi, l_pos)
        lineLb.set_data(phi, l_neg) 
        p_pos,p_neg=separateSign(P*P_s)
        linePa.set_data(phi, p_pos)
        linePb.set_data(phi, p_neg)
        third_pos,third_neg=separateSign(third) #already normalized
        line3a.set_data(phi,third_pos)
        line3b.set_data(phi,third_neg)
        
        line_c.set_data([phi_s], [source_position])
    

        return lineQa,lineQb, lineMa,lineMb, lineLa,lineLb, linePa,linePb, line3a,line3b,line_c
        
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    # interval= time between calculations in ms
    # frames=  each frames iterations, start again
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=200, interval=20, blit=True)

    
    return anim    


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def plotPointSourceMovingDirectivity(step=1000,theta=0):
    """
    plot a polar representation in the horizontal plane of a circle-moving puntual source,
    encoded with up to third order 3D spherical harmonics
    
    each plot is normalized by the number of channels

    Parameters:
        step: number of points to calculate (default:1000)
        theta: elevation angle of the plane (default:0 rads - horizontal plane)
    """
    
    #adapted from http://matplotlib.org/1.3.1/examples/animation/simple_anim.html
    
    #plot parameters
    phi=arange(0,2*pi,2*pi/step)
    theta=ones(step)*theta
    phi_s=0
    theta_s=0
    
    #encoding values
    W=              nullOrder(theta,phi)
    X,Y,Z=          firstOrder(theta,phi)
    V,T,R,S,U=      secondOrder(theta,phi)
    Q,O,M,K,L,N,P=  thirdOrder(theta,phi)
    
    #source coefficients
    W_s=                            nullOrder(theta_s,phi_s)
    X_s,Y_s,Z_s=                    firstOrder(theta_s,phi_s)
    V_s,T_s,R_s,S_s,U_s=            secondOrder(theta_s,phi_s)
    Q_s,O_s,M_s,K_s,L_s,N_s,P_s=    thirdOrder(theta_s,phi_s)

    # First set up the figure, the axis, and the plot element we want to animate

    fig = plt.figure(figsize=(20,10))
    
    ax1= fig.add_subplot(221,polar=True)
    ax1.set_ylim(0,1.2)
    ax1.set_xlabel('m=0')
    line1a, = ax1.plot([], [], color='b')
    line1b, = ax1.plot([], [],color='r')
    line1c, = ax1.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')
    
    
    ax2=fig.add_subplot(222,polar=True)
    ax2.set_ylim(0,1.2)
    ax2.set_xlabel('m=1')
    line2a, = ax2.plot([], [], color='b')
    line2b, = ax2.plot([], [],color='r')
    line2c, = ax2.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')
    
    ax3=fig.add_subplot(223,polar=True)
    ax3.set_ylim(0,1.2)
    ax3.set_xlabel('m=2')
    line3a, = ax3.plot([], [], color='b')
    line3b, = ax3.plot([], [],color='r')
    line3c, = ax3.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')    
    
    ax4=fig.add_subplot(224,polar=True)
    ax4.set_ylim(0,1.2)
    ax4.set_xlabel('m=3')
    line4a, = ax4.plot([], [], color='b')
    line4b, = ax4.plot([], [],color='r')
    line4c, = ax4.plot([], [],color='g',lw=5,linestyle='steps--',marker='o')   
     
    

    # initialization function: plot the background of each frame
    def init():
        #initialize empty lines: line_a positive values, line_b negative values, line_c point source
        line1a.set_data([], [])
        line1b.set_data([], [])
        line1c.set_data([], [])
        
        line2a.set_data([], [])
        line2b.set_data([], [])
        line2c.set_data([], [])

        line3a.set_data([], [])
        line3b.set_data([], [])
        line3c.set_data([], [])
        
        line4a.set_data([], [])
        line4b.set_data([], [])
        line4c.set_data([], [])

    
    # animation function.  This is called sequentially
    def animate(i):
        global phi_s
        phi_s =2*pi*i/200 
        source_position=1

        X_s,Y_s,Z_s=                    firstOrder(theta_s,phi_s)
        V_s,T_s,R_s,S_s,U_s=            secondOrder(theta_s,phi_s)
        Q_s,O_s,M_s,K_s,L_s,N_s,P_s=    thirdOrder(theta_s,phi_s)
        
        zero=(W*W_s)
        first=(zero+(X*X_s)+(Y*Y_s)+(Z*Z_s))
        second=(first+(V*V_s)+(T*T_s)+(R*R_s)+(S*S_s)+(U*U_s))
        third=(second+(Q*Q_s)+(O*O_s)+(M*M_s)+(K*K_s)+(L*L_s)+(N*N_s)+(P*P_s))

        # normalize each decoding by the number of channels
        first_pos,first_neg=separateSign(zero/1)
        line1a.set_data(phi, first_pos)
        line1b.set_data(phi, first_neg)
        line1c.set_data([phi_s], [source_position])
        
        second_pos,second_neg=separateSign(first/4)
        line2a.set_data(phi, second_pos)
        line2b.set_data(phi, second_neg)
        line2c.set_data([phi_s], [source_position])

        third_pos,third_neg=separateSign(second/9)
        line3a.set_data(phi, third_pos)
        line3b.set_data(phi, third_neg)
        line3c.set_data([phi_s], [source_position])
        
        all_pos,all_neg=separateSign(third/16)
        line4a.set_data(phi, all_pos)
        line4b.set_data(phi, all_neg)
        line4c.set_data([phi_s],[source_position]) 


        return line1a,line1b,line1c, line2a,line2b,line2c, line3a,line3b,line3c, line4a,line4b,line4c
        
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    # interval= time between calculations in ms
    # frames=  each frames iterations, start again
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=200, interval=20, blit=True)

    
    return anim
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def plotPointSourceDirectivity(step=1000):
    """
    linear plot of directivity from a point source at (phi=0, theta=0) over different ambisonics levels
    
    each plot is normalized by the number of channels
    
    Parameters:
        step: number of points to calculate (default:1000)
    """
        
    #plot parameters
    phi=arange(-pi,pi,2*pi/step)
    theta=zeros(step)
    phi_s=0
    theta_s=0
    
    #encoding values
    W=              nullOrder(theta,phi)
    X,Y,Z=          firstOrder(theta,phi)
    V,T,R,S,U=      secondOrder(theta,phi)
    Q,O,M,K,L,N,P=  thirdOrder(theta,phi)
    
    #source coefficients
    W_s =                            nullOrder(theta_s,phi_s)
    X_s,Y_s,Z_s =                    firstOrder(theta_s,phi_s)
    V_s,T_s,R_s,S_s,U_s =            secondOrder(theta_s,phi_s)
    Q_s,O_s,M_s,K_s,L_s,N_s,P_s =    thirdOrder(theta_s,phi_s)
    
    #coefficient times encoding functions
    zero =       (W*W_s)
    first =      zero+(X*X_s)+(Y*Y_s)+(Z*Z_s)
    second =     first+(V*V_s)+(T*T_s)+(R*R_s)+(S*S_s)+(U*U_s)
    third =      second+(Q*Q_s)+(O*O_s)+(M*M_s)+(K*K_s)+(L*L_s)+(N*N_s)+(P*P_s)

    # normalize each decoding by the number of channels
    plt.figure()
    plt.xlabel('azimuth (rad)')
    plt.ylabel('level')
    plt.xlim(-pi,pi)
    plt.title('Directivity of a point source encoding with different Ambisonic levels')
    plt.grid()
    p0,=plt.plot(phi,zero/1)
    p1,=plt.plot(phi,first/4)
    p2,=plt.plot(phi,second/9)
    p3,=plt.plot(phi,third/16)
    plt.legend([p0,p1,p2,p3],['m=0','m=1','m=2','m=3'])
    

    return   