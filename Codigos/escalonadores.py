# -*- coding: utf-8 -*-
import operator
import processo
class Escalonadores(object):

    lista_espera = []   # lista de espera da execucao
    ordem = []  #ordem de execucao
    tempos = {"execucao" : 0, "espera" : 0}
    lista_prontos = [] # lista de prontos para round robin

    def __init__(self, processos):
        self.processos = processos
    def ordenar(self):
        pass
    def executar(self, processo):
        pass

    


#class RR(Escalonadores):   
#    def __init__(self, processos):
#        super(SJF,self).__init__(processos) #herança da classe pai
#	def ordenar(self):
#        self.ordem = sorted(self.processos, key = operator.attrgetter("tamanho")) #ordena por tamanho  
#         visualizar ordenação print(self.ordem)
#    def __str__(self):  #função de print de um objeto
#        return "\n" + str(self.__dict__) 
#    def __repr__(self): #função de print de uma lista de objetos
#        return str(self) + "\n"    
#    def executar(self): #função principal, executa os processos na ordem RR 

#    tempo_total = 0 
#        for i in range(len(self.ordem)): 
#        	tempo_total = tempo_total + self.ordem[i].tamanho 
#        for i in range(tempo_total): 
        	

#class PRIORIDADE(Escalonadores): 


class SJF(Escalonadores):  
  
    def __init__(self, processos):
        super(SJF,self).__init__(processos) #herança da classe pai

    def ordenar(self):
        self.ordem = sorted(self.processos, key = operator.attrgetter("tamanho")) #ordena por tamanho  

    def __str__(self):  #função de print de um objeto
        return "\n" + str(self.__dict__) 

    def __repr__(self): #função de print de uma lista de objetos
        return str(self) + "\n"    

    # def executar(self): #função principal, executa os processos na ordem SJF
    #  	self.ordenar()
    #     for i in range(len(self.ordem)):
    #         if self.tempos["execucao"] < self.ordem[i].tempos["chegada"]:   #verifica se não tinha outro processo executando
    #             dif = self.ordem[i].tempos["chegada"] - self.tempos["execucao"] #
    #             self.tempos["espera"] = self.tempos["espera"] + dif             #Se nao tinha outro processo executando, adiciona ao tempo de espera, o tempo em que o programa está ocioso
    #             self.tempos["execucao"] = self.ordem[i].tempos["chegada"]       #
    #         self.ordem[i].estado = "executando" #seta o estado do precesso como executando 
    #         self.ordem[i].tempos["inicio"] = self.tempos["execucao"]    #seta o tempo de inicio de execucao do processo 
    #         if self.ordem[i].tempos["chegada"] < self.tempos["execucao"]:   #verifica se ele esperou pra ser executado
    #             dif = self.tempos["execucao"] - self.ordem[i].tempos["chegada"]
    #             self.tempos["espera"] = self.tempos["espera"] + dif    
    #         print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+self.ordem[i].tamanho), self.ordem[i].id))
    #         self.tempos["execucao"] = self.tempos["execucao"] + self.ordem[i].tamanho  
    #         self.ordem[i].estado = "terminado"  #seta o estado do processo como terminado 
    #         for j in range(len(self.ordem[i].eventos)): #execucao dos I/O
    #             self.exec_IO(self.ordem[i].eventos[j])
    #             print("Evento de IO do processo {} do tempo {} executado no tempo {}".format(self.ordem[i].id,self.ordem[i].eventos[j],self.ordem[i].eventos[j])) 
    #             #self.tempos["execucao"]))
    #     print("\nTempo total de execução: {}ns".format(self.tempos["execucao"]))
    #     print("Tempo total de espera: {}ns".format(self.tempos["espera"]))
    #     print("Tempo médio de espera: {}ns".format((float(self.tempos["espera"]) / float(len(self.ordem)))))  

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
        while self.tempos["execucao"] < processo.tempos["chegada"]:
            self.tempos["execucao"] = self.tempos["execucao"] + 1 
            self.tempos["espera"] = self.tempos["espera"] + 1 

    def executar_proc(self, processo): 
        while processo.tempos["executado"] < processo.tamanho:   #nao premptivo, nao pode ser parado ate que termine
            self.tempos["execucao"] = self.tempos["execucao"] + 1
            processo.tempos["executado"] = processo.tempos["executado"] + 1

    def bloqueiaProcIO(self, processo):
        self.lista_prontos.remove(processo)
        self.lista_espera.append(processo)

    def executar(self): #função principal, executa os processos na ordem fifo
        self.ordenar()
        for i in range(len(self.ordem)):
            if self.ordem[i].tipo == processo.USUARIO:
                self.esperar(self.ordem[i])
                self.lista_prontos.append(self.ordem[i])
                self.executar_proc(self.ordem[i])
                if len(self.ordem[i].eventos):
                    self.bloqueiaProcIO(self.ordem[i])
                else:
                    self.lista_prontos.remove(self.ordem[i])
            else:
                self.lista_prontos = self.ordem[i].exec_IO(self.lista_espera,self.tempos["execucao"])
                self.lista_prontos = []

        print("\nTempo total de execução: {}ns".format(self.tempos["execucao"]))
        print("Tempo total de espera: {}ns".format(self.tempos["espera"]))
        print("Tempo médio de espera: {}ns".format((float(self.tempos["espera"]) / float(len(self.ordem)))))
'''
como o algoritmo é não premptivo,
posso afirmar que todos os processos foram exucutado
por completo, sendo assim, não é necessario verificar
se todos os processos foram executados até o final
'''



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
            
        #     print("{} - {} # Processo {}".format(self.tempos["execucao"], (self.tempos["execucao"]+self.ordem[i].tamanho), self.ordem[i].id))
        #     self.tempos["execucao"] =self.tempos["execucao"] + self.ordem[i].tamanho 
        #     self.ordem[i].estado = "terminado"  #seta o estado do processo como terminado
        #     for j in range(len(self.ordem[i].eventos)): #execucao dos I/O
        #         self.exec_IO(self.ordem[i].eventos[j])
        #         print("Evento de IO do processo {} do tempo {} executado no tempo {}".format(self.ordem[i].id,self.ordem[i].eventos[j],self.tempos["execucao"]))