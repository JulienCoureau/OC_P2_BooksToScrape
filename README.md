# OC_P2_BooksToScrape
INFORMATIONS GÉNÉRALES
Titre du jeu de données : Scraping de livres depuis Books to Scrape

Date de création : 22/04/2025

Auteur : Julien Coureau

Version : 0.0.1

INFORMATIONS MÉTHODOLOGIQUES
Contexte et objectif
Ce projet a été réalisé dans le cadre d’un exercice (Projet 2 de Openclassroom) visant à automatiser la récupération des prix de livres au moment de l'exécution. Le script permet de scraper les données de livres depuis le site Books to Scrape.​

Méthodes de collecte et de traitement des données
Collecte : Le script télécharge les pages HTML des livres à l'aide de requests, puis les analyse avec BeautifulSoup.

Traitement : Chaque livre est converti en un dictionnaire Python contenant les champs pertinents (titre, prix, etc.).
Tous les dictionnaires sont stockés dans une liste.

Enregistrement : La liste est enregistrée dans un fichier CSV (création et ouverture du fichier avec open(..., 'w')).
Les colonnes sont écrites à l’aide de csv.DictWriter.
Chaque ligne du CSV correspond à un livre.
L'utilisateur peut retrouver le fichier dans le répertoire du script, avec le nom nom_catégorie_books.csv.

NFORMATIONS SPÉCIFIQUES AUX DONNÉES
Liste des variables/entêtes de colonne :
product_page_url : URL de la page du produit

universal_product_code (UPC) : Code universel du produit

title : Titre du livre

price_including_tax : Prix TTC

price_excluding_tax : Prix HT

number_available : Nombre d'exemplaires disponibles

product_description : Description du livre

category : Catégorie du livre

review_rating : Note du livre (sur 5)

image_url : URL de l'image du livre​

Code des valeurs manquantes
Les valeurs manquantes sont indiquées par "Na".​
Recherche Data Gouv

ENVIRONNEMENT D'EXÉCUTION
Langage : Python 3.8+

Bibliothèques nécessaires :

requests

beautifulsoup4​

UTILISATION

Pré-requis : 
Avant de démarrer, assurez-vous d'avoir installé les bibliothèques suivantes : 
- pip install requests
- pip install beautifulsoup4

Installation et démarrage 

1°) Cloner le repository : https://git@github.com:JulienCoureau/OC_P2_BooksToScrape.git
2°) Créer et activer un environnement virtuel
cd OC_P2_BooksToScrape
python -m venv env
source env/bin/activate # mac/linux
env\Scripts\activate # Windows

3°) Installer les dépendances : 
pip install -r requirements.txt

4°) Exécuter le scipt principal : 
python ScrapBooksToScrape.py

Resultats : 

Après exécution : 
    - Un dossier books sera créé automatiquement
    - Chaque catégorie aura son propre sous-dossier
    - Chaque sous dossier contiendra : 
        - Un fichier CSV avec les informations des livres
        - Un dossier images contenant toutes les couvertures des livres

Note 

- Un script vérifie automatiquement qu'il y a bien 50 catégories
- En cas de problème réseau ou de structure du site modifiée, un message d'erreur apparaîtra

