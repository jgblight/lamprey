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
freq = 30

net = nef.Network('Neural Lamprey')

subprocess.call(["python","/Users/jgblight/Documents/Neuro/lamprey/pinv.py"])
time.sleep(100)
output = open('/Users/jgblight/Documents/Neuro/lamprey/data.pkl', 'r')
m_d = pickle.load(output)
m_i = pickle.load(output)
gamma = pickle.load(output)
gamma_inv = pickle.load(output)
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

net.make('a', neurons=400, dimensions=10,radius=1,encoders=encoders)
net.make('a_', neurons=400, dimensions=10,radius=1,encoders=encoders)

#net.connect('a','a_',pstc=tau)
#net.connect('a_','a',func=m_d_,pstc=tau)

M_d = [[damp0,freq,damp0],[-0.5*freq,0,0.5*freq],[damp0,-1*freq,damp0]]

net.make_input('damping',[-0.1])
net.make_input('swim',[30])

net.make('A', neurons=200, dimensions=4)

net.make('M_d',1,5,radius=5,mode='direct')
net.make('M_a',1,5,radius=40,mode='direct')

net.connect('damping','M_d',transform=[[1],[0],[0],[0],[0]])
net.connect('A','M_d',transform=[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

def damping(x):
    dx1 = x[0]*x[1] + x[0]*x[3]
    dx2 = 0
    dx3 = x[0]*x[1] + x[0]*x[3]
    dx4 = damp*x[4]
    return dx1 * tau + x[1], dx2 * tau + x[2], dx3 * tau + x[3], dx4 * tau + x[4]
net.connect('M_d', 'A', func=damping)

net.connect('swim','M_a',transform=[[1],[0],[0],[0],[0]])
net.connect('A','M_a',transform=[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

def swimming(x):
    dx1 = x[0]*x[2]
    dx2 = -0.5*x[0]*x[1] + 0.5*x[0]*x[3]
    dx3 = -1*x[0]*x[2]
    dx4 = 0
    return dx1 * tau, dx2 * tau, dx3 * tau, dx4 * tau
net.connect('M_a', 'A', func=swimming)
net.make('a_actual',200,10)

#def M_d_(x):
#	dx = []
#	for i in range(3):
#		dx0 = 0
#		for j in range(3):
#			dx0 += (M_d[i][j])*x[j]
#		dx.append(dx0*tau + x[i])
#	return dx

#net.connect('A','A',func=M_d_,pstc=tau)

def Gamma(x):
	dx = []
	for i in range(10):
		dx0 = 0
		for j in range(3):
			dx0 += (gamma_inv[i][j])*x[j]
		dx.append(dx0)
	return dx


net.connect('A','a_actual',func=Gamma,pstc=tau)

#net.make('error',100,10,radius=20)
learning.make(net,errName='error', N_err=100, preName='a', postName='a',rate=5e-4)
net.connect('a_actual','error')
net.connect('a', 'error', weight=-1)

net.make_input('switch',[0])
gating.make(net,name='Gate', gated='error', neurons=40,
    pstc=0.01)
net.connect('switch', 'Gate')

#net.make_input('input', [1])
#net.make('switch',1,10,mode='direct')
#net.connect('a','switch')
#net.connect('switch','a',func=m_i_)

#gating.make(net,name='Gate', gated='switch', neurons=40,
#    pstc=0.01) #Make a gate population with 40 neurons, and a postsynaptic 
               #time constant of 10ms
#net.connect('input', 'Gate')


def T(x,z):
	y = 0
	for m in range(10):
		y += x[m]*phi(z,m)
	return y

net.make('T1',1,1,mode='direct')
net.connect('a','T1',func=lambda x: T(x,0.25))

net.make('T2',1,1,mode='direct')
net.connect('a','T2',func=lambda x: T(x,0.5))

net.make('T3',1,1,mode='direct')
net.connect('a','T3',func=lambda x: T(x,0.75))

net.add_to_nengo()

