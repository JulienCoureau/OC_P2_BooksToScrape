import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
from image_saver import save_image_from_url

def get_all_categories():
    """Scrappe toutes les catégories disponibles sur la page d'accueil."""

    url = "https://books.toscrape.com/index.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erreur lors de l'accès à {url}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    category_links = soup.select("div.side_categories ul li ul li a")

    category_dict = {}

    for link in category_links:
        name = link.text.strip().lower().replace(" ", "-")  
        href = link["href"]                                 
        full_url = urljoin(url, href)                       
        category_dict[name] = full_url                      
    
    expected_categories = 50
    if len(category_dict) != expected_categories:
        print(f"Attention : {len(category_dict)} catégories trouvées au lieu de {expected_categories}.")
        print("Vérifiez si le site a été modifié.")
        return None

    return category_dict

def scrape_book_data(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erreur : impossible d'accéder à {url}")
        return None
    else:
        print(f"Accès à l'URL : {url}") 

    soup = BeautifulSoup(response.text, 'html.parser') 

    product_page_url = url  

    title = soup.find("h1").text  

    table = soup.find("table", class_="table table-striped") 
    rows = table.find_all("tr")  
    data_dict = {row.th.text: row.td.text for row in rows} 

    universal_product_code = data_dict.get("UPC", "Na")
    price_including_tax = data_dict.get("Price (incl. tax)", "Na").replace("Â", "").strip()
    price_excluding_tax = data_dict.get("Price (excl. tax)", "Na").replace("Â", "").strip()
    number_available = data_dict.get("Availability", "Na")

    description = soup.find("div", id="product_description")
    if description: 
        product_description = description.find_next_sibling("p").text 
    else:
        product_description = "Na"

    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    
    rating_tag = soup.find("p", class_="star-rating")
    star_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    if rating_tag:
        rating_word = rating_tag.get("class")[1]
        review_rating = f"{star_map.get(rating_word, 0)}/5"
    else:
        review_rating = "Na"

    image_relative_url = soup.find("div", class_="item active").img["src"]
    image_url = "https://books.toscrape.com/" + image_relative_url.replace("../", "")

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

def get_all_book_urls_from_category(category_url):
    book_urls = []

    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')

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
            break

    return book_urls

def save_multiple_books_to_csv(data_list, filename="books.csv"):
    if not data_list:
        print("Aucune donnée à enregistrer.")
        return

    fieldnames = [
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

    try:
        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)

        print(f"{len(data_list)} livres enregistrés dans le fichier : {filename}")
        print(f"Emplacement : {os.path.abspath(filename)}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

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

                save_image_from_url(book_data["image_url"], book_data["universal_product_code"], folder=images_folder)

        csv_filename = os.path.join(category_folder, f"{category_name}.csv")
        save_multiple_books_to_csv(books_data, csv_filename)

    print("\n Toutes les catégories ont été scrapées avec succès !")

if __name__ == "__main__":
    categories = get_all_categories()
    if categories != None :
        scrape_all_categories(categories)
