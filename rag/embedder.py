import chromadb
from chromadb.utils import embedding_functions

class Embedder:
    def __init__(self, chunks, file_name, vector_database):
        self.chunks = chunks
        self.file_name = file_name
        self.vector_database = vector_database
        self.process_chunks()

    def process_chunks(self):
        # Prepare data for Chroma DB
        ids = [f"{self.file_name}_{i}" for i in range(len(self.chunks))]
        metadatas = [{"source": self.file_name} for _ in self.chunks]
       
        # Add paragraphs to the Chroma collection
        self.vector_database.chunk_collection.add(
            documents=self.chunks,
            ids=ids,
            metadatas=metadatas
            )
