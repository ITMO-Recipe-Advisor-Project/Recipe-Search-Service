import numpy as np
from fastapi import HTTPException
from app.config import get_config
import runpod
import logging

logger = logging.getLogger("main")

runpod.api_key = get_config().get("RUNPOD_API_KEY")

def get_embedding(sentence: str, endpoint: str):
    try:
        runpod_endpoint = runpod.Endpoint(endpoint)
        response = runpod_endpoint.run_sync(
            {
                "input": {
                    "text": sentence,
                },
            },
            timeout=60,
        )
        embedding = (
            np.array(response)
            .reshape(1, -1)
            .astype(np.float32)
        )
        return embedding
    except TimeoutError:
        logger.error("RunPod API request has timed out.")
        raise HTTPException(status_code=500, detail="RunPod API request has timed out.")
    except Exception as e:
        logger.error(f"An error occurred while making a request to RunPod: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while making a request to RunPod.")
