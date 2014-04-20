import nef
tau = 0.1
damp0 = -0.1
damp = -1
freq = 20
from math import sin, cos, pi

net = nef.Network('High-Level Lamprey')
net.make_input('input', [0])
net.make_input('damping',[-0.1])
net.make_input('swim',[30])

net.make('A', neurons=200, dimensions=4)

net.make('M_d',1,5,radius=5,mode='direct')
net.make('M_a',1,5,radius=40,mode='direct')

net.connect('input', 'A')

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
    dx2 = -1*x[0]*x[1]
    dx3 = -1*x[0]*x[2]
    dx4 = 0
    return dx1 * tau + x[1], dx2 * tau + x[2], dx3 * tau + x[3], dx4 * tau + x[4]
net.connect('M_a', 'A', func=swimming)


def phi_1(x):
    return x[0] + x[1]*sin(2*pi*0.1) + x[2]*sin(2*pi*0.1)
net.make('phi_1',1,1,mode='direct')
net.connect('A','phi_1',func=phi_1)

def phi_2(x):
    return x[0] + x[1]*sin(2*pi*0.25) + x[2]*sin(2*pi*0.25)
net.make('phi_2',1,1,mode='direct')
net.connect('A','phi_2',func=phi_2)


def phi_3(x):
    return x[0] + x[1]*sin(2*pi*0.5) + x[2]*sin(2*pi*0.5)
net.make('phi_3',1,1,mode='direct')
net.connect('A','phi_3',func=phi_3)

net.add_to_nengo()