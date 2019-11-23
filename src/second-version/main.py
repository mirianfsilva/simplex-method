#Python 3.6.1 (Dec 2015) [GCC 4.8.2] on linux
'''	PESQUISA OPERACIONAL 
	Mírian Francielle da Silva 
'''
import ast, sys
from tableaux import solution, solution_infeasible, solution_unbounded
from tableaux import primal_pivot, dual_pivot, matrix_ope, change_tableau

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

def map(f, it):
    result = []
    for x in it:
        result.append(f(x))
    return result

infeasible = 'Status: inviavel'
unbounded = 'Status: ilimitado'
optimal = 'Status: otimo'
linerules = 4 #linha que inicia as restrições

def check_optimal(tableau):
	#column_b = -1  #posição do vetor b no tableau
	#checa se o tableau final realmente tem c > 0
	for x in range(0, len(tableau[0]) - 1):
		if (tableau[0][x] < 0):
			return False

	#checa se o tableau final realmente tem b > 0
	for x in range(1, len(tableau)):
		if (tableau[x][-1] < 0):
			return False
	return True

def print_tableau(tableau):
	for i in range(0, len(tableau)):
		#tableau[i] = map(prettyfloat,tableau[i])
		print(tableau[i])
	print('\n')

with open("input.txt", "r") as csvfile:
    arq = csvfile.readlines()

columns = int(arq[0])
lines = int(arq[1])

var_conditions_temp = arq[2].split()
var_conditions = [float(i) for i in var_conditions_temp] 

objective_temp = arq[3].split()
objective = [float(i) for i in objective_temp]
objective.append(0) #valor obj

print ('COLUMS:', columns, 'LINES:', lines)
print('VAR CONDITIONS:', var_conditions)
print('OBJECTIVE:', objective)

matrix_temp = []
for i in range(linerules, linerules + lines):
    lines_temp = arq[i].split()
    matrix_temp.append(lines_temp)

#Standard Form
#greater than equal and less than equal equations 
#Add slack variables to matrix 
# to transform all inequalities to equalities.
"""
TO-DO: TODA VARIÁVEL LIVRE DEVE SE TORNAR DUAS VARIÁVEIS NÃO NEGATIVAS
"""

matrix_id = []
for x in range(0, lines):
    temp = []
    for y in range(0, lines):
        #add 1 on diagonals
        if (x == y):
            #check inequalities 
            if (matrix_temp[x][columns] == '>='):
                temp.append(-1)
            elif(matrix_temp[x][columns] == '<='):
                temp.append(1)
            #geq.append(x)
        else:
            temp.append(0)
    matrix_id.append(temp)
        
matrix = [] 
vc = [] #vector objetive c for tableau
for i in objective:
    vc.append(i)
for i in range(0, len(matrix_id)):
    vc.append(0)
matrix.append(vc)

#mudança dos valores da função objetiva no tableau
for i in range(0, columns):
	matrix[0][i] = matrix[0][i] * (-1)

for x in range(0,lines):
    temp = []
    for y in range(0, columns):
        temp.append(float(matrix_temp[x][y]))

    for k in range(0, len(matrix_id)):
        temp.append(matrix_id[k][x])
    temp.append(float(matrix_temp[x][-1])) #vector b
    matrix.append(temp)

print_tableau(matrix)

#matrix = sympy.Matrix(matrix)
#reduced_form = matrix.rref()
#check linear independence in tableau 
temp = 0
auxtableau = matrix_ope(matrix, lines, columns)
tableau = matrix
while (temp == 0):
	#checa vetor b do tableau, se possuir entradas negativas aplica o dual
	for i in range(1, len(tableau)):
		if (tableau[i][-1] < 0):
			dual_pivot(tableau, auxtableau, lines, i)
			break
    #checa vetor c do tableau, se possuir entradas negativas aplica o primal
	for i in range(0, (len(tableau[0]) - 1)):
		if (tableau[0][i] < 0):
			primal_pivot(tableau, auxtableau, lines, columns, i)
			break
	
	temp = check_optimal(tableau)
