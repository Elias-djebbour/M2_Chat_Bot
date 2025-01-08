from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Modèle de données pour le contenu reçu
class Content(BaseModel):
    content: str  # Le texte (tweet, article, etc.)

# Charger le modèle paraphrase-MiniLM-L6-v2
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

@app.post("/embed")
async def calculate_embedding(content: Content):
    
    try:
        # Calculer l'embedding du contenu en utilisant le modèle paraphrase-MiniLM-L6-v2
        embedding = model.encode(content.content)

        # Retourner l'embedding sous forme de réponse
        return {"embedding": embedding.tolist()}  # Convertir en liste pour JSON sérialisable

    except Exception as e:
        logger.info(content.content)
        logger.error(f"Erreur lors du calcul de l'embedding: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors du calcul de l'embedding")
