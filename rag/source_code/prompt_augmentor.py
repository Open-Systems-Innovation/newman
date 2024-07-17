# prompt_utils.py

class PromptAugmentor:
    def __init__(self, max_chunks=10):
        self.max_chunks = max_chunks
    
    def create_augmented_prompt(self, prompt, results):
        augmented_prompt = f"{prompt}\n\nRelevant Information:\n"
        
        used_sources = {}
        chunk_count = 0
        
        # Sort results by relevance score if available
        sorted_results = self._sort_results(results)
        
        for result, metadata, id, score in sorted_results:
            if chunk_count >= self.max_chunks:
                break
            
            source = metadata["source"]
            chunk_id = id.split('_')[-1]  # Assuming id format is "source_chunknum"
            # Add chunk to augmented prompt with metadata
            augmented_prompt += f"[{chunk_count + 1}] (Source: {source}, Chunk: {chunk_id}, Relevance: {1 - score:.2f})\n{result}\n\n"
            
            if source not in used_sources:
                used_sources[source] = []
            used_sources[source].append(chunk_id)
            
            chunk_count += 1
        
        # Add instruction for using the information
        augmented_prompt += "\nBased on the above information and your own knowledge of the subject, please answer the following question. If the information provided is insufficient, please state so.\n\n"
        augmented_prompt += f"Question: {prompt}\n\nAnswer:"
        
        # Print references used
        self._print_references(used_sources)
        
        return augmented_prompt
    
    def _sort_results(self, results):
        return sorted(zip(results["documents"][0], results["metadatas"][0], results["ids"][0], results.get("distances", [[1]] * len(results["documents"][0]))[0]), 
                      key=lambda x: x[3])  # Sort by distance/score
    
    def _print_references(self, used_sources):
        print("\nReferences used:")
        for source, chunks in used_sources.items():
            print(f"{source}: chunks {', '.join(chunks)}")

# Example usage
if __name__ == "__main__":
    # Example data
    prompt = "What is the capital of France?"
    results = {
        "documents": [["Paris is the capital of France.", "France is a country in Europe."]],
        "metadatas": [[{"source": "Wikipedia"}, {"source": "Britannica"}]],
        "ids": [["Wikipedia_0", "Britannica_1"]],
        "distances": [[0.1, 0.2]]
    }
    
    augmentor = PromptAugmentor()
    augmented_prompt = augmentor.create_augmented_prompt(prompt, results)
    print(augmented_prompt)
