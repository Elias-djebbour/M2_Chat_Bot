import tkinter as tk
from tkinter import scrolledtext
import requests

import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Port de l'application 8005
# URL de l'API
API_URL = "http://127.0.0.1:8004/AI_Response"  # Assurez-vous que l'API FastAPI est lancée à cette URL

# Fonction pour envoyer le texte utilisateur à l'API et obtenir les tweets similaires
def get_response_from_api(user_input):
    payload = {"text": user_input}
    try:

        logger.info(payload)
        # Appel API pour obtenir les tweets similaires
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Gérer les erreurs HTTP

        # Extraction des tweets similaires depuis la réponse
        similar_tweets = response.json().get("similar_tweets", [])
        
        if similar_tweets:
            # Formater les tweets similaires pour l'affichage
            formatted_response = "\n\n".join(
                f"- {tweet['content']}" for tweet in similar_tweets
            )
            return f"Tweets similaires:\n{formatted_response}"
        else:
            return "Aucun tweet similaire trouvé."
    except requests.RequestException as e:
        return f"Erreur de l'API: {e}"

# Fonction pour envoyer le message
def send_message():
    user_message = entry_field.get()  # Récupérer le message de l'utilisateur
    if user_message.strip() != "":
        chat_window.config(state=tk.NORMAL)  # Débloquer la zone de texte
        chat_window.insert(tk.END, "Vous: " + user_message + "\n")  # Afficher le message de l'utilisateur
        entry_field.delete(0, tk.END)  # Effacer la zone de saisie

        # Obtenir la réponse de l'API
        bot_response = get_response_from_api(user_message)
        chat_window.insert(tk.END, "Bot: " + bot_response + "\n\n")  # Afficher la réponse du bot
        chat_window.config(state=tk.DISABLED)  # Bloquer la zone de texte après l'ajout
        chat_window.yview(tk.END)  # Faire défiler vers le bas pour voir la nouvelle réponse

# Configuration de l'interface utilisateur
root = tk.Tk()
root.title("Chatbot avec API de Similarité")
root.geometry("400x500")
root.resizable(width=False, height=False)

# Zone de chat avec défilement
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_window.config(state=tk.DISABLED)  # Zone de texte initialement en lecture seule
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Zone de saisie pour le message
entry_field = tk.Entry(root, font=("Arial", 12))
entry_field.pack(padx=10, pady=10, fill=tk.X)
entry_field.focus()

# Bouton d'envoi
send_button = tk.Button(root, text="Envoyer", command=send_message)
send_button.pack(padx=10, pady=5)

# Fonction pour envoyer le message avec la touche "Entrée"
def on_enter_key(event):
    send_message()

entry_field.bind("<Return>", on_enter_key)  # Lier la touche Entrée à l'envoi du message

# Lancement de l'application
root.mainloop()
