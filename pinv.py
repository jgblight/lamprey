import numpy as np
import sys

matrix = sys.argv[1]

matrix = np.array([[ float(x) for x in y.split(',')] for y in matrix.split(';') ])

inv = np.linalg.pinv(matrix)

output =  ';'.join([ ','.join([str(y) for y in x]) for x in inv])
f = open('/Users/jgblight/Documents/Neuro/lamprey/output','w')
f.write(output)
f.close()