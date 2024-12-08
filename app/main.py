from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import get_config
from app.db import load_data
from app.endpoints import recipes
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("main")

config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing data...")
    df, index = load_data(config["DATASET"])
    app.state.df = df
    app.state.index = index
    app.state.config = config

    logger.info("Data initialization complete.")

    yield

    logger.info("Cleaning up resources...")
    del app.state.df
    del app.state.index


app = FastAPI(lifespan=lifespan)

app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
