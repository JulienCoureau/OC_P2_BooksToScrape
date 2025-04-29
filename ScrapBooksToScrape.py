# ## Import des Librairies
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
from image_saver import save_image_from_url

## --------------------------------------
## RÉCUPÉRER TOUTES LES CATÉGORIES
## --------------------------------------

def get_all_categories():
    """Scrappe toutes les catégories disponibles sur la page d'accueil."""

    url = "https://books.toscrape.com/index.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erreur lors de l'accès à {url}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    # Sélectionne toutes les balises <a> dans la liste des catégories
    category_links = soup.select("div.side_categories ul li ul li a")

    category_dict = {}

    for link in category_links:
        name = link.text.strip().lower().replace(" ", "-")  # Nettoie le nom de la catégorie
        href = link["href"]                                 # Récupère l'URL relative
        full_url = urljoin(url, href)                       # Construit l'URL complète
        category_dict[name] = full_url                      # Ajoute au dictionnaire

    return category_dict

## Vérification du nombre de catégories trouvées

categories = get_all_categories()

expected_categories = 50  # Nombre attendu normalement
if len(categories) != expected_categories:
    print(f"Attention : {len(categories)} catégories trouvées au lieu de {expected_categories}.")
    print("Vérifiez si le site a été modifié.")
else:
    print(f"Nombre correct de catégories : {len(categories)}")

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
    price_including_tax = data_dict.get("Price (incl. tax)", "Na").replace("Â", "").strip()
    price_excluding_tax = data_dict.get("Price (excl. tax)", "Na").replace("Â", "").strip()
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
# Verifie si il existe une page suivante
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
## SCRAPPER TOUTES LES CATÉGORIES AUTOMATIQUEMENT
## --------------------------------------

def scrape_all_categories(categories):
    """Scrappe toutes les catégories et enregistre CSV + Images."""

    base_folder = "books"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    for category_name, category_url in categories.items():
        print(f"\nScraping catégorie : {category_name}")

        category_folder = os.path.join(base_folder, category_name)
        images_folder = os.path.join(category_folder, "images")
        os.makedirs(images_folder, exist_ok=True)

        book_urls = get_all_book_urls_from_category(category_url)
        print(f"{len(book_urls)} livres trouvés.")

        books_data = []

        for book_url in book_urls:
            book_data = scrape_book_data(book_url)
            if book_data:
                books_data.append(book_data)

                # Sauvegarde l'image
                save_image_from_url(book_data["image_url"], book_data["universal_product_code"], folder=images_folder)

        csv_filename = os.path.join(category_folder, f"{category_name}.csv")
        save_multiple_books_to_csv(books_data, csv_filename)

    print("\n Toutes les catégories ont été scrapées avec succès !")

## --------------------------------------
## Appel
## --------------------------------------

if __name__ == "__main__":
    categories = get_all_categories()

    # Vérification du nombre de catégories
    expected_categories = 50
    if len(categories) != expected_categories:
        print(f"Attention : {len(categories)} catégories trouvées au lieu de {expected_categories}.")
    else:
        print(f"Nombre de catégories correct : {len(categories)}")

    scrape_all_categories(categories)
