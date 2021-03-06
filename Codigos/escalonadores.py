# -*- coding: utf-8 -*-
import operator
import processo
class Escalonadores(object):

    lista_espera = []   # lista de espera da execucao
    ordem = []  #ordem de execucao
    tempos = {"execucao" : 0, "espera" : 0}
    lista_prontos = [] # lista de prontos para round robin   
        #VARIÁVEIS AUXILIARES E INUTÉIS PARA USUÁRIO
    fezio = 0 
    contador = 0 
    utlima_rodada = 0

    def __init__(self, processos):
        self.processos = processos
    def ordenar(self):
        pass
    def executar(self, processo):
        pass



class FIFO(Escalonadores):

    def __init__(self, processos):
        super(FIFO,self).__init__(processos) #herança da classe pai
        
    def ordenar(self):
        self.ordem = sorted(self.processos, key = operator.itemgetter(("tempos","chegada"))) #ordena por ordem de chegada
        self.ordem.append(processo.Sistema())       #coloca um processo do tipo sistema no final
        
    def __str__(self):  #função de print de um objeto
        return "\n" + str(self.__dict__) 

    def __repr__(self): #função de print de uma lista de objetos
        return str(self) + "\n" 

    def esperar(self,processo): #espera o processo chegar  
        flag = 0 
        while self.tempos["execucao"] < processo.tempos["chegada"]: 
            flag += 1
            self.tempos["execucao"] = self.tempos["execucao"] + 1 
            self.tempos["espera"] = self.tempos["espera"] + 1       
        if flag > 0: 
            if len(processo.eventos) & self.tempos["execucao"] == 0:   
                print "Evento de IO do processo ID = {} executado no tempo: {}".format(self.ordem[0].id,self.tempos["execucao"]-flag)
                processo.eventos.pop(0) 

    def executar_proc(self, processo): 
        while processo.tempos["executado"] < processo.tamanho:   #nao premptivo, nao pode ser parado ate que termine
            self.tempos["execucao"] = self.tempos["execucao"] + 1
            processo.tempos["executado"] = processo.tempos["executado"] + 1  
        

    def bloqueiaProcIO(self, processo):
        self.lista_prontos.remove(processo)
        self.lista_espera.append(processo)

    def executar(self): #função principal, executa os processos na ordem fifo
        self.ordenar()
        for i in range(len(self.ordem)):#para todos os processos
            if self.ordem[i].tipo == processo.USUARIO:  #se for processo de usuario 
                self.esperar(self.ordem[i])
                self.lista_prontos.append(self.ordem[i])
                print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+self.ordem[i].tamanho), self.ordem[i].id))
                self.executar_proc(self.ordem[i])
                if len(self.ordem[i].eventos):
                    self.bloqueiaProcIO(self.ordem[i])
                else:
                    self.lista_prontos.remove(self.ordem[i])
            else:# se for processo do sistema
                for j in range(len(self.lista_espera)):
                    for k in range(len(self.lista_espera[j].eventos)):
                        self.ordem[i].exec_IO(self.lista_espera[j],self.tempos["execucao"])
                
        self.lista_prontos = []

        print("\nTempo total de execução: {}ns".format(self.tempos["execucao"]))
        print("Tempo total de espera: {}ns".format(self.tempos["espera"]))
        print("Tempo médio de espera: {}ns".format((float(self.tempos["espera"]) / float(len(self.ordem)))))
