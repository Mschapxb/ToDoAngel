
# ToDoAngel

Bienvenue sur le repository de ToDoAngel, une application de gestion de tâches simple et efficace. Ce projet est écrit en Python et est dockerisé pour faciliter le déploiement et l'exécution.

## Caractéristiques

ToDoAngel permet aux utilisateurs de :

- Ajouter de nouvelles tâches à faire.
- Visualiser la liste des tâches en cours.
- Marquer les tâches comme terminées ou les supprimer.

## Prérequis

Pour utiliser ce projet, vous aurez besoin de Docker et Docker Compose installés sur votre machine. Consultez [la documentation Docker](https://docs.docker.com/get-docker/) pour des instructions sur l'installation de Docker.

## Installation et démarrage

Pour démarrer l'application, suivez les étapes ci-dessous :

1. Clonez ce repository sur votre machine locale :
   ```
   git clone https://github.com/Mschapxb/ToDoAngel.git
   cd ToDoAngel
   ```

2. Construisez et lancez le conteneur Docker avec Docker Compose :
   ```
   docker-compose up --build -d
   ```

   Cette commande construira l'image Docker nécessaire et démarrera un conteneur en arrière-plan.

3. Une fois le conteneur en cours d'exécution, accédez à l'application via `http://localhost` dans votre navigateur.

