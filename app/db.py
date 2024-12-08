import pandas as pd
import faiss
import numpy as np
import logging

logger = logging.getLogger("main")


def load_data(dataset_path: str):
    """
    Loads data from a Parquet dataset, processes embeddings, and creates a FAISS index.

    :param dataset_path: Path to the Parquet file containing the dataset.
    :return: A tuple containing:
             - The processed DataFrame with the embeddings and directions removed.
             - A FAISS index initialized with the normalized embeddings.
    """
    logger.info("Loading data...")
    df = pd.read_parquet(dataset_path)
    embeddings = np.vstack(df["NER_embedding"].values)
    faiss.normalize_L2(embeddings)

    df.drop(columns=["NER_embedding", "directions"], inplace=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    logger.info("FAISS index is created and data is loaded.")
    return df, index
