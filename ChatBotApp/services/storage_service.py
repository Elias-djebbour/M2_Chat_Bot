from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)  # Niveau INFO pour afficher les logs INFO et plus graves
logger = logging.getLogger(__name__)  # Obtient un logger spécifique à ce module

app = FastAPI()

class StoredContent(BaseModel):
    content: str
    embedding: list

DATABASE_FILE = "../database.json"  # Fichier JSON pour stocker les données

def store_in_json(data):
    """Enregistre les données dans un fichier JSON"""
    try:
        # Si le fichier existe, on charge les données existantes
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, "r") as f:
                database = json.load(f)
        else:
            # Si le fichier n'existe pas, on initialise une liste vide
            database = []

        # Ajout des nouvelles données à la base de données
        database.append(data)

        # Sauvegarde des données dans le fichier
        with open(DATABASE_FILE, "w") as f:
            json.dump(database, f, indent=4)

        logger.info("Données sauvegardées avec succès dans le fichier JSON.")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des données: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de sauvegarde : {e}")

@app.post("/store")
async def store_data(content: StoredContent):
    """Reçoit des données et les stocke dans un fichier JSON"""
    store_in_json(content.dict())
    return {"status": "Stored successfully"}
