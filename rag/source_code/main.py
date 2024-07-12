import sys
from vector_database_manager import VectorDatabaseManager
from response_generator import ResponseGenerator

import pdb

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please provide a prompt as a command-line argument.")
        sys.exit(1)
    
    prompt = sys.argv[1]
    n_simliar_results = 10
    
    # create a vector database from the data files
    data_files = "../data/rag"
    vector_database = "./rag_vector_database"
    
    db_manager = VectorDatabaseManager(vector_database, data_files)
    db_manager.process_and_add_paragraphs()

    # query vector database to get top k results
    results = db_manager.collection.query(
        query_texts=[prompt], # chroma will embed this for you
        n_results= n_simliar_results# how many results to return
    )

    # Concatenate the original prompt with the retrieved paragraphs
    augmented_prompt = prompt + "\n\n"
    for result in results["documents"][0]:
        augmented_prompt += result + "\n\n"
    
    response_generator = ResponseGenerator()
    response_generator.run(augmented_prompt)
