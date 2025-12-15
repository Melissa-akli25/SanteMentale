# Commandes à réaliser avant de lancer le projet
mettre dans mysql workbench le script de la BD 
aller dans settings et mettre ses codes de la BD
pip3 install PyMySQL
pip3 install cryptography
python3 manage.py runserver

python manage.py makemigrations mood
python manage.py migrate --fake mood
python manage.py migrate


# commande pour run le projet (a lancer a la racine)
python manage.py runserver 

# installer le connecteur mysql
 
pip install PyMySQL


# ce qu'il reste à faire
Page profile :
- modifier les infos de son profil

 

Page inscription/connexion
- vérifier l'entrée de l'utilisateur lors de la création du compte
- (hasher le mdp)

DONE

Page exercice
- les exercices (lancer un audio au pire)

Page tracking
- insérer en BD les données de tracking
- récupérer les données des 30 derniers jours et les afficher

Page résolutions
- insérer les résolutions en BD
- les modifier en BD
- les supprimer en BD

# EXPLICATION DU FONCTIONNEMENT DE DJANGO
- On va se concentrer principalement sur le dossier mood :
- dans le fichier views.py,on retrouve les fonction qui vont charger les pages qu'on veut
- les pages sont contenues dans templates, c'est celles que l'utilisateur voit à l'écran
- dans models.py, on a les tables de notre base 
- dans urls.py, on retrouve les différentes url, home par exemple, et on peut ordonner de charger une fonction de la vue
qui elle renvoie la page
(voir l.53)

- dans les pages html, on peut mettre des boucles for




