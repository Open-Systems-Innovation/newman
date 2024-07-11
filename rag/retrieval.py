import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

class EmbeddingRetriever:
    def __init__(self, embeddings_file, chunks_file, model_name='all-MiniLM-L6-v2'):
        self.embeddings = np.load(embeddings_file)
        self.model = SentenceTransformer(model_name)
        self.index = self._create_index()
        self.chunks = self._load_chunks(chunks_file)

    def _create_index(self):
        dimension = self.embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(self.embeddings)
        return index

    def _load_chunks(self, chunks_file):
        with open(chunks_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return [chunk.strip() for chunk in content.split('=' * 50) if chunk.strip()]

    def retrieve_similar_chunks(self, query, top_k=10):
        query_embedding = self.model.encode([query])[0]
        distances, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
        return [self.chunks[i] for i in indices[0]]

def main():
    embeddings_file = "./embeddings/all_embeddings.npy"
    chunks_file = "./chunks/all_chunks.txt"
    output_file = "./augmented_prompts/augmented_prompts.txt"
    
    retriever = EmbeddingRetriever(embeddings_file, chunks_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        query = "What is the best way to augment the prompt using RAG?"
        similar_chunks = retriever.retrieve_similar_chunks(query)
        augmented_prompt = f"{query}\n\n{' '.join(similar_chunks)}"
        f.write(augmented_prompt + "\n\n")

    print(f"Generated augmented prompts and saved to {output_file}")

if __name__ == "__main__":
    main()
