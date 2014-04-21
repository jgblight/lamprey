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

net = nef.Network('Neural Lamprey')

output = open('/Users/jgblight/Documents/Neuro/lamprey/data.pkl', 'r')
m_d = pickle.load(output)
m_i = pickle.load(output)
start = pickle.load(output)
output.close()

#for i in range(10):
#	encoders = []
#	for j in range(200):
#		encoders.append([random.choice([-1,1])])
#	net.make('a'+str(i), neurons=200, dimensions=1,encoders=encoders)

#for i in range(10):
#	for j in range(10):
#		if i == j:
#			net.connect('a'+str(i),'a'+str(j),func=lambda x: x[0]*(m_d[j][i])*tau + x[0])
#		else:
#			net.connect('a'+str(i),'a'+str(j),func=lambda x: x[0]*(m_d[j][i])*tau)
#net.make_input('input', [0])
#net.connect('input','a0')

def phi(z,m):
	return exp(-1*(z-0.1*m)**2/0.13**2)

encoders = []
for i in range(400):
	e = [] 
	for j in range(10):
		e.append(random.choice([-1,1]))
	encoders.append(e)

def m_d_(x):
	dx = []
	for i in range(10):
		dx0 = 0
		for j in range(10):
			dx0 += m_d[i][j]*x[j]
		dx.append(dx0*tau + x[i])
	return dx

def m_i_(x):
	if x[0] > 0.8:
		o = []
		for i in range(10):
			dx0 = 0
			for j in range(10):
				dx0 += m_i[i][j]*start[j]
			o.append(dx0*tau)

	else:
		o = [0,0,0,0,0,0,0,0,0,0]
	return o

net.make('a', neurons=400, dimensions=10,encoders=encoders)
net.connect('a','a',func=m_d_)

net.make_input('input', [0])
net.make('switch',1,1,mode='direct')
net.connect('input','switch')
net.connect('switch','a',func=m_i_)

def T(x):
	y = 0
	for m in range(10):
		y += x[0]*phi(0.5,m)
	return y

net.make('T1',1,1,mode='direct')
net.connect('a','T1',func=T)


net.add_to_nengo()

