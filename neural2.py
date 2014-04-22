import nef
import random
import os
import os.path
from math import sin,cos,pi,exp
import subprocess
import pickle
import time
import nef.templates.gate as gating

tau = 0.02
damp0 = -0.1
damp = -1
freq = 30

net = nef.Network('Neural Lamprey')

subprocess.call(["python","/Users/jgblight/Documents/Neuro/lamprey/pinv.py"])
time.sleep(100)
output = open('/Users/jgblight/Documents/Neuro/lamprey/data.pkl', 'r')
m_d = pickle.load(output)
m_i = pickle.load(output)
start = pickle.load(output)
output.close()

def phi(z,m):
	return exp(-1*((z-(1/10.0)*m)**2)/0.25)

def print_weights(w):
    print w
    return w

for i in range(10):
	encoders = []
	for j in range(200):
		encoders.append([random.choice([-1,1])])
	net.make('a'+str(i), neurons=200, dimensions=1,encoders=encoders)

for i in range(10):
	for j in range(10):
		if i == j:
			net.connect('a'+str(i),'a'+str(j),func=lambda x: x[0]*(m_d[j][i])*tau + x[0],pstc=tau)
		else:
			net.connect('a'+str(i),'a'+str(j),func=lambda x: x[0]*(m_d[j][i])*tau,pstc=tau)


#def T(x,z):
#	y = 0
#	for m in range(10):
#		y += x[m]*phi(z,m)
#	return y

#net.make('T1',1,1,mode='direct')
#net.connect('a','T1',func=lambda x: T(x,0.25))

#net.make('T2',1,1,mode='direct')
#net.connect('a','T2',func=lambda x: T(x,0.5))

#net.make('T3',1,1,mode='direct')
#net.connect('a','T3',func=lambda x: T(x,0.75))

net.add_to_nengo()