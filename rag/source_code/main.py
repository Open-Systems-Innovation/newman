import sys
import os
from vector_database_manager import VectorDatabaseManager
from response_generator import ResponseGenerator

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide a prompt or a .txt file as a command-line argument.")
        sys.exit(1)

    prompt = ""
    input_arg = sys.argv[1]

    # Check if the argument is a file
    if os.path.isfile(input_arg) and input_arg.endswith('.txt'):
        with open(input_arg, 'r') as file:
            prompt = file.read()
    else:
        prompt = input_arg

    n_similar_results = 10
    
    # Set paths
    data_files = "../data/fem"
    vector_database = "./fem_vector_database"
    
    # Check for command line arguments
    update_database = "-update-database" in sys.argv
    print_prompt = "-print-prompt" in sys.argv
    
    # Initialize database manager
    db_manager = VectorDatabaseManager(vector_database, data_files)
    
    # Create or update database if flag is present, or if the database doesn't exist
    if update_database or not os.path.exists(vector_database):
        print("\nCreating/Updating database...")
        db_manager.process_and_add_paragraphs()
    else:
        print("\nUsing existing database...")
    
    # Query vector database to get top k results
    results = db_manager.collection.query(
        query_texts=[prompt],
        n_results=n_similar_results
    )

    # Concatenate the original prompt with the retrieved paragraphs
    augmented_prompt = prompt + "\n\n"
    
    print("\nReferences used:")
    used_sources = {}
    for result, metadata, id in zip(results["documents"][0], results["metadatas"][0], results["ids"][0]):
        augmented_prompt += result + "\n\n"
        source = metadata["source"]
        chunk_id = id.split('_')[-1]  # Assuming id format is "source_chunknum"
        
        if source not in used_sources:
            used_sources[source] = []
        used_sources[source].append(chunk_id)

    for source, chunks in used_sources.items():
        print(f"- {source}: chunks {', '.join(chunks)}")
    
    # Print the augmented prompt if the flag is present
    if print_prompt:
        print("\nAugmented Prompt:")
        print(augmented_prompt)
    
    print("\nGenerating response...")
    response_generator = ResponseGenerator()
    response_generator.run(augmented_prompt)
