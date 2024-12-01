from fastapi import APIRouter, HTTPException, Request
from app.models import RecipeQuery
from app.services import get_embedding
import faiss
import random
import logging

logger = logging.getLogger("main")

router = APIRouter()

@router.post("/search/")
async def search_recipes(query: RecipeQuery, request: Request):
    df = request.app.state.df
    index = request.app.state.index
    config = request.app.state.config

    logger.info(f"Received query: {query.query}")

    query_embedding = get_embedding(query.query, config['RUNPOD_ENDPOINT'])
    faiss.normalize_L2(query_embedding)

    k = 100
    distances, indices = index.search(query_embedding, k)

    results = []
    for i, idx in enumerate(indices[0]):
        if distances[0][i] < float(config['LOWER_THRESHOLD']):
            break
        result = {
            "title": df.iloc[idx]["title"],
            "ingredients": df.iloc[idx]["ingredients"].tolist(),
            "link": f"https://{df.iloc[idx]['link']}",
        }
        results.append(result)

    if not results:
        logger.warning("No recipes found for the given query.")
        raise HTTPException(status_code=404, detail="No recipes found.")

    random_results = random.sample(results, min(10, len(results)))
    logger.info(f"Returning {len(random_results)} random recipes.")

    return random_results
