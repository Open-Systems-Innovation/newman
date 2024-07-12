import os
import logging
import warnings
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from latex_processor import LatexProcessor


# Configure the root logger to suppress all but warning and error messages

class VectorDatabaseManager:
    def __init__(self, db_path, data_dir):
        """
        Initializes the VectorDatabaseManager with the path to the Chroma DB and the data directory.
        """

        warnings.filterwarnings("ignore", category=UserWarning, module='onnxruntime')
        logging.getLogger('chromadb').setLevel(logging.ERROR)
        self.data_path = Path(data_dir)
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.chroma_client.get_or_create_collection(
            name="latex_paragraphs",
            embedding_function=self.embedding_function
        )

    def process_and_add_paragraphs(self):
        """
        Processes each LaTeX file in the data directory, extracts paragraphs, and adds them to the Chroma collection.
        """
        latex_processor = LatexProcessor()
        for tex_file in self.data_path.glob('*.tex'):
            paragraphs = latex_processor.process_document(tex_file)
            # Prepare data for Chroma DB
            ids = [f"{tex_file.stem}_{i}" for i in range(len(paragraphs))]
            metadatas = [{"source": tex_file.stem} for _ in paragraphs]
            
            # Add paragraphs to the Chroma collection
            self.collection.add(
                documents=paragraphs,
                ids=ids,
                metadatas=metadatas
            )
