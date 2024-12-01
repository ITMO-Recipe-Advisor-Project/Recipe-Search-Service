from dotenv import dotenv_values

def get_config():
    env_vars = dotenv_values("env/.env")
    return {
        "RUNPOD_API_KEY": env_vars["RUNPOD_API_KEY"],
        "RUNPOD_ENDPOINT": env_vars["RUNPOD_ENDPOINT"],
        "DATASET": env_vars["DATASET"],
        "LOWER_THRESHOLD": env_vars["LOWER_THRESHOLD"],
    }