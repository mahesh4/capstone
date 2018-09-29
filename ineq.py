import numpy as np
a = np.array([1,2,3,2])
b = np.array([[2,3,4,5],[3,2,4,4]])
# pnt < endpnt[0] - t(endpnt[0] - endpnt[1]) 
lhs = a - b[0]
rhs = b[1]-b[0]
greater_than = float('-Inf')
lesser_than = float('+Inf')

'''for i in range(4):
  if rhs[i]<0:
    lesser_than = min(lhs[i]/rhs[i],lesser_than)
  elif rhs[i] > 0:
    greater_than = max(lhs[i]/rhs[i],greater_than)'''
lesser_than = min([l/r for l,r in zip(lhs,rhs) if r<0])
greater_than = max([l/r for l,r in zip(lhs,rhs) if r>0])

print (greater_than,lesser_than)
print (greater_than < 1) and (lesser_than > 0)
