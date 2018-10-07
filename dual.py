import math, sys
from tableauform import change_tableau

infeasible = 0
unbounded = 1
optimal = 2

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def map(f, it):
    result = []
    for x in it:
        result.append(f(x))
    return result

def solution_infeasible(tableau, _aux):
	for i in range(1, len(tableau)):
		for j in range(0, len(tableau[0])):
			if (tableau[i][j] <= 0):
				break
			if (j == len(tableau[0]) - 1):
				if (tableau[i][j] < 0):
					out_aux = map(prettyfloat, _aux[i])
					return(infeasible, out_aux)
					sys.exit()
    
def dual_pivot(tableau, _aux, lines, index_line):
	ratio = math.inf
	index_column = math.inf

	#menor razão positiva da coluna
	for i in range(0, len(tableau[0])):
		if (tableau[index_line][i] != 0):
			curr = (tableau[0][i] / (tableau[index_line][i]) * (-1))
			if (curr < ratio and curr > 0):
				ratio = curr
				index_column = i
	
	solution_infeasible(tableau, _aux)
    
	denominator = tableau[index_line][index_column]
	for i in range(0, len(tableau[0])):
		tableau[index_line][i] /= denominator
	for i in range(0, lines):
		_aux[index_line][i] /= denominator
	change_tableau(tableau, _aux, index_line, index_column)
