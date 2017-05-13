# Ce 13 Mai 2017 (C) Jady - A lire attentivement 

# Dossiers et fichiers indispensables POUR CETTE VERSION: (tout est rangé dans VERSION1.zip)

    scv2/flaskApp/flaskApp/scv2_ORM/insertvalues_scv2.py
    scv2/flaskApp/flaskApp/scv2_ORM/rqst_fun_scv2.py
    scv2/flaskApp/flaskApp/scv2_ORM/tests_base_scv2.py
    scv2/flaskApp/flaskApp/scv2_ORM/base_model_scv2.py
    scv2/flaskApp/flaskApp/main_server.py
    scv2/flaskApp/flaskApp/templates/layout.html
    scv2/flaskApp/flaskApp/templates/pages/home.html
    scv2/flaskApp/flaskApp/templates/pages/pres_item.html
    scv2/flaskApp/flaskApp/templates/pages/all_items.html
    scv2/flaskApp/flaskApp/templates/pages/requested_list.html
    scv2/flaskApp/flaskApp/static/*

# Tuto pour que cette V1 marche bien

  ### 1. Allez dans votre répertoire scv2. Faites un git pull (sauvegardez vos fichiers autre part si jamais!)
    • Si le pull fait erreur, vous pouvez faire git stash et refaire git pull
    • ATTENTION: veillez à bien enregistrer vos changements dans d'autres dossiers si jamais...
    • Si vous téléchargez VERSION1.zip, tout l'architecture est déjà respectée et il n'y aura pas de fichiers inutiles

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

  ### . Recherche par mot-clé
  ### . Login (déjà prêt mais à intégrer, Thomas dis-moi quand tu peux)
  ### . Fiche d'un item
  ### . Liste des rôles possibles à chaque type d'item (dans le menu déroulant à gauche)
  ### . Fiche d'un participant (la liste des items auxquels il a joué un rôle)
  ### . Espace personnel : photo, biographie, mes notes sur les items, mes intérêts
  ### . Possibilité de noter par les étoiles
  ### . Diverses redirections (à compléter!):
    • si /<itemtype.item_type_id> alors /<itemtype.type_name>/All
    • si /<itemtype.item_type_id>/<item.title> n'existe plus alors /home
    • ...



# NB:Modules indispensables:

    mysql
    flask
    flask-sqlAlchemy
    mysql-connector
    bootstrap
    jinja
    ...
