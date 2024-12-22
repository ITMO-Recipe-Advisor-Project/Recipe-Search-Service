from dotenv import dotenv_values


def get_config():
    """
    Loads configuration values from a `.env` file.

    :return: A dictionary containing:
             - RUNPOD_API_KEY: API key for RunPod authentication.
             - RUNPOD_ENDPOINT: API endpoint for RunPod.
             - DATASET: Path to the dataset file.
             - LOWER_THRESHOLD: A threshold value for ingredient and recipe similarity.
             - K_NEIGHBORS: Number of neighbors to consider during index search.
    """

    env_vars = dotenv_values("env/.env")
    return {
        "RUNPOD_API_KEY": env_vars["RUNPOD_API_KEY"],
        "RUNPOD_ENDPOINT": env_vars["RUNPOD_ENDPOINT"],
        "EMBEDDING_SERVICE_LOCAL_URL": env_vars["EMBEDDING_SERVICE_LOCAL_URL"],
        "EMBEDDING_SERVICE_USAGE_FLAG": bool(env_vars["EMBEDDING_SERVICE_USAGE_FLAG"]),
        "DATASET": env_vars["DATASET"],
        "LOWER_THRESHOLD": float(env_vars["LOWER_THRESHOLD"]),
        "K_NEIGHBORS": int(env_vars["K_NEIGHBORS"]),
    }