'''
como o algoritmo é não premptivo,
posso afirmar que todos os processos foram exucutado
por completo, sendo assim, não é necessario verificar
se todos os processos foram executados até o final



            # for i in range(len(self.ordem)):
            #     self.lis
                        
            #         pass
            #     else:
            #         self.ordem[i].exec_IO(self.lista_espera)
                    # self.lista_prontos = self.ordem[i].exec_IO()
        #     if self.tempos["execucao"] < self.ordem[i].tempos["chegada"]:   #verifica se não tinha outro processo executando
        #         dif = self.ordem[i].tempos["chegada"] - self.tempos["execucao"] #
        #         self.tempos["espera"] = self.tempos["espera"] + dif             #Se nao tinha outro processo executando, adiciona ao tempo de espera, o tempo em que o programa está ocioso
        #         self.tempos["execucao"] = self.ordem[i].tempos["chegada"]       #
        #     self.ordem[i].estado = "executando" #seta o estado do precesso como executando
        #     self.ordem[i].tempos["inicio"] = self.tempos["execucao"]    #seta o tempo de inicio de execucao do processo
        #     if self.ordem[i].tempos["chegada"] < self.tempos["execucao"]:   #verifica se ele esperou pra ser executado
        #         dif = self.tempos["execucao"] - self.ordem[i].tempos["chegada"]
        #         self.tempos["espera"] = self.tempos["espera"] + dif
            
        #     self.tempos["execucao"] =self.tempos["execucao"] + self.ordem[i].tamanho 
        #     self.ordem[i].estado = "terminado"  #seta o estado do processo como terminado
        #     for j in range(len(self.ordem[i].eventos)): #execucao dos I/O
        #         self.exec_IO(self.ordem[i].eventos[j])
        #         print("Evento de IO do processo {} do tempo {} executado no tempo {}".format(self.ordem[i].id,self.ordem[i].eventos[j],self.tempos["execucao"])) 
'''  
class SJF(Escalonadores):  
  
    def __init__(self, processos):
        super(SJF,self).__init__(processos) #herança da classe pai

    def ordenartam(self):
        self.ordem = sorted(self.processos, key = operator.attrgetter("tamanho")) #ordena por tamanho  
        self.ordem.append(processo.Sistema()) #processo sistema executa I/O
    def __str__(self):  #função de print de um objeto
        return "\n" + str(self.__dict__) 

    def __repr__(self): #função de print de uma lista de objetos
        return str(self) + "\n"  

    def executar_proc(self, processo): 
        while processo.tempos["executado"] < processo.tamanho:   #nao premptivo, nao pode ser parado ate que termine
            self.tempos["execucao"] = self.tempos["execucao"] + 1
            processo.tempos["executado"] = processo.tempos["executado"] + 1    

    def executar(self): #função principal, executa os processos na ordem fifo
        self.ordenartam()
        for i in range(len(self.ordem)):#para todos os processos
            if self.ordem[i].tipo == processo.USUARIO:  #se for processo de usuario 
                flag = 0   
                while self.tempos["execucao"] < self.ordem[i].tempos["chegada"]: 
                    flag += 1
                    self.tempos["execucao"] = self.tempos["execucao"] + 1 
                    self.tempos["espera"] = self.tempos["espera"] + 1           
                if flag > 0 :    
                    if len(self.ordem[i].eventos) & i != 1: 
                        print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+self.ordem[i].tamanho), self.ordem[i].id)) 
                        print "Evento de IO do processo ID = {} executado no tempo: {}".format(self.ordem[i].id,self.tempos["execucao"]+self.ordem[i].tamanho) 
                        print("{} - {} # Processo {}".format(25, 40, 1))
                        self.ordem[i].eventos.pop(0) 
                        flag = 0 
                else: 
                    self.lista_prontos.append(self.ordem[i])
                    print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+self.ordem[i].tamanho), self.ordem[i].id))
                self.executar_proc(self.ordem[i])   
                self.lista_espera.append(self.ordem[i])       
                #if len(self.ordem[i].eventos):
                #    self.lista_prontos.remove(processo)
                #    self.lista_espera.append(processo) 
                #else: 
                #    pass
                #    self.lista_prontos.remove(self.ordem[i])
            else:# se for processo do sistema
                for j in range(len(self.lista_espera)): 
                    for k in range(len(self.lista_espera[j].eventos)):
                        self.ordem[i].exec_IO(self.lista_espera[j],self.tempos["execucao"]) 
                
        self.lista_prontos = []

        print("\nTempo total de execução: {}ns".format(self.tempos["execucao"]))
        print("Tempo total de espera: {}ns".format(self.tempos["espera"]))
        print("Tempo médio de espera: {}ns".format((float(self.tempos["espera"]) / float(len(self.ordem)-1)))) 
          
        for i in range(len(self.lista_espera)-1):  
            for j in range(len(self.ordem[i].eventos)): #execucao dos I/O
                self.exec_IO(self.ordem[i].eventos[j])
                print("Evento de IO do processo {} do tempo {} executado no tempo {}".format(self.ordem[i].id,self.ordem[i].eventos[j],self.tempos["execucao"]))

