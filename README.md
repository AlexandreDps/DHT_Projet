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

![image](https://user-images.githubusercontent.com/93133836/228903789-35caf1f9-328e-4d69-8fad-517f948b9030.png)

Ensuite, lorsque l'on ajoute un nœud, on obtient la DHT suivante :

![Figure 2023-03-30 180239](https://user-images.githubusercontent.com/93133836/228904148-9196ba81-8ad9-4476-ae0d-ed12e18a7321.png)

On voit que le nœud avec l'identifiant 393 a été ajouté et qu'il est bien placé au bon endroit selon la valeur de son identifiant.

Enfin, lorsque l'on supprime un nœud, on obtient la DHT suivante :

![Figure 2023-03-30 183630](https://user-images.githubusercontent.com/93133836/228905066-9d23cde3-8737-4c3a-91c3-97e46806b752.png)

On voit que c'est le nœud 534 qui a quitté la plateforme (cercle rouge) et que ses anciens voisins ont bien été mis en relation.
