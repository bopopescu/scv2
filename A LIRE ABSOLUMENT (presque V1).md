# Ce 13 Mai 2017 (C) Jady
# A lire attentivement 




## Dossiers et fichiers indispensables POUR CETTE VERSION: (tout est dans versionJ.zip)

### scv2/flaskApp/flaskApp/scv2_ORM/insertvalues_scv2.py
### scv2/flaskApp/flaskApp/scv2_ORM/rqst_fun_scv2.py
### scv2/flaskApp/flaskApp/scv2_ORM/tests_base_scv2.py
### scv2/flaskApp/flaskApp/scv2_ORM/base_model_scv2.py
### scv2/flaskApp/flaskApp/main_server.py
### scv2/flaskApp/flaskApp/templates/layout.html
### scv2/flaskApp/flaskApp/templates/pages/home.html
### scv2/flaskApp/flaskApp/templates/pages/pres_item.html
### scv2/flaskApp/flaskApp/templates/pages/all_items.html
### scv2/flaskApp/flaskApp/templates/pages/requested_list.html
### scv2/flaskApp/flaskApp/static/*



## Tuto pour que cette V1 marche bien

### Allez dans votre répertoire scv2. Faites un git pull (sauvegardez vos fichiers autre part si jamais!)

. Si le pull fait erreur, vous pouvez faire git stash et refaire git pull
. ATTENTION: veillez à bien enregistrer vos changements dans d'autres dossiers si jamais...
. Si vous téléchargez VERSION1.zip, tout l'architecture est déjà respectée et il n'y aura pas de fichiers inutiles

### Lancer: python3 scv2/flaskApp/flaskApp/scv2_ORM/insert_values.py (version de Arno)
### Lancer: python3 scv2/flaskApp/flaskApp/scv2_ORM/tests_base_scv2.py

. Si la BDD est créée, il n'y aura pas de probleme normalement. Que des affichages.
. S'il y a problème, contactez Arno ou Jady.

### Lancer: python3 scv2/flaskApp/flaskApp/main_server.py
### Allez sur votre navigateur, sur http://127.0.0.1:5000
### Testez les caractéristiques ci-dessous de cette version



## Caratéristiques:

### Accueil, lié au fichier scv2/flaskApp/flaskApp/pages/home.html. Encore à modifier, le site doit être en anglais
### Barres fixes: liste d'items (à gauche) et login (en haut à droite, redirection encore à faire)

. tous types confondus (alphabétique, récent, populaire, mieux noté)
. pour un type particulier (alphabétique, récent, populaire, mieux noté)
### Redirections: URL Mapping




## A faire:

### Recherche par mot-clé
### Login (déjà prêt mais à intégrer, Thomas dis-moi quand tu peux)
### Fiche d'un item
### Fiche d'un participant
### Espace personnel
### Possibilité de noter par les étoiles
### Diverses redirections:

. si /<itemtype.item_type_id> alors /<itemtype.type_name>/All
. si /<itemtype.item_type_id>/<item.title> n'existe plus alors /home
. ...



# NB:Modules indispensables:

### mysql
### flask
### flask-sqlAlchemy
### mysql-connector
### bootstrap
### jinja
### ...
