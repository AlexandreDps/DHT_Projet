_DESCOMPS Alexandre_  
_FASKA Rachid_

# Projet DHT

Le but de ce projet est de réaliser et implémenter une DHT.

# Mode d'emploi

Pour lancer la construction et la simulation de la DHT, il suffit d'exécuter le fichier _dht.py_  
Le fichier _graphic.py_ contient le code permettant de traçer l'anneau représentant la DHT

# Construction de la DHT

## Étape 1 : Join and Leave

Tout d’abord, nous avons créés une classe Node pour construire des nœuds avec un identifiant aléatoire et différentes méthodes pour pouvoir gérer les différents nœuds et leurs voisins. Nous avons ensuite fait une classe DHT pour construire la DHT et gérer l’arrivée de nouveaux nœuds et le départ des nœuds. Lorsqu’un nouveau nœud arrive, il contacte un nœud de la DHT de manière aléatoire et se place correctement dans l’anneau de la DHT selon son identifiant.

Voici un exemple de DHT construite :

![image](https://user-images.githubusercontent.com/93133836/228913541-aa210dee-c0d1-4a70-8fcd-fb1d3501cbcc.png)

Ensuite, lorsque l'on ajoute un nœud, on obtient la DHT suivante :

![Figure 2023-03-30 180239](https://user-images.githubusercontent.com/93133836/228913966-f2e695d7-b48a-4b61-aa22-1ba5ffe83392.png)

On voit que le nœud avec l'identifiant 399 a rejoint la plateforme et qu'il est bien placé au bon endroit selon la valeur de son identifiant.

Enfin, lorsque l'on supprime un nœud, on obtient la DHT suivante :

![Figure 2023-03-30 183630](https://user-images.githubusercontent.com/93133836/228914323-13c7c771-967d-4494-8537-5e7c6187b746.png)

On voit que c'est le nœud 984 qui a quitté la plateforme (zone rouge) et que ses anciens voisins ont bien été mis en relation.

En effet, lorsqu’un nœud quitte la plateforme, ses voisins doivent le remarquer.  
Pour cela, on a une méthode _check_alive_ qui permet à chaque nœud de vérifier toutes les 5 secondes si ses voisins sont encore présents grâce à l’attribut _is_alive_ de chaque nœud et en utilisant des threads.  
Voici le résultat affiché lorsque le nœud 984 a quitté la plateforme :

![image](https://user-images.githubusercontent.com/93133836/228972990-a095e575-a5e7-421e-a577-91df485bc32f.png)

Les nœuds 951 et 64 ont bien remarqué que leur voisin, le nœud 984 avait quitté la DHT.

## Étape 2 : Routing (Send and Deliver)

Maintenant que les nœuds ont été construits, ils peuvent s’envoyer des messages.  
Pour ce faire, nous avons créé une classe _Message_ contenant le nœud expéditeur, le nœud destinataire et le contenu du message. Nous avons ensuite ajouté les méthodes _new_message_ et _send_message_ à la classe _Node_ permettant de créer et d’envoyer un message.  
Par exemple, disons que le nœud 355 veut envoyer le message « salut » au nœud 182 :

<img src="https://user-images.githubusercontent.com/93133836/228915077-c82ae4f9-8a79-498d-b408-b76fe24acfc2.png" width="400" height="100">

On voit que le message doit d’abord passer par 3 autres nœuds avant d’atteindre le nœud 182.

## Étape 3 : Storage (Put and Get)

Cette étape va permettre aux nœuds de stocker des données.  
Nous avons alors ajouté une classe _Data_ avec le contenu de la donnée et la DHT à laquelle la donnée est rattaché ainsi qu’un identifiant qui prend une valeur de manière aléatoire.  
Cette classe permet également d’identifier le nœud qui a l’identifiant le plus proche de celui de la nouvelle donnée.  
On a aussi ajouté un nouvel attribut _data_storage_ à la classe _Node_ permettant à chaque nœud de stocker de la donnée. La nouvelle méthode _get_data_ de la classe _Node_ va alors permettre d’ajouter la donnée au nœud le plus proche ainsi qu’à ses deux voisins immédiats.

Voici un exemple d’ajout de deux données dans la DHT :

```python
d1 = Data(dht=dht1, contenu='Test1')
d2 = Data(dht=dht1, contenu='Test2')
```
Résultat obtenu :

<img src="https://user-images.githubusercontent.com/93133836/228916073-b25b5464-6f4c-4726-9561-4f26d5ec3d42.png" width="650" height="40">

On voit qu’une donnée a été créée avec l’identifiant 922 et a été correctement associée au nœud le plus proche qui est le nœud 908. On peut faire le même constat pour la donnée d’identifiant 492.

## Étape 4 : Advanced routing

Nous devons maintenant chercher une méthode de routage plus performante.  
Notre méthode se base sur la construction d’une table de routage pour chaque nœud.  
Lorsqu’un chemin est parcouru, on ajoute des infos dans le message pour que la donnée reste en mémoire de chacun des nœuds et les nœuds ayant participé au transfert du message peuvent faire des liens longs directement.

Voici un exemple :

![image](https://user-images.githubusercontent.com/93133836/228974321-450d0f3e-d891-45b7-997d-cef4f6d81237.png)

![image](https://user-images.githubusercontent.com/93133836/228974366-52c3de1f-d40e-4104-a14c-6c062442b0dc.png)

Avant que le nœud 984 ne quitte la plateforme, il a d'abord envoyé un message au nœud 679 et le nœud 951 a partcipé au transfert de ce message.  
Puis, lors de l'envoi d'un nouveau message au nœud 355, un lien long a été trouvé entre le nœud 984 et le nœud 951 car encore une fois le nœud 951 participe au transfert du nouveau message.
