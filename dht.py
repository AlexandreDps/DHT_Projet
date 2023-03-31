# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:11:59 2023

@author: Alexandre
"""
#Noeuds augmentent dans le sens trigo (voisin de droite plus grand)

import graphic

import random
from threading import Thread
import time
from matplotlib import pyplot as plt

DEGRE_REPLICATION = 3
TIMING_CHECK_IF_ALIVE = 5 #secondes
RUN_WITH_THREAD = True #Active ou désactive le check alive

class Node():
    def __init__(self):
        #Identifiant aléatoire
        self.identifiant=random.randint(0, 1000)
        self.v_gauche=self
        self.v_droite=self
        self.data_storage = []
        self.table_routage = {}
        self.is_alive = True
        #Lance une thread pour chaque noeud
        if RUN_WITH_THREAD:
            node_thread = Thread(target=self.check_alive)
            node_thread.start()
    def set_v_gauche(self,node):
        self.v_gauche = node
    def set_v_droite(self,node):
        self.v_droite = node
    def new_message(self,destinataire,contenu):
        path={}
        path[self]=self.identifiant
        m1 = Message(envoyeur=self,destinataire=destinataire,contenu=contenu)
        print(f'Message envoyé par le noeud {self.identifiant} à destination de {destinataire.identifiant}')
        #Recherche d'un lien long
        noeud_proche = None
        mindiff = None
        for key, value in self.table_routage.items():
            diff = abs(destinataire.identifiant - value)
            if mindiff is None or diff < mindiff:
                noeud_proche = key
                mindiff = diff
        if noeud_proche != None and noeud_proche != self:
            print(f'[+] Un lien long a été trouvé ! {self.identifiant} ====> {noeud_proche.identifiant}')
            noeud_proche.send_message(m1,path)
        else :
            self.send_message(m1,path)
    def send_message(self,message,path):
        #Prends en compte le sens
        if message.destinataire == self:
            self.table_routage.update(path)
            print(f'Message reçu par le noeud {self.identifiant} : {message.contenu}')
        else:
            nextnode = next_node(message.sens, self)
            print(f'{self.identifiant} ==> {nextnode.identifiant}')
            #Ajout du chemin en mémoire
            path[nextnode] = nextnode.identifiant
            self.table_routage.update(path) #Evite les doublons
            nextnode.send_message(message,path)
    def get_data(self,data):
        #Quand un noeud reçoit de la data, il la transmet à ses 3voisins de droite et gauche les + proches
        self.data_storage.append(data)
        ng = self.v_gauche
        nd = self.v_droite
        for i in range(DEGRE_REPLICATION-1):
            ng.data_storage.append(data)
            nd.data_storage.append(data)
            ng = ng.v_gauche
            nd = nd.v_droite
    def check_alive(self):
        while self.is_alive: #La thread meurt en meme temps que le noeud
            #Check si ses voisins sont encore en vie toutes les 5secondes
            time.sleep(TIMING_CHECK_IF_ALIVE)
            if self.v_droite.is_alive == False :
                print(f'[*] {self.identifiant} à remarqué que son voisin {self.v_droite.identifiant} était mort. Il fera le necessaire.\n')
                self.set_v_droite(self.v_droite.v_droite)
            if self.v_gauche.is_alive == False :
                print(f'[*] {self.identifiant} pleure déjà la perte de son camarade {self.v_gauche.identifiant}.\n')
                self.set_v_gauche(self.v_gauche.v_gauche)
        
class Message():
    def __init__(self,**kwargs):
        self.envoyeur = kwargs.get('envoyeur',None)
        self.destinataire = kwargs.get('destinataire',None)
        self.contenu = kwargs.get('contenu',None)
        if self.envoyeur.identifiant < self.destinataire.identifiant:
            self.sens=1
        else :
            self.sens=-1
        
class Data():
    def __init__(self,**kwargs):
        self.identifiant=random.randint(0, 1000)
        self.contenu = kwargs.get("contenu")
        self.dht = kwargs.get('dht')
        #Choix aléatoire d'un premier noeud dans la liste 
        compared_node = random.choice(list(self.dht.nodes.keys()))
        if self.identifiant < compared_node.identifiant :
            sens = -1
        else :
            sens = 1
        while abs(self.identifiant - next_node(sens,compared_node).identifiant) < abs(self.identifiant-compared_node.identifiant):
            compared_node = next_node(sens,compared_node)
        compared_node.get_data(self)
        print(f"[+] La donnée {self.identifiant} à été transmise au noeud {compared_node.identifiant} et ses {DEGRE_REPLICATION} voisins de droite et gauche les plus proches")
    
    
    
class DHT():
    def __init__(self):
        #Initialisation de la DHT avec un seul noeud
        N0 = Node()
        self.nodes = {N0:N0.identifiant}
            
    def add_node(self):
        new_node = Node()
        EXTREMUM = False
        #Check si l'identifiant du noeud existe déjà
        while new_node.identifiant in list(self.nodes.values()) :
            new_node = Node()
        #Choix aléatoire d'un premier noeud dans la liste 
        compared_node = random.choice(list(self.nodes.keys()))
        #Definition du sens de recherche
        if new_node.identifiant<compared_node.identifiant: sens = -1
        else : sens=1
            
        while new_node.identifiant*sens > compared_node.identifiant*sens:
            if compared_node.identifiant*sens < next_node(sens,compared_node).identifiant*sens:
                compared_node=next_node(sens,compared_node)
            else :
                EXTREMUM = True
                break
        if (sens==1 and not(EXTREMUM) or (sens==-1 and EXTREMUM)) :
            #Le nouveau noeud est plus faible que le noeud comparé
            new_node.set_v_droite(compared_node)
            new_node.set_v_gauche(compared_node.v_gauche)
            compared_node.v_gauche.set_v_droite(new_node)
            compared_node.set_v_gauche(new_node)
        else :
            #Le nouveau noeud est plus gros que le noeud comparé
            new_node.set_v_droite(compared_node.v_droite)
            new_node.set_v_gauche(compared_node)
            compared_node.v_droite.set_v_gauche(new_node)
            compared_node.set_v_droite(new_node)
                
        self.nodes[new_node]=new_node.identifiant
        print(f'[+] Le noeud {new_node.identifiant} a rejoins la DHT.')
        
    def remove_node(self,node):
        node.v_gauche.set_v_droite(node.v_droite)
        node.v_droite.set_v_gauche(node.v_gauche)
        print(f'[-] Le noeud {node.identifiant} a quitté la DHT.')
        del self.nodes[node]
        
    def die(self,node):
        node.is_alive = False
        del self.nodes[node]
        print(f'[--] Oh non ! Le regretté noeud {node.identifiant} est mort :(')
        
def next_node(sens,node):
    if sens==1:
        #Retourne le node plus gros
        return node.v_droite
    else:
        return node.v_gauche
    
    
'''    
dht1 = DHT()

#Test ajout de noeud
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()
dht1.add_node()

print('\n')
#Test suppression de noeud 
dht1.remove_node(list(dht1.nodes.keys())[0])


fig1 = plt.figure()
graphic.show_graph(list(dht1.nodes.keys())[0],len(dht1.nodes))
print('\n')

#Envoi de messages
node1 = list(dht1.nodes.keys())[3]
node2 = list(dht1.nodes.keys())[5]
node1.new_message(node2,'salut')

print('\n')
#Ajout de données dans la dht
d1 = Data(dht=dht1, contenu='Test1')
d2 = Data(dht=dht1, contenu='Test2')
   
#Une fois que notre chemin à été parcouru, il reste en mémoire et nos noeuds ayant participé au chemin peuvent
#faire des liens longs
print('\n') 
node2.new_message(node1,'ça va?')
node1.new_message(node2,'bien et toi ?') 
node3 = list(dht1.nodes.keys())[4]
node4 = list(dht1.nodes.keys())[6]    
node3.new_message(node4,'Si t es passé par moi la première fois, je trouverai peut etre un lien long !')   
node3.new_message(node1,'Si t es passé par moi la première fois, je trouverai forcément un lien long !')  
    
print('\n') 
#Mort d'un noeud
dht1.die(node1)
dht1.die(node3)
#Un noeud meurt spontanément -> les voisins doivent le remarquer 
time.sleep(TIMING_CHECK_IF_ALIVE+1)
fig2 = plt.figure()
graphic.show_graph(list(dht1.nodes.keys())[0],len(dht1.nodes))
    
'''   