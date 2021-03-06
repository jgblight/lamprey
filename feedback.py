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

def phi(z,m):
    return exp(-1*((z-(1/10.0)*m)**2)/0.01)

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


net.make('a', neurons=400, dimensions=10,radius=1,encoders=encoders,noise=0.1)

class SineWave(nef.SimpleNode):
    def origin_target(self):
        T = []
        for i in range(10):
            T.append(sin(freq*self.t - 2*pi*i*0.1)-sin(freq*self.t))
        return T

target=net.add(SineWave('target'))

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

net.make('dif',100,10)
net.connect(target.getOrigin('target'),'dif')
net.connect('T','dif',weight=-1)

net.connect('dif','a',weight=4)

net.add_to_nengo()