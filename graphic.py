# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 02:14:37 2023

@author: Alexandre
"""
import numpy as np
from matplotlib import pyplot as plt

def polar_to_cartesian(r,theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x,y

def show_graph(node, number):
    n = number
    theta = [((2*np.pi)/n) * i for i in range(n)]
    r = 1
    x = []
    y = []
    for i in range(n):
        xi,yi = polar_to_cartesian(r, theta[i])
        x.append(xi)
        y.append(yi)
    x.append(x[0])
    y.append(y[0])
    plt.plot(x,y)
    for i in range(n):
        plt.text(x[i],y[i],str(node.identifiant))
        node = node.v_droite
    return plt