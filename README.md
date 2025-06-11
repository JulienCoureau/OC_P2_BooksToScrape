# OC_P2_BooksToScrape
## INFORMATIONS GÉNÉRALES

Titre du jeu de données : Scraping de livres depuis Books to Scrape

Date de création : 22/04/2025

Auteur : Julien Coureau

Version : 0.0.1

## INFORMATIONS MÉTHODOLOGIQUES
Contexte et objectif
Ce projet a été réalisé dans le cadre d’un exercice (Projet 2 de Openclassroom) visant à automatiser la récupération des prix de livres au moment de l'exécution. Le script permet de scraper les données de livres depuis le site Books to Scrape.​

## INFORMATIONS SPÉCIFIQUES AUX DONNÉES

Liste des variables/entêtes de colonne :

| Variable / Entêtes | Traduction |
| ------ | ------ |
| universal_product_code (UPC)  | Code universel du produit|
| title | Titre du livre |
| price_including_tax | Prix TTC |
| price_excluding_tax | Prix HT |
| number_available | Nombre d'exemplaires disponibles |
| product_description | Description du livre |
| category | Catégorie du livre |
| review_rating | Note du livre (sur 5) |
| image_url | URL de l'image du livre |
- Code des valeurs manquantes : les valeurs manquantes sont indiquées par "Na".

## UTILISATION
##### Pré-requis
Langage : [Python 3.8+]

Bibliothèques nécessaires :
- requests
- beautifulsoup4

##### Installation et démarrage 

1°) Cloner le repository :

```sh
https://git@github.com:JulienCoureau/OC_P2_BooksToScrape.git
```

2°) Créer et activer un environnement virtuel

```sh
cd OC_P2_BooksToScrape
python -m venv env
```
mac/linux
```
source env/bin/activate 
```
Windows
```
env\Scripts\activate
```

3°) Installer les dépendances

```
pip install -r requirements.txt
```

4°) Exécuter le scipt principal

```
python ScrapBooksToScrape.py
```
### Resultats

Après exécution : 
- Un dossier books sera créé automatiquement
- Chaque catégorie aura son propre sous-dossier
- Chaque sous dossier contiendra : 
    - Un fichier CSV avec les informations des livres
    -  Un dossier images contenant toutes les couvertures des livres

Note 

- Un script vérifie automatiquement qu'il y a bien 50 catégories
- En cas de problème réseau ou de structure du site modifiée, un message d'erreur apparaîtra