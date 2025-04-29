import  os
import requests

def save_image_from_url(image_url, upc, folder="images"):
    """Télécharge et enregistre une image à partir de son URL."""
    
    if not os.path.exists(folder):  # Vérifie si le dossier existe
        os.makedirs(folder)          # Crée le dossier s'il n'existe pas

    filename = os.path.join(folder, f"{upc}.jpg")  # Définit le chemin complet du fichier image

    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"📷 Image enregistrée : {filename}")
        else:
            print(f"⚠️ Image non trouvée : {image_url}")
    except Exception as e:
        print(f" Erreur lors du téléchargement de l'image : {e}")