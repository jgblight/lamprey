import nef
import random
import os
import os.path
from math import sin,cos,pi,exp
import subprocess
import pickle
import time
import nef.templates.gate as gating
import nef.templates.learned_termination as learning

tau = 0.02
damp0 = -0.1
damp = -1
freq = 60

net = nef.Network('Neural Lamprey')

subprocess.call(["python","/Users/jgblight/Documents/Neuro/lamprey/pinv.py"])
time.sleep(100)
output = open('/Users/jgblight/Documents/Neuro/lamprey/data.pkl', 'r')
m_d = pickle.load(output)
m_i = pickle.load(output)
gamma = pickle.load(output)
gamma_inv = pickle.load(output)
output.close()

def phi(z,m):
	return exp(-1*((z-(1/10.0)*m)**2)/0.25)

encoders = []
for i in range(10):
	for j in range(20):
		en = [0,0,0,0,0,0,0,0,0,0]
		en[i] = 1
		encoders.append(en)
	for j in range(20):
		en = [0,0,0,0,0,0,0,0,0,0]
		en[i] = -1
		encoders.append(en)

def print_weights(w):
    print w
    return w

def m_d_(x):
	dx = []
	for i in range(10):
		dx0 = 0
		for j in range(10):
			dx0 += (m_d[i][j])*x[j]
		dx.append(dx0*tau + x[i])
	return dx

def m_i_(x):
	o = []
	for i in range(10):
		dx0 = 0
		for j in range(10):
			dx0 += m_i[i][j]*x[j]
		o.append(dx0*tau)
	return o

net.make('a', neurons=400, dimensions=10,radius=3,encoders=encoders,noise=0.1)
net.connect('a','a',func=m_d_,weight_func=print_weights,pstc=tau)

def T(x):
    t = []
    for z in range(10):
        y = 0
        for m in range(10):
            y += x[m]*phi(z*0.1,m)
        t.append(y)
    return t

net.make('T',1,10,mode='direct')
net.connect('a','T',func=T)

net.add_to_nengo()

