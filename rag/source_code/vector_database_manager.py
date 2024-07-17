import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

class VectorDatabaseManager:
    def __init__(self, vector_database_path, vector_db_name, embedding_function):
        """
        Initializes the VectorDatabaseManager with the path to the Chroma DB and the data directory.
        """
        self.chroma_client = chromadb.PersistentClient(path=vector_database_path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.chroma_client.get_or_create_collection(
            name="latex_paragraphs",
            embedding_function=self.embedding_function
        )

    def process_and_add_latex_paragraphs(self):
        """
        Processes each LaTeX file in the data directory, extracts paragraphs, and adds them to the Chroma collection.
        """
        latex_processor = LatexProcessor()
        for latex_file in self.latex_data_path.glob('*.tex'):
            paragraphs = latex_processor.process_document(latex_file)
            # Prepare data for Chroma DB
            ids = [f"{latex_file.stem}_{i}" for i in range(len(paragraphs))]
            metadatas = [{"source": latex_file.stem} for _ in paragraphs]
            
            # Add paragraphs to the Chroma collection
            self.collection.add(
                documents=paragraphs,
                ids=ids,
                metadatas=metadatas
            )

    def process_and_add_pdf_paragraphs(self):
        textbook_processor = TextbookProcessor()
        for pdf in self.textbook_data_path.glob('*.pdf'):
            paragraphs = textbook_processor.process_document(pdf)
            ids = [f"{pdf.stem}_{i}" for i in range(len(paragraphs))]
            metadatas = [{"source": pdf.stem} for _ in paragraphs]
            
            # Add paragraphs to the Chroma collection
            self.collection.add(
                documents=paragraphs,
                ids=ids,
                metadatas=metadatas
            )