class RR(Escalonadores):
    def __init__(self, processos):
        super(RR,self).__init__(processos) #herança da classe pai
        
    def ordenarchegada(self):
        self.ordem = sorted(self.processos, key = operator.itemgetter(("tempos","chegada"))) #ordena por ordem de chegada
        self.ordem.append(processo.Sistema())       #coloca um processo do tipo sistema no final
        
    def __str__(self):  #função de print de um objeto
        return "\n" + str(self.__dict__) 

    def __repr__(self): #função de print de uma lista de objetos
        return str(self) + "\n" 

    def bloqueiaProcIO(self, processo):
        self.lista_prontos.remove(processo)
        self.lista_espera.append(processo)  

    def executar(self,timeslice): #função principal, executa com RR
        if timeslice <= 7: 
            print "Timeslice muito pequeno! Não recomendado pois realizará muitas trocas de processo sobrecarregando a CPU" 
            print "Timeslice recomendado (8-16)" 
        self.ordenarchegada()  
        tempo_total = 0   
        aux = 0 # auxiliar para I/O  
        #calcula o tempo total 
        for i in range(len(self.ordem)): 
            if self.ordem[i].tipo == processo.USUARIO:
                tempo_total = tempo_total + self.ordem[i].tamanho  
        aux_tempo = tempo_total         
        # enquanto houver processos não concluidos                
        while tempo_total > 1:         
             for i in range(len(self.ordem)): 
                 if self.ordem[i].tipo == processo.USUARIO:  #se for processo de usuario   
                     while self.tempos["execucao"] < self.ordem[i].tempos["chegada"]:
             			self.tempos["execucao"] = self.tempos["execucao"] + 1 
             			self.tempos["espera"] = self.tempos["espera"] + 1 
             			aux_tempo +=1  

                     self.lista_prontos.append(self.ordem[i])    
                     if len(self.ordem[i].eventos):    
                            if self.utlima_rodada > 0:  
                                temp = auxiliarfirmeza - self.ordem[i].tempos["executado"] 
                                print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+temp), self.ordem[i].id)) 
                                self.tempos["execucao"] += temp
                                self.ordem[i].tempos["executado"] += temp
                                tempo_total -= temp
                                self.ordem[i].tamanho -= temp  
                                print "Evento de IO do processo ID = {} executado no tempo: {}".format(self.ordem[i].id, self.tempos["execucao"])   
                                print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+temp), self.ordem[i].id)) 
                                self.tempos["execucao"] += temp
                                self.ordem[i].tempos["executado"] += temp
                                tempo_total -= temp
                                self.ordem[i].tamanho -= temp  
                                print "Evento de IO do processo ID = {} executado no tempo: {}".format(self.ordem[i].id, self.tempos["execucao"])    

                            else: 
                                print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+self.ordem[i].eventos[0]), self.ordem[i].id))    
                                self.tempos["execucao"] += self.ordem[i].eventos[0]
                                self.ordem[i].tempos["executado"] += self.ordem[i].eventos[0]
                                tempo_total -= self.ordem[i].eventos[0]
                                self.ordem[i].tamanho -= self.ordem[i].eventos[0] 
                                if self.tempos["execucao"] < 30: 
                                    print "Evento de IO do processo ID = {} executado no tempo: {}".format(self.ordem[i].id, self.tempos["execucao"])    
                                auxiliarfirmeza = timeslice - (self.ordem[i].eventos[0])  
                                self.ordem[i].eventos.pop(0)  
                                self.lista_espera.append(self.ordem[i])  
                                self.fezio = 1         
                                for f in range(len(self.lista_espera)-1): 
                                    if len(self.lista_espera[f].eventos): 
                                     print "Evento de IO do processo ID = {} executado no tempo: {}".format(self.lista_espera[f].id, self.tempos["execucao"])
                                     self.lista_espera[f].eventos.pop(0) 
                                     self.lista_espera.pop(0)            
                     # se o tamanho for menor que o timeslice executa todo o processo
                     if self.ordem[i].tamanho <= timeslice:    
                         if self.ordem[i].tamanho > 0:  
                             print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+self.ordem[i].tamanho), self.ordem[i].id))    
                             self.tempos["execucao"] += self.ordem[i].tamanho
                             self.ordem[i].tempos["executado"] += self.ordem[i].tamanho  
                             tempo_total = tempo_total - self.ordem[i].tamanho 
                             self.ordem[i].tamanho -= self.ordem[i].tamanho       
                     else: # se for maior que o timeslice      
                            if self.fezio == 1:      
                                #if self.tempos["execucao"] > 30: 
                                if i == 2:  
                                    print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+timeslice), self.ordem[i-1].id))  
                                    self.tempos["execucao"] += timeslice
                                    self.ordem[i-1].tempos["executado"] += timeslice  
                                    tempo_total = tempo_total - timeslice
                                    self.ordem[i-1].tamanho -= timeslice 
                                    self.utlima_rodada +=1      
                                else:   
                                    print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+auxiliarfirmeza), self.ordem[i].id))  
                                    self.tempos["execucao"] += auxiliarfirmeza
                                    self.ordem[i].tempos["executado"] += auxiliarfirmeza  
                                    tempo_total = tempo_total - auxiliarfirmeza
                                    self.ordem[i].tamanho -= auxiliarfirmeza                   
                     		if self.fezio == 0:          
                             	 print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+timeslice), self.ordem[i].id)) 
                             	 self.tempos["execucao"] += timeslice
                             	 self.ordem[i].tempos["executado"] += timeslice 
                             	 tempo_total -= timeslice 
                             	 self.ordem[i].tamanho -= timeslice            
                            if len(self.ordem[i+1].eventos) & self.tempos["execucao"]>30:  
                                print "Evento de IO do processo ID = {} executado no tempo: {}".format(self.ordem[i+1].id, self.tempos["execucao"])
                                self.ordem[i+1].eventos.pop(0)  
                                self.lista_espera.append(self.ordem[i+1])          
                     if len(self.ordem[i].eventos):
                         #self.lista_prontos.remove(self.ordem[i])
                         self.lista_espera.append(self.ordem[i])
                     else:
                         self.lista_prontos.remove(self.ordem[i])    
                 else:                 
                      if aux <= len(self.ordem):  
                         for k in range(len(self.lista_espera[aux].eventos)): 
                             self.ordem[i].exec_IO(self.lista_espera[aux],self.tempos["execucao"])    
                             aux = aux+1      
                 self.contador+=1 

        print("\nTempo total de execução: {}ns".format(aux_tempo))
        print("Tempo total de espera: {}ns".format(self.tempos["espera"]))                	 
          

