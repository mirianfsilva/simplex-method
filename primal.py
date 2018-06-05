import math, sys
from fractions import Fraction
from tableauform import change_tableau
from decimal import getcontext, Decimal

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


''' Função para checar o tableau pra saber se a PL é ilimitada, caso seja, retorna um certificado
'''	

def solution_unbounded(tableau, ratio, columns, index_column,output_2):
	if (ratio == math.inf):
		cert = [0 for _ in range(0, len(tableau[0]))] #vetor para o certificado
		for i in range(1, len(tableau)):
				for j in range(0, columns):
					if (tableau[i][j] == 1):
						for k in range(0, len(tableau)):
							if (tableau[k][j] == 0):
								tableau[i][index_column] = 1
								cert[j] = round((tableau[i][index_column]),3)
							break
		output_2.write(unbounded,'\n',cert)
		sys.exit()
		
''' Função de pivotamento primal, caso b > 0 e tenha valores < 0 em c, que nesse caso é a primeira linha do tableau[0]
'''    
def primal_pivot(tableau, _aux, lines, columns, index_column,output_2):
	ratio = math.inf
	index_line = math.inf
	#escolhe a linha baseado na menor razao positiva
	for i in range(1, len(tableau)):
		if (tableau[i][index_column] != 0):
			curr = tableau[i][-1] / tableau[i][index_column]
			if (curr < ratio and curr > 0):
				ratio = curr
				index_line = i

	solution_unbounded(tableau, ratio, columns, index_column,output_2)

	denominator = tableau[index_line][index_column]
	#divide a linha pelo valor temporario de um divisor calculado acima
	for i in range(0, len(tableau[0])):
		tableau[index_line][i] /= denominator
	for i in range(0, lines):
		_aux[index_line][i] /= denominator
	
	change_tableau(tableau, _aux,index_line,index_column)
	



