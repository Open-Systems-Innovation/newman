import sys
import os

import chromadb

from prompt_parser import PromptParser
from vector_database_manager import VectorDatabaseManager
from chunker import Chunker
from embedder import Embedder
from generator import Generator

import pdb

def parse_prompt(arguments):
    parser = PromptParser(arguments)
    return parser.prompt

def get_or_create_vector_db(database_path, database_name, embedding_function):
    vector_database_manager =  VectorDatabaseManager(database_path,
                                                     database_name,
                                                     embedding_function)
    return vector_database_manager
    
def chunk_text(path_to_textbook_txt, max_chunk_size, vector_db, similarity_threshold):
    chunker = Chunker(path_to_textbook_txt, max_chunk_size, vector_db, similarity_threshold) 
    return chunker.chunks

def embed_chunks(chunks, file_name, vector_db):
    embedder = Embedder(chunks, file_name, vector_db)

def retrieve_chunks(prompt, vector_db, n_chunks_to_retrieve):
    retrieved_chunks = vector_db.query(
        query_texts = [prompt],
        n_results = n_similar_results
        )
    return retrieved_chunks

def generate_response():
    response_generator = Generator()
    response_generator.run()
    return response_generator.response


if __name__ == "__main__":

    # SET PARAMETERS
    n_chunks_to_retrieve = 10  # set the number of chunks to retrieve
    path_to_textbook_txt = "../data/develop/petsc-users-manual-2024.txt" 
    vector_database_path = "./vector_databases/petsc_textbook"
    vector_database_name = "petsc_textbook"
    embedding_model = "all-MiniLM-L6-v2"
    max_chunk_size = 2506 # max chunk size in characters
    cosine_similarity_threshold = 0.8
    
    # parse prompt from commandline arguments
    prompt = parse_prompt(sys.argv)
        
    # Check for other command line arguments
    update_database = "-update-database" in sys.argv
    print_prompt = "-print-prompt" in sys.argv

    vector_db = get_or_create_vector_db(vector_database_path,
                                        vector_database_name,
                                        embedding_model)
    
    # update database if necessary
    if update_database:
        data_chunks = chunk_text(path_to_textbook_txt,
                                 max_chunk_size,
                                 vector_db,
                                 cosine_similarity_threshold)
        embed_chunks(data_chunks, path_to_textbook_txt, vector_db)

    # retrieve similar chunks to prompt
    retrieved_chunks = retrieve_chunks(prompt, vector_db, n_chunks_to_retrieve)

    # augment prompt
    augmented_prompt = augment_prompt(prompt, retrieved_chunks)

    # generate response
    response = generate_response(augmented_prompt) 

    print(response) 
