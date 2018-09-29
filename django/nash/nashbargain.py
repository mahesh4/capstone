import sympy as sym
import numpy as np
import itertools
from operator import itemgetter


class nashsolution():
    NUM_PLAYERS = None
    utilities = None
    breakpoint = None
    
    def __init__(self,breakpoint,utilities):
        self.breakpoint = breakpoint
        self.NUM_PLAYERS = breakpoint.shape[0]
        self.utilities = utilities


    def solution_space(self,utilities,breakpoint):
        boundry_points = np.array([a for a in utilities if (a>=breakpoint).all()])
        return list(itertools.combinations(boundry_points,2))
    
    def find_max(self,end_points):
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
        line_pairs = self.solution_space(self.utilities,self.breakpoint)
        solns = [self.find_max(i) for i in line_pairs]
        return max(solns,key=itemgetter(0))[1]


        
        

        

        
   


