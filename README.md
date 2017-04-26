# TUTO environnement virtuel (venv)

## Les venv c'est la vie :
. On abime pas notre python global (si on fait des bétises on a juste à supprimer l'environnment python et on en refait un autre) 
. On est sûr que **tout le monde** a exactement le même environnement python (version, dépendances, modules complémentaires ...)
. On est sur que le site archera sur tout système  UNIX

## Comment utiliser les venv 
##### Lancement de l'environnement
 \. (un POINT)  [répertoire scv2]/venv/bin/activate
  **ex** : . /home/boss/scv2/venv/bin/activate
  
##### Au sein du venv
. Au début du prompt il y a (venv) , cela indique que toute les commandes python vont s'éxécuter en utilisant les modules du répertoire .../scv2/venv/
. Ensuite il suffit de lancer les programme avec par exemple : **python base.py**
. Les modules pythons complémentaires doivent être installés avec pip3 et si le module était nécessaire, on fait un ***COMMIT DU REPERTOIRE VENV***

##### Quitter le venv
Si vous voulez quittez le venv (quelle idée !), tapez simplement : **deactivate**
# TUTO GIT (MAC et LINUX)

## 1) Initialisation :
1. Créer un dossier  
2.  Dans le dossier, initialiser  git : **git init**  
3.  Puis faire un clone du répertoire git sur le serveur : **git clone https://github.com/oaioa/web_scv2.git**

## 2) Mettre à jour son dossier local avec les modifications des autres
### Toujours faire ça avant de coder !!!
1. Dans le dossier : **git pull**

## 3) Mettre à jour le dossier server suite à ses modifications
1. Ajouter les fichier modifiés : **git add "nom fichier"**  ou si on est sûr que TOUT (!!!) les fichiers doivent être envoyés au serveur **git add \*** 
2. "commit" : préparer son envoi avec un petit message git commit -m **"J'ai fait des trucs de malade"**
3. Enfin envoyer ses modifications sur le serveur : **git push origin master**

# Contributions

J'ai modifié (Jady)2
