import numpy as np
import random
import os
import os.path
from math import sin,cos,pi,exp
import subprocess

tau = 0.1
damp0 = -0.1
damp = -1
freq = 30

def phi(z,m):
	return exp(-1*(z-0.1*m)**2/0.1**2)

def Phi(z):
	return [1,sin(2*pi*z),cos(2*pi*z),sin(4*pi*z)]

def get_coeffiecient(n,m):
	dx = 1/100000.
	return sum([Phi(z*dx)[n]*phi(z*dx,m)*dx for z in range(0,100001)])

def matmul(x,y):
	m = []
	for i in range(len(x)):
		row = []
		for j in range(len(y[0])):
			element = sum([x[i][k]*y[k][j] for k in range(len(x[i])) ])
			row.append(element)
		m.append(row)
	return m


Gamma = [[get_coeffiecient(n,m) for m in range(10)] for n in range(4)]
print Gamma
Gamma_inv = np.linalg.pinv(Gamma)
print Gamma_inv

M_d = [[damp0,freq,damp0,0],[-0.5*freq,0,0.5*freq,0],[damp0,-1*freq,damp0,0],[0,0,0,damp]]
M_i = [[0.5,0,-0.5,0],[0,1,0,0],[-0.5,0,0.5,0],[0,0,0,0]]

#m_d = sum([Gamma[j][0]*sum([Gamma_inv[i][0]*M_d[i][j] for i in range(4)]) for j in range(4)])
#m_i = sum([Gamma[j][0]*sum([Gamma_inv[i][0]*M_i[i][j] for i in range(4)]) for j in range(4)])

m_d = matmul(matmul(Gamma_inv,M_d),Gamma)
m_i = matmul(matmul(Gamma_inv,M_i),Gamma)

m = []
for i in range(10):
	row = []
	for j in range(10):
		row.append(m_d[i][j] + m_i[i][j])
	m.append(row)

A0 = [-1 * sin(30*t*0.001) for t in range(1000)]
A1 = [-1 * cos(30*t*0.001) for t in range(1000)]
A2 = [sin(30*t*0.001) for t in range(1000)]
A3 = [0 for t in range(1000)]

A = [A0,A1,A2,A3]

a = matmul(Gamma_inv,A)
a = np.array(a)
print a[0,:]


