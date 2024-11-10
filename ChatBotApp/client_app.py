from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Création de l'application FastAPI
app = FastAPI()

# Modèle pour la requête du client
class TextInput(BaseModel):
    text: str

# URLs des services externes
EMBEDDING_SERVICE_URL = "http://127.0.0.1:8002/embed"  # URL du service de calcul d'embed
COMPARISON_SERVICE_URL = "http://127.0.0.1:8003/find_similar_tweets"  # URL du service de comparaison

@app.post("/AI_Response")
async def AI_Response(input_data: TextInput):
    """
    Reçoit un texte en entrée, envoie ce texte au service d'API pour calculer l'embedding,
    puis utilise cet embedding pour trouver les tweets les plus similaires via le service de comparaison.
    """
    # Préparer les données pour l'API d'embedding
    payload = {"text": input_data.text}
    
    try:
        # 1. Appel au service d'embedding
        embedding_response = requests.post(EMBEDDING_SERVICE_URL, json=payload)
        
        # Vérifie si l'appel au service d'embedding a réussi
        if embedding_response.status_code != 200:
            raise HTTPException(status_code=embedding_response.status_code, detail="Erreur dans le service d'embedding")
        
        # Récupère l'embedding
        embedding_result = embedding_response.json().get("embedding")
        if embedding_result is None:
            raise HTTPException(status_code=500, detail="Embedding non trouvé dans la réponse du service d'embedding")

        # Préparer les données pour le service de comparaison
        comparison_payload = {"embedding": embedding_result}

        # 2. Appel au service de comparaison
        comparison_response = requests.post(COMPARISON_SERVICE_URL, json=comparison_payload)

        # Vérifie si l'appel au service de comparaison a réussi
        if comparison_response.status_code != 200:
            raise HTTPException(status_code=comparison_response.status_code, detail="Erreur dans le service de comparaison")
        
        # Récupère et retourne les tweets les plus similaires
        similar_tweets = comparison_response.json().get("top_similar_tweets")
        if similar_tweets is None:
            raise HTTPException(status_code=500, detail="Aucun tweet similaire trouvé dans la réponse du service de comparaison")

        print(similar_tweets)
        return {"similar_tweets": similar_tweets}

    except requests.RequestException as e:
        # Gestion des erreurs de communication avec les services externes
        raise HTTPException(status_code=500, detail=f"Erreur lors de la communication avec les services externes : {str(e)}")
