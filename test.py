import numpy as np
import nashbargain as nb
brk = np.array([.3,.2])
util = np.array([[0,1],[1,0],[0,0]])
a = nb.nashsolution(brk,util)
print a.find_global_max()
