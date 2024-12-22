import faiss
import random
import logging
from app.config import get_config
from fastapi import APIRouter, HTTPException, Request
from app.models import RecipeQuery
from app.services import get_embedding

logger = logging.getLogger("main")
k_neighbors = get_config()["K_NEIGHBORS"]

router = APIRouter()


@router.post("/search/")
async def search_recipes(query: RecipeQuery, request: Request):
    """
    Endpoint to search for recipes based on a query string.

    :param query: A `RecipeQuery` object containing the search query string.
    :param request: A `Request` object providing access to application state.
    :return: A list of up to 10 random recipes matching the query.
    :raises HTTPException: If no recipes are found or an error occurs.
    """

    df = request.app.state.df
    index = request.app.state.index
    config = request.app.state.config

    logger.info(f"Received query: {query.query}")

    try:
        query_embedding = await get_embedding(
            text=query.query,
            endpoint=config["RUNPOD_ENDPOINT"],
            api_key=config["RUNPOD_API_KEY"],
            local_url=config["EMBEDDING_SERVICE_LOCAL_URL"],
            use_local=config["EMBEDDING_SERVICE_USAGE_FLAG"],
        )

        faiss.normalize_L2(query_embedding)

        k = k_neighbors
        distances, indices = index.search(query_embedding, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if distances[0][i] < float(config["LOWER_THRESHOLD"]):
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

    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unknown error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
