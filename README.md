# OC_P2_BooksToScrape
INFORMATIONS GÉNÉRALES
Titre du jeu de données : Scraping de livres depuis Books to Scrape

Date de création : 22/04/2025

Auteur : Julien Coureau

Version : Python 3.12.7

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
1°) Ouvrir le fichier Scrap BooksToScrape.py

2°) Modifier la ligne suivante pour choisir une des catégories disponibles :​
test_category = "sports"  # ou "science", "travel"
scrape_category(test_category)

3°) Exécuter le script : Scrap BooksToScrape.py

4°) Une fois exécuté :

Un fichier CSV nommé sports_books.csv (ou autre catégorie) est généré automatiquement.
Ce fichier contient toutes les données collectées.
Il est enregistré dans le dossier courant du script

