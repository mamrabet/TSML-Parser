# But du programme

L'intérêt est de parser un fichier texte contenant un automate sous la syntaxe TSML, de réaliser son produit synchronisé et de vérifier certaines propriétés (ici les deadlocks uniquement).

# Utilisation

La version 3.4.2 de Python a été utilisée durant le développement du programme (fichier .python-version inclus). Il vous est donc conseillé d'utiliser cette même version.

Dans un terminal, il est possible de lancer une exécution à l'aide de la commande :

`python ./model_checker.py`

Ce fichier Python est assez court et lisible et vous permettra, si vous l'éditez, de choisir un autre automate ou de sauter des étapes comme la recherche de deadlocks par exemple.
