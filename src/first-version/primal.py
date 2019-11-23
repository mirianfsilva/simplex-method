import math, sys
from tableauform import change_tableau

infeasible = 0
unbounded = 1
optimal = 2

class prettyfloat(float):
    def __repr__(self):
        return "%0.5f" % self

def map(f, it):
    result = []
    for x in it:
        result.append(f(x))
    return result

def solution_unbounded(tableau, ratio, columns, index_column):
	if (ratio == math.inf):
		cert = [0 for _ in range(0, len(tableau[0])-1)]
		for i in range(1, len(tableau)):
				for j in range(0, len(tableau[0])-1):
					if tableau[i][j] == 1:
						for k in range(0, len(tableau)):
							if tableau[k][j] != 0:
								if tableau[i][index_column] == 0: 
									cert[j] = round((tableau[i][index_column]),5)
								elif tableau[i][index_column] > 0 or tableau[i][index_column] < 0: 
									cert[j] = (-1)*round((tableau[i][index_column]),5)
							cert[index_column] = 1 
					elif tableau[i][index_column] > 0 or tableau[i][index_column] < 0:
						continue
					break
		output_2 = [unbounded,cert]
		with open("conclusão.txt","w") as file_2:
			file_2.write('\n'.join(map(str, output_2)))
		sys.exit()
		
''' Função de pivotamento primal, caso b > 0 e tenha valores < 0 em c, que nesse caso é a primeira linha do tableau[0]
'''    
def primal_pivot(tableau, _aux, lines, columns, index_column):
	ratio = math.inf
	index_line = math.inf
	for i in range(1, len(tableau)):
		if (tableau[i][index_column] != 0):
			curr = tableau[i][-1] / tableau[i][index_column]
			if (curr < ratio and curr > 0):
				ratio = curr
				index_line = i

	solution_unbounded(tableau, ratio, columns, index_column)

	denominator = tableau[index_line][index_column]
	#divide a linha pelo valor temporario de um divisor calculado acima
	for i in range(0, len(tableau[0])):
		tableau[index_line][i] /= denominator
	for i in range(0, lines):
		_aux[index_line][i] /= denominator
	
	change_tableau(tableau, _aux,index_line,index_column)
	
