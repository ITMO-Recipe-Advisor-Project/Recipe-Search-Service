import numpy as np
import httpx
from fastapi import HTTPException
import logging

logger = logging.getLogger("main")


async def get_embedding(endpoint: str, api_key: str, text: str, timeout: int = 60):
    """
    Asynchronous request to the RunPod API to obtain embeddings.

    :param endpoint: RunPod API endpoint.
    :param api_key: API key for authorization.
    :param text: Text to process.
    :param timeout: Request timeout in seconds.
    :return: Value from the `output` field of the response.
    """
    url = f"https://api.runpod.ai/v2/{endpoint}/runsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {"input": {"text": text}}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=timeout)
            response.raise_for_status()

            data = response.json()
            if "output" not in data:
                raise ValueError("The response does not contain the 'output' field.")

            embedding = np.array(data["output"]).reshape(1, -1).astype(np.float32)

            return embedding

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to RunPod API timed out.")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error: {str(e)}")
