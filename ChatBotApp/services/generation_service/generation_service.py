from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI()

# Initialisation du pipeline de résumé avec un modèle abstrait
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Modèle pour la requête du client
class TextGenerationRequest(BaseModel):
    prompt: str  # Texte envoyé par l'utilisateur
    max_tokens: int = 150  # Nombre maximum de tokens dans la réponse


@app.post("/generate_text")
async def generate_text(request: TextGenerationRequest):
    """
    Cette fonction reçoit un texte en entrée (prompt), utilise le pipeline de résumé
    pour générer un résumé reformulé du texte et renvoie ce résumé.
    """
    try:
        # Utilisation du pipeline de résumé abstrait pour générer un résumé
        summary = summarizer(request.prompt, max_length=request.max_tokens, min_length=50, do_sample=True)

        logger.info(f"Résumé généré: {summary[0]['summary_text']}")
        
        # Retourner le résumé généré
        return {"summary": summary[0]['summary_text']}
    
    except Exception as e:
        # En cas d'erreur, renvoyer une erreur HTTP 500
        logger.error(f"Erreur lors de la génération du résumé: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du résumé")
