import sys
import os

import chromadb

from prompt_parser import PromptParser
from vector_database_manager import VectorDatabaseManager
from chunker import Chunker
from embedder import Embedder
from prompt_augmenter import PromptAugmentor
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
    retrieved_chunks = vector_db.chunk_collection.query(
        query_texts = [prompt],
        n_results = n_chunks_to_retrieve
        )
    return retrieved_chunks

def augment_prompt(prompt, retrieved_chunks):
    prompt_augmentor = PromptAugmentor(prompt, retrieved_chunks)
    return prompt_augmentor.augmented_prompt

def generate_response(llm_model, augmented_prompt):
    response_generator = Generator(llm_model, augmented_prompt)
    response_generator.run()
    return response_generator.response


if __name__ == "__main__":
    # TO BUILD THE TXT from PDF
    # pdftotext -x 0 -y 57 -W 612 -H 655 argonne-2024-petsc-toa-users-manual.pdf testing.txt

    # SET PARAMETERS
    n_chunks_to_retrieve = 20  # set the number of chunks to retrieve
    path_to_textbook_txt = "../data/develop/petsc-users-manual-2024.txt" 
    vector_database_path = "./vector_databases/petsc_textbook"
    vector_database_name = "petsc_textbook"
    embedding_model = "all-MiniLM-L6-v2"
    max_chunk_size = 2506 # max chunk size in characters
    cosine_similarity_threshold = 0.4
    llm_model = "llama3"
    
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
        breakpoint()
        embed_chunks(data_chunks, path_to_textbook_txt, vector_db)

    # retrieve similar chunks to prompt
    retrieved_chunks = retrieve_chunks(prompt, vector_db, n_chunks_to_retrieve)

    # augment prompt
    augmented_prompt = augment_prompt(prompt, retrieved_chunks)

    # generate response
    response = generate_response(llm_model, augmented_prompt) 

    print(response) 
