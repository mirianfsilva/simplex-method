import sys 

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

''' Standard form - FPI - matriz com adição de variaveis de folga
    range percorre uma lista estatica de inteiros que já "estão lá" para serem usadas 
    xrange not working in python 3
'''

def standard_form(matrix, lines):
	b = []  #vector column b
	#Add slack variables to matrix to transform all inequalities to equalities.
	for x in range(0, lines):
		matrix[0].append(0)
	for x in range(1, len(matrix)):
		b.append(matrix[x].pop())
	for x in range(1, len(matrix)):
		for y in range(1, len(matrix)):
			#add 1 on diagonals
			if x == y:
				matrix[x].append(1)
			else:
				matrix[x].append(0)
	for x in range(1, len(matrix)):
		matrix[x].append(b[x - 1])
	return (matrix, b)
	

def check_optimal(tableau):
	column_b = -1  #posição do vetor b no tableau
	#checa se o tableau final realmente tem c > 0
	for x in range(0, len(tableau[0]) - 1):
		if (tableau[0][x] < 0):
			return False

#checa se o tableau final realmente tem b > 0
	for x in range(1, len(tableau)):
		if (tableau[x][-1] < 0):
			return False
	return True

#função que modifica os valores das lines do tableau e da matriz de operações, após realizada a operação de pivotamento
def change_tableau(tableau, _aux, index_line, index_column):
    for i in range (0, len(tableau)):
        temp = tableau[i][index_column]
        if temp != 0 and i != index_line:
            for j in range(0,len(tableau[0])):
                tableau[i][j] -= temp*tableau[index_line][j]
            for j in range(0, len(tableau)-1):
                _aux[i][j] -= temp * _aux[index_line][j]

