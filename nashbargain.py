import sympy as sym
import numpy as np
import itertools
from operator import itemgetter


class nashsolution():
    
    def __init__(self,breakpoint,utilities):
        self.breakpoint = np.array(breakpoint)
        self.NUM_PLAYERS = breakpoint.shape[0]
        self.utilities = np.array(utilities)

    def fast_soln(self):
        soln = np.prod((self.utilities - self.breakpoint),1)
        return (np.argmax(soln),np.max(soln))

    def solution_space(self,pnts):
        # boundry_points = np.array([a for a in utilities if (a>=breakpoint).all()])
        # return list(itertools.combinations(boundry_points,2))
        lhs = self.breakpoint - pnts[0]
        rhs = pnts[1] - pnts[0]
        try:
            lesser_than = min([l/r for l,r in zip(lhs,rhs) if r<0])
            greater_than = max([l/r for l,r in zip(lhs,rhs) if r>0])
            if greater_than > lesser_than:
                return False
            return (greater_than < 1) and (lesser_than > 0)
        except ValueError:
            return False

    
    def find_max(self,end_points):
        if not self.solution_space(end_points):
            return None
        t = sym.symbols('t')
        line_expr = end_points[0] + t*(end_points[1]-end_points[0])
        max_utility = np.prod(line_expr - self.breakpoint)
        maxima = sym.solve(sym.diff(max_utility,t),t)
        maxima = np.array([i for i in maxima if (0<i and i<1)])
        maxima = np.append(maxima,[0,1])
        utility_values_maxima = np.array([max_utility.subs(t,i).evalf() for i in maxima])
        #index of the point which gives max utility
        index = utility_values_maxima.argmax()
        final_t_val = maxima[index]
        return (utility_values_maxima[index],np.array([i.subs(t,final_t_val) for i in line_expr]))

    def find_global_max(self):
        #line_pairs = self.solution_space(self.utilities,self.breakpoint)
        line_pairs = list(itertools.combinations(self.utilities,2))
        solns = filter(None,[self.find_max(i) for i in line_pairs])
        return (max(solns,key=itemgetter(0))[1]).astype('float64')


        
        

        

        
   


