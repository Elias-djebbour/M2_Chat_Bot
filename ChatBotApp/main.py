from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# URL des services externes
EMBEDDING_SERVICE_URL = "http://127.0.0.1:8002/embed"
STORAGE_SERVICE_URL = "http://127.0.0.1:8001/store"

# Modèle de données pour le contenu reçu
class Content(BaseModel):
    content: str  # le tweet ou l'article

@app.post("/send")
async def process_content(content: Content):
    # Appeler le service de calcul d'embedding
    try:
        embedding_response = requests.post(EMBEDDING_SERVICE_URL, json={"content": content.content})
        if embedding_response.status_code != 200:
            raise Exception("Erreur lors de la récupération de l'embedding")
        embedding = embedding_response.json().get("embedding")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'appel au service d'embedding : {e}")

    # Préparer les données pour le stockage
    data_to_store = {
        "content": content.content,
        "embedding": embedding
    }

    # Envoi au service de stockage
    try:
        storage_response = requests.post(STORAGE_SERVICE_URL, json=data_to_store)
        if storage_response.status_code != 200:
            raise Exception("Erreur lors de l'enregistrement des données dans le service de stockage")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de stockage : {e}")

    return {"status": "OK"}