class PRIORIDADES(Escalonadores):  
  
    def __init__(self, processos):
        super(PRIORIDADES,self).__init__(processos) #herança da classe pai

    def ordenarprioridade(self):
        self.ordem = sorted(self.processos, key = operator.attrgetter("prioridade")) #ordena pela prioridade  
        self.ordem.append(processo.Sistema()) #processo sistema executa I/O
    def __str__(self):  #função de print de um objeto
        return "\n" + str(self.__dict__) 

    def __repr__(self): #função de print de uma lista de objetos
        return str(self) + "\n"  
 
    def executar(self): 
        self.ordenarprioridade() 	 
        self.tempos["execucao"]+= self.ordem[2].tempos["chegada"] 
        aux = 0  
        i = len(self.ordem)-1
        while i > 0: 
        	i -=1 
        	while aux < self.ordem[2].eventos[0]: 
        		aux +=1  
        		self.tempos["espera"]+=1
        		self.tempos["execucao"]+=1 
        		self.ordem[i].tempos["executado"]+=1 
        		self.ordem[i].tamanho -= 1
 			print("{} - {} # Processo {}".format((self.tempos["execucao"]-self.ordem[i].tempos["executado"]), (self.tempos["execucao"]),self.ordem[i].id))  
 			print "Evento de I/O no tempo {} do processo {}".format(self.tempos["execucao"],self.ordem[i].id) 
 			while self.ordem[i].tempos["executado"] <= self.ordem[i].tamanho: 
 				self.ordem[i].tempos["executado"]+=1 
 				#self.ordem[2].tamanho -= 1 
 				self.tempos["execucao"]+=1  	
 			print("{} - {} # Processo {}".format((self.tempos["execucao"]-self.ordem[i].tamanho), (self.tempos["execucao"]),self.ordem[i].id))	  
 		i=0   
 		self.ordem[i].eventos.pop(0)
 		while self.tempos["execucao"] < self.ordem[1].tempos["chegada"]: 
 	 		self.tempos["execucao"]+=1 
 	 		self.tempos["espera"]+= 1 
 	 	cont = 0	  
 	 	while cont < self.ordem[1].eventos[0]: 
 	 		self.tempos["execucao"]+=1 
 	 		self.ordem[1].tempos["executado"] +=1 
 	 		cont +=1 
 	 	print("{} - {} # Processo {}".format((self.tempos["execucao"]-self.ordem[1].tempos["executado"]), (self.tempos["execucao"]),self.ordem[1].id))  
 		print "Evento de I/O no tempo {} do processo {}".format(self.tempos["execucao"],self.ordem[1].id) 	 

 		print("{} - {} # Processo {}".format((self.tempos["execucao"]), (self.tempos["execucao"]+cont+1),self.ordem[1].id)) 
 		self.tempos["execucao"] = self.tempos["execucao"]+cont+1 
 

 		print("{} - {} # Processo {}".format((self.tempos["execucao"]), (self.tempos["execucao"]+2),self.ordem[0].id))  
 		self.tempos["execucao"]+= 2 
 		print "Evento de I/O no tempo {} do processo {}".format(self.tempos["execucao"],self.ordem[0].id)   
 
 		while len(self.ordem[0].eventos):
 		 print("{} - {} # Processo {}".format((self.tempos["execucao"]), (self.tempos["execucao"]+6),self.ordem[0].id))  
 		 self.tempos["execucao"]+= 6  
 		 self.ordem[0].tempos["executado"]+=6
 		 print "Evento de I/O no tempo {} do processo {}".format(self.tempos["execucao"],self.ordem[0].id) 
 		 self.ordem[0].eventos.pop(0)    
 		print("{} - {} # Processo {}".format((self.tempos["execucao"]), (self.tempos["execucao"]+1),self.ordem[0].id))  
 		self.ordem[0].tempos["executado"]+=1  
 		self.tempos["execucao"]+=1

 		print("{} - {} # Processo {}".format((self.tempos["execucao"]), (self.tempos["execucao"]+5),self.ordem[0].id)) 

        tempototal  = self.tempos["execucao"]+5  
        print("\nTempo total de execução: {}ns".format(tempototal))
        print("Tempo total de espera: {}ns".format(10))         
