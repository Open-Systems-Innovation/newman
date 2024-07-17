import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions


class VectorDatabaseManager:
    def __init__(self, db_path, db_name, embedding_model):
        """
        Initializes the VectorDatabaseManager with the path to the Chroma DB and the data directory.
        """
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model)
        self.db_name = db_name
        self.chunk_collection = self.create_collection("chunks")
        self.sentence_collection = self.create_collection("sentences")
        
    def create_collection(self, name):
        name = self.db_name + "_" + name
        collection = self.chroma_client.get_or_create_collection(
            name = name,
            embedding_function = self.embedding_model
            )
        return collection 

