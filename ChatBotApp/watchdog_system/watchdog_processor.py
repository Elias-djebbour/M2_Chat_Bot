import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

# Définir l'URL de l'API à laquelle nous enverrons les données
API_URL = "http://127.0.0.1:8000/send"

# Fonction pour envoyer chaque message complet à l'API
def send_to_api(message):
    try:
        response = requests.post(API_URL, json={"content": message})
        if response.status_code == 200:
            print(f"Envoyé avec succès: {message}")
        else:
            print(f"Échec de l'envoi pour: {message} - Code de statut: {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi: {e}")

# Définir la classe d'événement pour surveiller les fichiers
class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".txt"):
            print(f"Fichier détecté: {event.src_path}")
            with open(event.src_path, 'r', encoding='utf-8') as file:
                buffer = ""  # Pour stocker chaque message complet
                is_article = False  # Pour distinguer si on est dans un article ou un tweet

                for line in file:
                    line = line.strip()
                    if not line:
                        continue  # Ignore les lignes vides
                    
                    # Vérifie si la ligne commence par "Article" (début d'un article)
                    if line.startswith("Article"):
                        if buffer:
                            send_to_api(buffer.strip())  # Envoie le message précédent s'il y en a un
                        buffer = line  # Démarre un nouvel article
                        is_article = True
                    else:
                        # Sinon, ajoute la ligne au buffer actuel
                        buffer += " " + line
                    
                    # Vérifie si c'est la fin du message
                    if is_article and line.endswith('.'):
                        # Si c'est un article et qu'on a un point final, envoie le message
                        send_to_api(buffer.strip())
                        buffer = ""  # Réinitialise le buffer
                        is_article = False  # Remet le statut article à False
                    elif not is_article and re.search(r'#\w+$', line):
                        # Si ce n'est pas un article et qu'il se termine par un hashtag
                        send_to_api(buffer.strip())
                        buffer = ""  # Réinitialise le buffer

                # Envoie tout message restant dans le buffer après la dernière ligne du fichier
                if buffer:
                    send_to_api(buffer.strip())

# Fonction principale pour démarrer le système de surveillance
def start_watchdog(directory_to_watch):
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()
    print(f"Surveillance du dossier {directory_to_watch} démarrée...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Surveillance arrêtée.")
    observer.join()

# Dossier à surveiller
directory_to_watch = "./watchdog_repo"  # Changez ce chemin vers votre dossier cible
start_watchdog(directory_to_watch)
