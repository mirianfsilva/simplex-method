import math, sys
from tableauform import change_tableau

infeasible = 0
unbounded = 1
optimal = 2

#precisão das casas decimais na saída do problema
class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

#pra usar em listas de valores que podem ser iteradas
def map(f, it):
    result = []
    for x in it:
        result.append(f(x))
    return result

''' Função que verifica no pivotamento dual se a PL é inviável, e retorna um certificado, resultado das operações da matriz de operações. 
'''
def solution_infeasible(tableau, _aux,output_2):
	for i in range(1, len(tableau)):
		for j in range(0, len(tableau[0])):
			if (tableau[i][j] <= 0):
				break
			if (j == len(tableau[0]) - 1):
				if (tableau[i][j] < 0):
					out_aux = map(prettyfloat, _aux[i])
					output_2.write(infeasible, '\n', out_aux)
					sys.exit()
    
''' Escolhe número para realizar pivoteamento dual, e faz o pivoteamento. 
'''
def dual_pivot(tableau, _aux, lines, index_line,output_2):
	ratio = math.inf
	index_column = math.inf

	#menor razão positiva da coluna
	for i in range(0, len(tableau[0])):
		if (tableau[index_line][i] != 0):
			curr = (tableau[0][i] / (tableau[index_line][i]) * (-1))
			#print (tableau[0][i], tableau[index_line][i]*(-1), curr)
			if (curr < ratio and curr > 0):
				ratio = curr
				index_column = i
	#checa se o tableau pra saber se a PL é inviável
	#retorna um certificado resultado das operações da matriz de operações
	solution_infeasible(tableau, _aux,output_2)
    
	denominator = tableau[index_line][index_column]
	#divide a linha pelo valor temporario de um divisor calculado acima
	for i in range(0, len(tableau[0])):
		tableau[index_line][i] /= denominator
	for i in range(0, lines):
		_aux[index_line][i] /= denominator
	change_tableau(tableau, _aux, index_line, index_column)
