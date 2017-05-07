# Installer l'application flaskApp

**Au sein d'un environnement virtuel** (très conseillé : voir le tuto dans le dossier supérieur )

* Dans le dossier flaskApp : 
	***pip install --editable .***
* Assigner variables_globales : 
	***export FLASK_APP=flaskApp*** & ***export FLASK_DEBUG=true***
* De n'importe où :
	***flask run***

# Utiliser notre DB depuis n'importe quel programme python !

Il est enfin possible d'utiliser notre database depuis n'importe quel programme python ! 

#### Une démo est disponible dans le programme de manip

Allez checker **manipbase.py** pour passer direct aux choses sérieuses !


### Pour utiliser la db en python: 

##### l'avoir créée sur votre machine déjà une fois

si elle existe déjà, passez à l'étape 2...
Si ce n'est pas fait, lancer **initbase.py** (DEPENDANCE **tempinsert.py**)
   
##### 1. lancer une engine et un metadata dans son .py

Comme montré dans l'exemple !

	
**exemple** (quand même)
	
	
 ```python
scv2_engine = create_engine('mysql+mysqlconnector://scv2:scv2@localhost/scv2db')

metadata = MetaData(scv2_engine)

```
	

##### 2. utiliser les fonctions pour importer le contexte de la database dans votre programme.

Elles sont contenues dans le module **scv2func.py**, il n'y a plus qu'à les utiliser ! 
	
=> Comment? voir ci-dessous:

Ce que l'on va appeller le **contexte**, c'est ce qui en python contient la **référence à vos tables**.
	
la fonction **importContext()** , est à lancer avec les arguments **engine** et **metadata**.
	
Elle renvoie un **dictionnaire** python contenant les tables, objets SQLalchemy.

	
**exemple** 
	
```python

	context_dic = importContext(engine,metada)
	
	#Pour accéder à la table user, utiliser:
		
	context_dic['user']
	
```
	 
		
	
#### 3. Créer des fonctions qui manipules nos tables dans n'importe quel module .py !

Ainsi, on peut créer des fonctions qui manipulent des tables et font des requêtes sur celles-ci depuis n'importe quel programme.

pour cela, **donner le context_dic à vos fonctions**, **incluez sqlalchemy** dans votre module, et appellez vos **select()**, etc ... 
sur les valeurs du dictionnaire ! :)
	
Un exemple de fonctions est disponible en fin du module scv2func.py
	
Pour les fainéants :
	
**exemple**

```python	
select([context_dic['item'].c.title]).where(and_(
	                                              context_dic['item_type'].c.type_name.like(itemtype),
	                                              context_dic['item'].c.title.like(startswith_letter)
	                                       ))
```	
### Voilà ! 


