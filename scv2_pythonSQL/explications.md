Il est enfin possible d'utiliser notre database depuis n'importe quel programme python ! 

Une démo est disponible dans le programme "manipbase.py" !


Pour utiliser la db en python: 

1) l'avoir créée sur votre machine déjà une fois (si elle existe déjà, passez à l'étape 2).
   Si ce n'est pas fait, lancer "initbase.py" (DEPENDANCE "tempinsert.py")
   
2) lancer une engine et un metadata comme montré dans l'exemple.

3) utiliser les fonctions contenues dans le module "scv2func.py" pour importer le contexte de la database dans votre programme.
	
	Comment? voir ci-dessous:

	Ce que l'on va appeller le contexte, c'est ce qui en python contient la référence à vos tables.
	
	la fonction importContext() , est à lancer avec les arguments engine et metadata.
	
	Elle renvoie un dictionnaire python contenant les tables.
	
	ex : context_dic = importContext(engine,metada)
	
	Pour accéder à la table user, utiliser context_dico['user'], etc ... 
	
	
	
4) Ainsi, on peut créer des fonctions qui manipulent des tables et font des requêtes sur celles-ci depuis n'importe quel programme.

	pour cela, donner le context_dic à vos fonctions, incluez sqlalchemy dans votre module, et appellez vos select(), etc ... 
	sur les valeurs du dictionnaire ! :)
	
	Un exemple de fonctions est disponible en fin du module scv2func.py


