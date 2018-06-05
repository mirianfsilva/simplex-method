#Python 3.6.1 (Dec 2015) [GCC 4.8.2] on linux
import ast, sys
import tableauform
from dual import dual_pivot
from primal import primal_pivot
from fractions import Fraction
import numpy as np
import json

#from decimal import getcontext, Decimal
# Set the precision.
#getcontext().prec = 2

#precisão das casas decimais na saída do problema
class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

#pra usar em listas de valores que podem ser iteradas
#alterar as casas decimais de uma lista
def map(f, it):
    result = []
    for x in it:
        result.append(f(x))
    return result

#printar tableau
def print_tableau(tableau):
	
	for i in range(0, len(tableau)):
		tableau[i] = map(prettyfloat,tableau[i])
		#print(tableau[i])
	#print('\n')
			
	#a cada chamada o arquivo é atualizado, então só a ultima fase do pivotamento vai ser impressa no arquivo, porque vai ser a ultima sobreposição
	with open("pivotamento.txt", "w") as file_1:
		for i in range(0, len(tableau)):
			file_1.write('[')
			file_1.write(', '.join(map(str,tableau[i])))
			file_1.write(']')
			file_1.write('\n')
	

''' A saída deve conter a seguinte informação: Dizer se o problema é inviável (INFEASIBLE) com output = 0; ou dizer que o problema é viável mas possui solução ilimitada (FEASIBLE & UNBOUNDED) com output = 1; ou se o problema é viável e limitado, sendo assim possui solução ótima, (FEASIBLE & BOUNDED) com output = 2, e a solução ótima contendo os valores das variáveis {x1,..., xn}; isto é, valores das variáveis e valor objetivo da solução ótima. 
'''
infeasible = 0
unbounded = 1
optimal = 2

''' Sempre que a entrada do programa é inviável ou a solução é ilimitada, a saída do modo detalhado deve dar alguma evidência para essa conclusão, sendo assim apresentar um certificado.
'''

#função que retorna o vetor solução
def solution(tableau, lines, columns):
	var_solution = [0 for _ in range(0,columns)]
	#print (len(tableau),columns)
	for i in range(1, len(tableau)):
		for j in range(0, columns):
			if(tableau[i][j] == 1):
				#print ('POSIÇÃO IGUAL A 1 verificar',i,j)
				for k in range(0, len(tableau)):
					if tableau[k][j] == 0:
						#print ('basica na posição', j, tableau[i][-1])
						var_solution[j] = round(tableau[i][-1],3)
						#print (var_solution)
						break
	return (var_solution)
	
''' Função que cria uma matriz para armazenar as operacoes realizadas durante o pivotamento no tableau
'''
def matrix_ope(matrix, lines, columns):
	#matriz de operacoes com posições vazias
	_aux = [[] for i in range(len(matrix))]
	for i in range(0, lines):
		#zeros no vetor c
		_aux[0].append(0)
	for i in range(1, len(matrix)):
		for j in range(1, len(matrix)):
			#criação da matriz identidade
			if j == i:
				_aux[i].append(1)
			else:
				_aux[i].append(0)
	return _aux

''' Procedimento que realiza o simplex na matriz já em FPI. A função verifica se é possível realizar o dual primeiro na matriz, caso contrário, faz o procedimento de pivotamento primal, e recebe a matriz, linhas e colunas como parametro como especificado da descrição do trabalho.
'''
def simplex(matrix, lines, columns):
	
	#coloca a matriz em FPI para começar as operações
	tableauform.standard_form(matrix, lines)
	tableau = matrix

	#matriz de operações
	aux = matrix_ope(tableau, lines, columns)

	#mudança dos valores da função objetiva no tableau
	for i in range(0, columns):
		tableau[0][i] = tableau[0][i] * (-1)

	temp = 0
	print_tableau(tableau)
	while (temp == 0):
		#checa vetor b do tableau, se possuir entradas negativas aplica o dual
		for i in range(1, len(tableau)):
			if (tableau[i][-1] < 0):
				dual_pivot(tableau, aux, lines, i)
				break

        #checa vetor c do tableau, se possuir entradas negativas aplica o primal
		for i in range(0, (len(tableau[0]) - 1)):
			if (tableau[0][i] < 0):
				primal_pivot(tableau, aux, lines, columns, i)
				break
			
		print_tableau(tableau)
		temp = tableauform.check_optimal(tableau)
	
	#print_tableau(tableau)
	#se tem solução ótima, retorna o vetor das variáveis
	var_solution = solution(tableau, lines, columns)
	cert = map(prettyfloat, aux[0])
	v_obj = round(tableau[0][-1],3)
	output_2 = [optimal,var_solution,v_obj,cert]
	
	with open("conclusão.txt","w") as file_2:
		file_2.write('\n'.join(map(str, output_2)))
	
	#print('\n'.join(map(str, output_2)))
	#print('', optimal,'\n',var_solution,'\n', v_obj,'\n', cert)


#saida no arquivo	
def print_output1(arg):
	with open("pivotamento.txt","w") as output_1:
		output_1.write(arg)
	
''' Ler arquivo usando: ast – Abstract Syntax Trees
    Tentar essa leitura caso literal_eval não funcione: 
    str(self.lostfeatures).replace('[array([[','').replace(']], dtype=float32)
    funçaõ l.strip remove caracters da linha
'''
with open("input.txt", "r") as csvfile:
	count = 0
	for l in csvfile:
		count += 1
		if count == 1:
			lines = ast.literal_eval(l.strip())
			#lines = np.array(eval())
		elif count == 2:
			columns = ast.literal_eval(l.strip())
			#columns = np.array(eval())
		elif count == 3:
			matrix = ast.literal_eval(l.strip())
			#matrix = np.array(eval())
#print (lines, columns, matrix)

simplex(matrix, lines, columns)


#https://www.kdnuggets.com/2017/03/working-numpy-matrices.html
#https://docs.python.org/3.1/library/fractions.html
