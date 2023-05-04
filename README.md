# WelshAcademy

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)

### Pré-requis

- Python 3.10 (Installer Python 3.10 depuis https://www.python.org/)
- Terminal
- Git
- Postman
- Navigateur


### Installation et exécution de l'application sans pipenv (avec venv et pip)

1. Clonez ce dépôt de code à l'aide de la commande `git clone https://github.com/seah78/WelshAcademy.git`
2. Rendez-vous depuis un terminal dans le répertoire avec la commande `cd WelshAcademy`
3. Créer un environnement virtuel pour le projet avec `python -m venv .venv` sous windows ou `python3 -m venv .venv` sous macos ou linux.
4. Activez l'environnement virtuel avec `env\Scripts\activate` sous windows ou `source env/bin/activate` sous macos ou linux.
5. Installez les dépendances du projet avec la commande `pip install -r requirements.txt`
6. Démarrer le serveur avec `python main.py`

Les étapes 1 à 5 ne sont requises que pour l'installation initiale. Pour les lancements ultérieurs du serveur, il suffit d'exécuter l'étape 6 à partir du répertoire WelshAcademy.


## Documentation de l'API

La documentation de l'API est accessible à cette adresse : https://documenter.getpostman.com/view/19380541/2s93eVXDwz

## Démarrage de l'API

Depuis un navigateur ou depuis Postman saisissez l'adresse http://127.0.0.1:5000/

## Docker

Pour construire l'image Docker, utilisez la commande suivante :
docker buid -t welshacademy .

Pour lancer le conteneur, utilisez la commande suivante :
docker run -d -p 5000:5000 welshacademy

## Fabriqué avec

* Visual Studio Code

## Versions

Version actuelle : v1.0.0
Liste des versions : [Cliquer pour afficher](https://github.com/seah78/WelshAcademy/tags)

## Auteurs

* ** Sébastien HERLANT ** _alias_ [@seah78](https://github.com/seah78)

