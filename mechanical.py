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


net.make_input('damping',[-0.1])
net.make_input('swim',[60])

net.make('A', neurons=200, dimensions=4)

net.make('M_d',1,5,radius=5,mode='direct')
net.make('M_a',1,5,radius=40,mode='direct')

net.connect('damping','M_d',transform=[[1],[0],[0],[0],[0]],pstc=tau)
net.connect('A','M_d',transform=[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],pstc=tau)

def damping(x):
    dx1 = x[0]*x[1] + x[0]*x[3]
    dx2 = 0
    dx3 = x[0]*x[1] + x[0]*x[3]
    dx4 = damp*x[4]
    return dx1 * tau + x[1], dx2 * tau + x[2], dx3 * tau + x[3], dx4 * tau + x[4]
net.connect('M_d', 'A', func=damping, pstc=tau)

net.connect('swim','M_a',transform=[[1],[0],[0],[0],[0]],pstc=tau)
net.connect('A','M_a',transform=[[0,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],pstc=tau)

def swimming(x):
    dx1 = x[0]*x[2]
    dx2 = -0.5*x[0]*x[1] + 0.5*x[0]*x[3]
    dx3 = -1*x[0]*x[2]
    dx4 = 0
    return dx1 * tau, dx2 * tau, dx3 * tau, dx4 * tau
net.connect('M_a', 'A', func=swimming,pstc=tau
)
net.make('a_actual',200,10,mode='direct')

def Gamma(x):
    dx = []
    for i in range(10):
        dx0 = 0
        for j in range(3):
            dx0 += (gamma_inv[i][j])*x[j]
        dx.append(dx0)
    return dx

net.connect('A','a_actual',func=Gamma,pstc=tau)

def T(x):
    t = []
    for z in range(10):
        y = 0
        for m in range(10):
            y += x[m]*phi(z*0.1,m)
        t.append(y)
    return t

net.make('T',1,10,mode='direct')
net.connect('a_actual','T',func=T)

def torque(x):
    f = []
    for i in range(9):
        f.append(x[i]-x[i+1])
    return f

net.make('F',1,9,mode='direct')
net.connect('T','F',func=torque)

net.make('x',1,9,mode='direct')
net.make('theta',1,9,mode='direct',radius=pi)
net.make('F_theta',1,18,mode='direct')
net.make('F_x',1,9,mode='direct')
net.make('F_z',1,9,mode='direct')

def get_theta(x):
    theta = []
    theta.append(sin((x[1]-x[0])/2.) + (pi/2.))
    for i in range(1,8):
        theta.append(sin((x[i+1]-x[i-1])/4.) + (pi/2.))
    theta.append(sin((x[8]-x[7])/2.) + (pi/2.))
    return theta
net.connect('x','theta',func=get_theta)

t = zeros((18,9)).tolist()
for i in range(9):
    t[i][i] = 1
net.connect('theta','F_theta',transform=t)

t = zeros((18,9)).tolist()
for i in range(9):
    t[i+9][i] = 1
net.connect('F','F_theta',transform=t)

def Fx(x):
    fx = []
    for i in range(9):
        fx.append(sin(x[i])*x[i+9])
    return fx
net.connect('F_theta','F_x',func=Fx)

def Fz(x):
    fz = []
    for i in range(9):
        fz.append(cos(x[i])*x[i+9])
    return fz
net.connect('F_theta','F_z',func=Fz)

t = zeros((9,9)).tolist()
for i in range(9):
    t[i][i] = tau*6
net.connect('x','x',pstc=tau)
net.connect('F','x',transform=t,pstc=tau)

net.add_to_nengo()