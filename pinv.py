import numpy as np
import sys
import pickle
from math import sin,cos,pi,exp
damp0 = -0.1
damp = -1
freq = 30

def phi(z,m):
	return exp(-1*(z-0.1*m)**2/0.07**2)

def Phi(z):
	return [1,sin(2*pi*z),cos(2*pi*z),sin(4*pi*z)]

def get_coefficient(n,m):
	dx = 1/100000.
	return sum([Phi(z*dx)[n]*phi(z*dx,m)*dx for z in range(0,100001)])

Gamma = np.zeros([4,10])
for m in range(10):
	for n in range(4):
		Gamma[n,m] = get_coefficient(n,m)

Gamma_inv = np.linalg.pinv(Gamma)



M_d = np.array([[damp0,freq,damp0,0],[-0.5*freq,0,0.5*freq,0],[damp0,-1*freq,damp0,0],[0,0,0,damp]])
M_i = np.array([[0.5,0,-0.5,0],[0,1,0,0],[-0.5,0,0.5,0],[0,0,0,0]])

m_d = np.dot(np.dot(Gamma_inv,M_d),Gamma)
m_i = np.dot(np.dot(Gamma_inv,M_i),Gamma)

A0 = [-1 * sin(30*t*0.001) for t in range(1000)]
A1 = [-1 * cos(30*t*0.001) for t in range(1000)]
A2 = [sin(30*t*0.001) for t in range(1000)]
A3 = [0 for t in range(1000)]

A = np.array([A0,A1,A2,A3])

a = np.dot(Gamma_inv,A)
print m_d

output = open('data.pkl', 'w')
pickle.dump(m_d.tolist(),output)
pickle.dump(m_i.tolist(),output)
pickle.dump(a[:,5].tolist(),output)
output.close()