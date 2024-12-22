import numpy as np
import httpx
from fastapi import HTTPException


async def get_embedding(
    endpoint: str,
    api_key: str,
    local_url: str,
    text: str,
    timeout: int = 60,
    use_local: bool = False,
):
    """
    Asynchronous function to obtain embeddings from either a local container or the RunPod API.

    :param endpoint: RunPod API endpoint.
    :param api_key: API key for authorization (only used for RunPod).
    :param text: Text to process.
    :param timeout: Request timeout in seconds.
    :param use_local: Flag to indicate whether to use the local container.
    :param local_url: URL of the local embedding service.
    :return: Embedding vector as a numpy array.
    """
    payload = {"text": text, "config": {}}

    try:
        async with httpx.AsyncClient() as client:
            if use_local:
                response = await client.post(local_url, json=payload, timeout=timeout)
            else:
                url = f"https://api.runpod.ai/v2/{endpoint}/runsync"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                }
                response = await client.post(url, headers=headers, json={"input": payload}, timeout=timeout)

            response.raise_for_status()
            data = response.json()

            if use_local:
                embedding = np.array(data["vector"]).reshape(1, -1).astype(np.float32)
            else:
                if "output" not in data:
                    raise ValueError("The response does not contain the 'output' field.")
                embedding = np.array(data["output"]).reshape(1, -1).astype(np.float32)

            return embedding

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timed out.")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error: {str(e)}")
