# Ce 13 Mai 2017 (C) Jady - A lire attentivement 

# Dossiers et fichiers indispensables POUR CETTE VERSION: (tout est rangé dans VERSION1.zip)

    scv2/flaskApp/flaskApp/main_server.py
    scv2/flaskApp/flaskApp/flask_user/*
    scv2/flaskApp/flaskApp/scv2_ORM/insert_values_scv2.py
    scv2/flaskApp/flaskApp/scv2_ORM/rqst_func_scv2.py
    scv2/flaskApp/flaskApp/scv2_ORM/tests_base_scv2.py
    scv2/flaskApp/flaskApp/scv2_ORM/base_model_scv2.py
    scv2/flaskApp/flaskApp/templates/layout.html
    scv2/flaskApp/flaskApp/templates/img/inscale_logo.png
    scv2/flaskApp/flaskApp/templates/pages/error.html
    scv2/flaskApp/flaskApp/templates/pages/home.html
    scv2/flaskApp/flaskApp/templates/pages/roles.html
    scv2/flaskApp/flaskApp/templates/pages/pres_item.html
    scv2/flaskApp/flaskApp/templates/pages/all_items.html
    scv2/flaskApp/flaskApp/templates/pages/requested_list.html
    scv2/flaskApp/flaskApp/templates/pages/search_results.html
    scv2/flaskApp/flaskApp/static/*

# Tuto pour que cette V1 marche bien

  ### 1. Allez dans votre répertoire scv2. Faites un git pull (sauvegardez vos fichiers autre part si jamais!)
    • Si le pull fait erreur, vous pouvez faire git stash et refaire git pull
    • ATTENTION: veillez à bien enregistrer vos changements dans d'autres dossiers si jamais...
    • Si vous téléchargez VERSION1.zip, toute l'architecture est déjà respectée et il n'y aura pas de fichiers inutiles

  ### 2. Lancer: python3 scv2/flaskApp/flaskApp/scv2_ORM/insert_values.py (version de Arno)
  ### 3. Lancer: python3 scv2/flaskApp/flaskApp/scv2_ORM/tests_base_scv2.py
    • Si la BDD est créée, il n'y aura pas de probleme normalement. Que des affichages.
    • S'il y a problème, contactez Arno ou Jady.

  ### 4. Lancer: python3 scv2/flaskApp/flaskApp/main_server.py
  ### 5. Allez sur votre navigateur, sur http://127.0.0.1:5000
  ### 6. Testez les caractéristiques ci-dessous de cette version



# Caratéristiques:

  ### . Accueil, lié au fichier scv2/flaskApp/flaskApp/pages/home.html. Encore à modifier, le site doit être en anglais
  ### . Barres fixes: liste d'items (à gauche) et login (en haut à droite, redirection encore à faire)
    • tous types confondus (alphabétique, récent, populaire, mieux noté)
    • pour un type particulier (alphabétique, récent, populaire, mieux noté)
  ### . Redirections: URL Mapping




# A faire:
  ### . Mettre le logo de Inscale sur la barre d'en haut (probleme de chargement...)
  ok ### . Mettre tout ce qui est en commun aux html dans le layout (barres laterales sous forme de block)
  ### . Login (déjà prêt mais à intégrer, Thomas dis-moi quand tu peux)
  ### . Most famous DOIT ETRE DIFFERENT de Most recent (users donc login à mettre en place)
  ### . Scrollbar sur le sidebar des différents item types quand sur ordi la liste est trop longue (et donc on voit pas le bas) -> Paul?
  ok ### . Recherche par mot-clé
  ### . Intégrer le nom du rôle (dans participation) pour la recherche par mot clé
  ok ### . Redirection à partir des résultats de recherche
  ### . Changer l'icône de musique sur les item types (quel css?)
  ### . Garder l barre en haut sur une les plateformes plus petites
  ### . Fiche d'un item avec le template d'harry potter
  ### . Désactiver le menu déroulé après une certaine taille de fenêtre (quel css?)
  ok ### . trois colonnes pour toute liste (css de panel-body)
  ok ### . Afficher le type en string et non en id!
  ok ### . Ajouter les roles pour chaque item type (déroulé)
  ok ### . Rediriger à la liste des participants à un rôle d'un type (requested list)
  ### . Trier les résultats de la recherche: alphabétique, mieux notés, plus notés et plus récents
  ### . Items commençant par...
  ### . garder la barre du dessus même avec une fenêtre petite
  NON ### . Pagination : 1 page = 50 items (pour les recherches)
  ### . Liste des rôles possibles à chaque type d'item (dans le menu déroulant à gauche)
  ### . Fiche d'un participant (la liste des items auxquels il a joué un rôle)
  ### . Espace personnel : photo, biographie, mes notes sur les items, mes intérêts
  ### . Possibilité de noter par les étoiles
  ok ### . Traduire tout le site en anglais
  ### . Rendre responsive (profile -> login ET texte d'accueil)
  ### . Diverses redirections (à compléter!):
    ok• si /<itemtype.item_type_id> alors /<itemtype.type_name>/All
    ok• si /<itemtype.item_type_id>/<item.title> n'existe plus alors /error
    • ...



# NB:Modules indispensables:

    mysql
    flask
    flask-sqlAlchemy
    mysql-connector (cf tuto sur git)
    bootstrap
    jinja
    flask_user
    wtforms_alchemy
    pycrypto (sudo yum install python3-crypto)

    ...
