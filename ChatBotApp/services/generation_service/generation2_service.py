import openai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging
# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Définir la clé API d'OpenAI
openai.api_key = "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"

# Initialisation de FastAPI
app = FastAPI()

# Définir la structure de la requête avec Pydantic
class TextGenerationRequest(BaseModel):
    question: str

# Fonction pour générer une réponse via OpenAI
def generate_answer(question: str) -> str:
    logger.info('salut')
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # ou "gpt-4"
    messages=[{"role": "user", "content": question}],
    max_tokens=150
    )
    logger.info("La réponse est : %s", response)

    return response.choices[0].text.strip()  # Retourner la réponse générée

# Point d'entrée POST pour générer du texte
@app.post("/generate_text")
async def generate_text(request: TextGenerationRequest):
    try:
        # Obtenir la question depuis la requête
        question = request.question
        # Générer une réponse avec GPT-4
        answer = generate_answer(question)

        logger.info('Réponse générée: %s', answer)
        
        # Retourner la réponse générée
        #return JSONResponse(content={"question": question, "answer": answer})
    
    except Exception as e:
        # En cas d'erreur, retourner un message d'erreur
        #return JSONResponse(content={"error": str(e)}, status_code=400)
        pass

# Lancer le serveur avec Uvicorn
# Exécuter avec: uvicorn main:app --reload
