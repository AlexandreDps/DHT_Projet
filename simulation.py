# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 01:01:19 2023

@author: Alexandre
"""
import simpy
import random
import dht
import simpy.rt
import graphic
import time

#Paramètres représentant le nombre moyen d'occurences par unité de temps (loi exponentielle)
TEMPS_SIMULATION = 20 #secondes
MOYENNE_JOIN = 0.6
MOYENNE_LEAVE = 0.2
MOYENNE_MESSAGE = 0.2
MOYENNE_DATA = 0.3
MOYENNE_MORT = 0.3

class Simulation:
    def __init__(self):
        self.env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1.0, strict=True)
        self.dht = dht.DHT()
        
    def join(self):
        while True:
            yield self.env.timeout(random.expovariate(MOYENNE_JOIN))
            self.dht.add_node()
    
    def leave(self):
        while True:
            yield self.env.timeout(random.expovariate(MOYENNE_LEAVE))
            #Car on souhaite garder au moins 3noeuds dans la dht et un noeud peut quitter en meme temps qu'un noeud meurt donc on garde une petite marge
            if len(self.dht.nodes) >5 : 
                node_to_remove = random.choice(list(self.dht.nodes.keys()))
                self.dht.remove_node(node_to_remove)
                
    def send_message(self):
        while True:
            yield self.env.timeout(random.expovariate(MOYENNE_MESSAGE))
            if len(self.dht.nodes) > 2 :
                nodes_aleatoire = random.sample(list(self.dht.nodes.keys()), k=2)
                message_aleatoire = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
                nodes_aleatoire[0].new_message(nodes_aleatoire[1],message_aleatoire)
    def add_data(self):
        while True:
            yield self.env.timeout(random.expovariate(MOYENNE_DATA))
            dht.Data(dht=self.dht)
            
    def die_node(self):
        while True:
            yield self.env.timeout(random.expovariate(MOYENNE_DATA))
            if len(self.dht.nodes) > 5 :
                alea_node = random.choice(list(self.dht.nodes.keys()))
                self.dht.die(alea_node)
        
    def run(self, runtime):
        self.env.process(self.join())
        self.env.process(self.leave())
        self.env.process(self.send_message())
        self.env.process(self.add_data())
        self.env.process(self.die_node())
        self.env.run(until=runtime)

        
simulation = Simulation()
simulation.run(TEMPS_SIMULATION)

time.sleep(5) #Temps nécessaire pour que les noeuds enlevent les derniers morts
#Graphique finale de la dht
print("[FIN DE LA SIMULATION] Affichage de la dht finale")
graphic.show_graph(list(simulation.dht.nodes.keys())[0],len(simulation.dht.nodes))
