# ## Import des Librairies
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os

## --------------------------------------
## Scrappe un livre
## --------------------------------------

## Creation de la fonction pour l'écrire qu'une seule fois (Utilisable dans les : boucles, fonction, dossier séparé)
def scrape_book_data(url):
    response = requests.get(url)  # Va chercher la page

    if response.status_code != 200:
        print(f"Erreur : impossible d'accéder à {url}")
        return None
    else:
        print(f"Accès à l'URL : {url}")  # Vérifie si la page est trouvée

    soup = BeautifulSoup(response.text, 'html.parser')  # Analyse le contenu HTML

    # ----------------------------
    ### Recuperer les données :

    ## URL
    product_page_url = url  # On recupère l'url

    ## Titre
    title = soup.find("h1").text  # On recupère la balise "h1" ➡️ Correspond au titre

    ## Recuperer les valeurs de chaque ligne dans le dictionaire.
    # .get et si il manque une valeur, "Na" apparait
    table = soup.find("table", class_="table table-striped")  # Cherche la première balise "table" avec la classe CSS
    rows = table.find_all("tr")  # Recupère toutes les lignes "tr"
    data_dict = {row.th.text: row.td.text for row in rows}  # Crée un dictionnaire avec les infos du tableau

    ## Valeurs du tableau
    universal_product_code = data_dict.get("UPC", "Na")
    price_including_tax = data_dict.get("Price (incl. tax)", "Na")
    price_excluding_tax = data_dict.get("Price (excl. tax)", "Na")
    number_available = data_dict.get("Availability", "Na")

    ## Description
    description = soup.find("div", id="product_description") #Cherche au niveau de balise <div> l'id et <p>
    if description:  # si la description est presente extraction
        product_description = description.find_next_sibling("p").text # Suit la structure HTML (trouve la balise(" ")) va au paragraphe qui suit la balise demander
    else:
        product_description = "Na" # si elle  n'est pas mets la valeur "Na"

    ## Catégorie
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    # Trouver la balise "ul" avec la classe breadcrumb, recuperation de tous les <li> et on prend le 3eme élement de la liste[2] car on commence a 0

    ## Note
    rating_tag = soup.find("p", class_="star-rating")
    star_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    if rating_tag: # condition verifie si rating_tag existe
        rating_word = rating_tag.get("class")[1] # Recupère le 2eme élement
        review_rating = f"{star_map.get(rating_word, 0)}/5" # met la note /5
    else:
        review_rating = "Na" # si erreur ou note absente "Na"

    # Image URL
    image_relative_url = soup.find("div", class_="item active").img["src"] # récupère les valeurs
    image_url = "https://books.toscrape.com/" + image_relative_url.replace("../", "")  # URL complète

    # Dictionnaire final pour retourner les informations demandées
    return {
        "product_page_url": product_page_url,
        "universal_product_code": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url
    }

## --------------------------------------
## Enregistrer une image (phase4)
## --------------------------------------

def save_image_from_url(image_url, upc, folder="images"):
    if not os.path.exists(folder): # verifie sir le dossier "images" existe
        os.makedirs(folder) # crée le dossier si il n'exsite pas

    filename = os.path.join(folder, f"{upc}.jpg") #nom (assemblage nom dossier + ficher)

    try: # Bloc pour gérer les erreurs
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image enregistrée : {filename}")
        else:
            print(f"Image non trouvée : {image_url}")
    except Exception as e:
        print(f"Erreur image : {e}")

## --------------------------------------
## Fonction pour scrapper une catégorie (url)
## --------------------------------------

def get_all_book_urls_from_category(category_url):
    book_urls = [] # prépare une liste vide pour stocker dous les livres

    while True: #boucle infini contiinue tant qu'il ya une page suivante
        response = requests.get(category_url) # telecharge la page
        soup = BeautifulSoup(response.text, 'html.parser') # analyse html

        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            relative_url = article.find("h3").a["href"]
            full_url = urljoin(category_url, relative_url)
            book_urls.append(full_url)

        next_page = soup.find("li", class_="next")
        if next_page:
            next_url = next_page.find("a")["href"]
            category_url = urljoin(category_url, next_url)
        else:
            break # sort de la boucle

    return book_urls

## --------------------------------------
## Enregistrer plusieurs livres
## --------------------------------------

def save_multiple_books_to_csv(data_list, filename="books.csv"): # data liste = liste dictionnaires pour chaque livre / filname nom du fichier de sortie
    if not data_list: # verifie sir la liste est vide
        print("Aucune donnée à enregistrer.")
        return

    fieldnames = [ # défiini le nom de dolonnes pour le csv qui doit correspondre au dictionnaire d'avant de data_list
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ]
# CSV
    try:
        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in data_list: # pour chaque dictinnaire de livre il ecrit une ligne complete dan sle scv
                writer.writerow(data)

        print(f"{len(data_list)} livres enregistrés dans le fichier : {filename}")
        print(f"Emplacement : {os.path.abspath(filename)}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

## --------------------------------------
## Scrape les info d'une catégorie donnée
## --------------------------------------

def scrape_category(category_name):
    category_dict = {
        "sports": "sports-and-games_17",
        "science": "science_22",
        "travel": "travel_2"
    }

    if category_name not in category_dict:
        print(f"Catégorie inconnue : {category_name}")
        return

    slug = category_dict[category_name]
    category_url = f"https://books.toscrape.com/catalogue/category/books/{slug}/index.html"

    print(f"\n🔍 Scraping de la catégorie : {category_name}")
    print(f"URL : {category_url}")

    book_urls = get_all_book_urls_from_category(category_url)
    print(f"🔗 {len(book_urls)} livres trouvés.")

    books_data = []
    for url in book_urls:
        book_data = scrape_book_data(url)
        if book_data:
            books_data.append(book_data)

    filename = f"{category_name}_books.csv"
    save_multiple_books_to_csv(books_data, filename)

## --------------------------------------
## Appel
## --------------------------------------

# Scrape la catégorie que l'on veut
test_category = "sports"  # "science", "travel"
scrape_category(test_category)

# fiche produit d’un livre
test_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Appel de la fonction
data = scrape_book_data(test_url) # retourne un dictionnanire avec toutes les infos du livre

# Vérification du contenu
if data:
    print("\nDictionnaire récupéré :")
    for key, value in data.items():
        print(f"{key} : {value}")
