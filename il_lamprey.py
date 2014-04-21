import nef
import random
import os
import os.path
from math import sin,cos,pi,exp
import subprocess

tau = 0.1
damp0 = -0.1
damp = -1
freq = 30

#silly hack
def pinv(matrix):
	mat_string = ';'.join([ ','.join([str(y) for y in x]) for x in matrix])
	subprocess.call(["python","/Users/jgblight/Documents/Neuro/lamprey/pinv.py",mat_string])
	output = open("/Users/jgblight/Documents/Neuro/lamprey/output").read().strip()
	output = [[ float(x) for x in y.split(',')] for y in output.split(';') ]
	if len(output) == 1:
		output = output[0]
	return output


net = nef.Network('Neural Lamprey')

def phi(z,m):
	return exp(-1*(z-0.1*m)**2/0.7**2)

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
Gamma_inv = pinv(Gamma)
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

for i in range(10):
	encoders = []
	for j in range(200):
		encoders.append([random.choice([-1,1])])
	net.make('a'+str(i), neurons=200, dimensions=1,encoders=encoders)

for i in range(10):
	for j in range(10):
		if i == j:
			net.connect('a'+str(i),'a'+str(j),func=lambda x: x[0]*(m_d[j][i] + m_i[j][i])*tau + x[0])
		else:
			net.connect('a'+str(i),'a'+str(j),func=lambda x: x[0]*(m_d[j][i] + m_i[j][i])*tau)

net.make_input('input', [0])
net.connect('input','a0')
net.add_to_nengo()

