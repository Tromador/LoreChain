# lc_core/bge_embedding.py

from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer
import torch

class BGEEmbedding(Embeddings):
    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5", device: str = "cuda"):
        self.model = SentenceTransformer(model_name)
        self.model.to(torch.device(device))

    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text):
        return self.model.encode(text, convert_to_numpy=True).tolist()
