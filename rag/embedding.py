import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

def read_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chunks = content.split('=' * 50)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def embed_chunks(chunks, model):
    return model.encode(chunks)

def main():
    input_file = "./chunks/all_chunks.txt"
    embeddings_file = "./embeddings/all_embeddings.npy"

    # Load the model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Read chunks
    chunks = read_chunks(input_file)
    
    # Embed the chunks
    embeddings = embed_chunks(chunks, model)

    # Ensure the output directory exists
    Path(embeddings_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Save embeddings
    np.save(embeddings_file, embeddings)
    
    print(f"Embedded {len(chunks)} chunks")
    print(f"Saved embeddings to {embeddings_file}")

if __name__ == "__main__":
    main()
