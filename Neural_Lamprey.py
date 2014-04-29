import nef
from ca.nengo.math.impl import ConstantFunction, FourierFunction, PostfixFunction
import math


# Network Neural Lamprey Start
net_Neural_Lamprey = nef.Network('Neural Lamprey')

# Neural Lamprey - Nodes
net_Neural_Lamprey.make('a', 400, 10, tau_rc=0.020, tau_ref=0.002, max_rate=(200.0, 400.0), intercept=(-1.0, 1.0), radius=20.00)
net_Neural_Lamprey.make('T1', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(200.0, 400.0), intercept=(-1.0, 1.0), radius=1.00)
net_Neural_Lamprey.make('T3', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(200.0, 400.0), intercept=(-1.0, 1.0), radius=1.00)
net_Neural_Lamprey.make('T2', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(200.0, 400.0), intercept=(-1.0, 1.0), radius=1.00)

# Neural Lamprey - Templates

# Neural Lamprey - Projections
transform = [[1.0]]
net.connect('a','T1',func=lambda x: T(x,0.25))
net_Neural_Lamprey.connect('a', 'T1', transform=transform, func=<lambda>)

transform = [[1.0]]
net.connect('a','T1',func=lambda x: T(x,0.25))
net_Neural_Lamprey.connect('a', 'T2', transform=transform, func=<lambda>)

transform = [[1.0]]
net.connect('a','T1',func=lambda x: T(x,0.25))
net_Neural_Lamprey.connect('a', 'T3', transform=transform, func=<lambda>)


# Network Neural Lamprey End

net_Neural_Lamprey.add_to_nengo()
