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
net.make_input('input', [0])
net.make_input('damping',[-0.1])
net.make_input('swim',[30])

encoders = []
for i in range(200):
	encoders.append([random.choice([-1,1])])

def phi(z,m):
	return exp(-(z-0.01*m)**2/0.01**2)

def Phi(z):
	return [1,sin(2*pi*z),cos(2*pi*z),sin(4*pi*z)]

def get_coeffiecient(n,m):
	return sum([Phi(z*0.001)[n]*phi(z*0.001,m)*0.001 for z in range(0,1000)])

Gamma = [[get_coeffiecient(n,50)] for n in range(4)]
print Gamma
Gamma_inv = pinv(Gamma)
print Gamma_inv

M_d = [[damp0,freq,damp0,0],[-0.5*freq,0,0.5*freq,0],[damp0,-1*freq,damp0,0],[0,0,0,damp]]
M_i = [[0.5,0,-0.5,0],[0,1,0,0],[-0.5,0,0.5,0],[0,0,0,0]]

m_d = sum([Gamma[j][0]*sum([Gamma_inv[i]*M_d[i][j] for i in range(4)]) for j in range(4)])
m_i = sum([Gamma[j][0]*sum([Gamma_inv[i]*M_i[i][j] for i in range(4)]) for j in range(4)])

def transform(x):
	dx = m_d*x[0] + m_i*x[0]
	return dx*tau + x[0]

net.make('a', neurons=200, dimensions=1,encoders=encoders)
net.connect('a','a',func=transform)

net.add_to_nengo()

