import os
import time 

clear = lambda: os.system('clear')
pc = 0
clock = 0


class instru(object):
	def __init__(self,clock,operandos,operacao):
		self.clock = clock
		self.operandos = operandos
		self.operacao = operacao
		

def inicializar(regis,dependentes):
	registrador = "$r" 
	x = [registrador+ str(i) for i in range(1,33)]
	for i in x:
		regis.update({i:0})
		dependentes.update({i:0})	


def add(operandos,regis):
	soma = regis[operandos[1]] + regis[operandos[2]]
	regis.update({operandos[0] : soma})

	

def addi(operandos,regis):
	soma = regis[operandos[1]] + int(operandos[2])
	regis.update({operandos[0] : soma})
	
def sub(operandos,regis):
	soma = regis[operandos[1]] - regis[operandos[2]]
	regis.update({operandos[0] : soma})

def subi(operandos,regis):
	soma = regis[operandos[1]] - int(operandos[2])
	regis.update({operandos[0] : soma})

def move(operandos,regis):
	regis.update({operandos[0]:regis[operandos[1]]})	
	
def jump(operandos,lines,pipeline):
	global buff
	global pc
	cont = 0
	for i in lines:
		if i == operandos[0]:
			pc = cont  
		else:
			cont = cont + 1	
	pipeline[0] = -1
	pipeline[1] = -1	
	buff = -1	



def execute(instrucao,regis,pipeline,lines):
	global clock
	if instrucao != -1 and instrucao != 0:

		if(instrucao.operacao == 'add'):
			
			add(instrucao.operandos,regis)

			mostraObj(pipeline,clock,regis)
			clock = clock + 1
		elif(instrucao.operacao == 'sub'):

			sub(instrucao.operandos,regis)
			mostraObj(pipeline,clock,regis)
			clock = clock + 1

		elif(instrucao.operacao == 'move'):
			

			move(instrucao.operandos,regis)
			


		elif(instrucao.operacao == 'addi'):
			
			addi(instrucao.operandos,regis)





		elif(instrucao.operacao.startswith('j')):
			

			jump(instrucao.operandos,lines,pipeline)




			
		elif(instrucao.operacao =='subi'):


			subi(instrucao.operandos,regis)




def limpar():
	x = input("Digite <enter> para prosseguir!")
	if not(x == ''):
		exit()	

def verificaPip(pipeline):
	for i in pipeline:
		if i != -1:
			return True
	return False	

def mostraObj(instrucoes,clock,regis):
	cont = 0
	print(clock,"º clock\n")

	for i in instrucoes:
		cont = cont + 1
		time.sleep(1)
		if i != -1 and i != 0:
			if cont == 1:
				print(cont,"Buscando Operando: ",i.operacao,' ',i.operandos,'\n')
			if cont == 2:
				print(cont,"Decodificando: ",i.operacao,' ',i.operandos,'\n')
			if cont == 3:
				print(cont,"Executando instrucao: ",i.operacao,' ',i.operandos,'\n')
			if cont == 4:
				print(cont,"Escrevendo resultado: ",i.operacao,' ',i.operandos,'\n')
				if i.operacao != 'j':	
					print("\n\n")
					print("------------REGISTRADORES ATUALIZADOS!!-----------")	
					print("\n\n")
					mostrar(regis)	
					limpar()

	print('\n\n')

def mostrar(regis):
	cont = 0
	for i in regis:
		print(i,":",regis[i],end = '|')
		if cont>10:
			cont = 0
			print('\n')
		cont = cont + 1
	print('\n')
	print('\n')	

def atualizaDependentes(dependentes,buff):
	if buff != -1:
		if buff.operandos != None:
			if len(buff.operandos)>=2:	
				dependentes.update({buff.operandos[0]: 1})

def verificaHazard(buff,dependentes,pipeline):

	if len(buff.operandos)>=2: # verifica se não é um jump 
		for i in buff.operandos:
			for j in range(3):
				if pipeline[j] != 0 and pipeline[j] != -1:
					if len(pipeline[j].operandos)>=2:
						if i == pipeline[j].operandos[0]:
							return True		
	return False				


		


def main():
	regis = {}
	dependentes = {}
	global clock
	global pc 
	global buff
	inicializar(regis,dependentes)

	pipeline = [0 for i in range(4)]


	with open('teste.txt') as f:
		lines = f.read().splitlines()

	instrucoes = []

	for i in lines:
		posicao = i.split(' ')
		if len(posicao)>1:			
			operadores = posicao[1].split(',')
			instrucao = instru(0,operadores,posicao[0])	
		instrucoes.append(instrucao)	



	while(verificaPip(pipeline)):

		if (pc>=len(instrucoes)):
			buff = - 1
		else:
			buff = instrucoes[pc]


		if buff != -1:
			while verificaHazard(buff,dependentes,pipeline):
				if pipeline[3] != 0 and pipeline[3] != -1:
					dependentes.update({pipeline[3].operandos[0] : 0})
				

				clock = clock + 1

				execute(pipeline[2],regis,pipeline,lines)
				pipeline[3] = pipeline [2]
				pipeline[2] = pipeline [1]
				pipeline[1] = pipeline [0]
				pipeline[0] = 0


		clock = clock + 1
		if pipeline[3] != 0 and pipeline[3] != -1:
			dependentes.update({pipeline[3].operandos[0] : 0})	

		atualizaDependentes(dependentes,buff)
		if pipeline[3] != 0 and pipeline[3] != -1:
			dependentes.update({pipeline[3].operandos[0] : 0})

		execute(pipeline[2],regis,pipeline,lines)
		pipeline[3] = pipeline [2]
		pipeline[2] = pipeline [1]
		pipeline[1] = pipeline [0]
		pipeline[0] = buff

		mostraObj(pipeline,clock,regis)
		print(pipeline)
		
		if pc<len(instrucoes):
			pc = pc + 1			


if __name__ == '__main__':
	main()