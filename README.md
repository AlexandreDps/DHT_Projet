DESCOMPS Alexandre  
FASKA Rachid

# Projet DHT

Le but de ce projet est de réaliser et implémenter une DHT.

# Mode d'emploi

Pour lancer la construction et la simulation de la DHT, il suffit d'exécuter le fichier _dht.py_  
Le fichier _graphic.py_ contient le code permettant de traçer l'anneau représentant la DHT

## Étape 1

Tout d’abord, nous avons créés une classe Node pour construire des nœuds avec un identifiant aléatoire et différentes méthodes pour pouvoir gérer les différents nœuds et leurs voisins. Nous avons ensuite fait une classe DHT pour construire la DHT et gérer l’arrivée de nouveaux nœuds et le départ des nœuds. Lorsqu’un nouveau nœud arrive, il contacte un nœud de la DHT de manière aléatoire et se place correctement dans l’anneau de la DHT selon son identifiant.

Voici un exemple de DHT construite :

![image](https://user-images.githubusercontent.com/93133836/228895817-72ad913e-856e-4bea-8408-42fc1f9b6b89.png)

Ensuite, lorsque l'on supprime un nœud, on obtient la DHT suivante :

![image](https://user-images.githubusercontent.com/93133836/228896123-f5d90219-ad3b-492a-b782-0f6bf3654fa8.png)

On voit que c'est le nœud 542 qui a quitté la plateforme (il n'est plus présent en bas à droite de l'anneau) et que ses anciens voisins ont bien été mis en relation.
