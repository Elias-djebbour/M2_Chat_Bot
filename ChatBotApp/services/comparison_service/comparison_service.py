from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import json

DATABASE_URL = "../../database.json"
# Charger les tweets et leurs embeddings depuis un fichier JSON
def load_tweets():
    with open(DATABASE_URL, "r") as f:
        return json.load(f)

tweets_data = load_tweets()

# Création de l'application FastAPI
app = FastAPI()

# Modèle pour l'input du client
class EmbeddingInput(BaseModel):
    embedding: List[float]

# Fonction pour calculer la similarité cosinus
def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2) if norm_vec1 and norm_vec2 else 0.0

@app.post("/find_similar_tweets")
async def find_similar_tweets(input_data: EmbeddingInput):
    """
    Reçoit un embedding, le compare avec les embeddings de tweets stockés,
    et retourne les deux tweets les plus proches en utilisant la similarité cosinus.
    """
    input_embedding = input_data.embedding

    # Liste pour stocker les similarités cosinus pour chaque tweet
    similarity_scores = []

    # Calculer la similarité cosinus entre l'input_embedding et chaque embedding de tweet
    for tweet in tweets_data:
        tweet_embedding = tweet["embedding"]
        similarity = cosine_similarity(input_embedding, tweet_embedding)
        similarity_scores.append((tweet, similarity))

    # Trier les tweets par similarité (du plus grand au plus petit)
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    # Récupérer les deux tweets les plus similaires
    top_2_tweets = [tweet for tweet, _ in similarity_scores[:2]]
    
    return {"top_similar_tweets": top_2_tweets}
