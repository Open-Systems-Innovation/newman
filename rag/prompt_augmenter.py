class PromptAugmentor:
    def __init__(self, prompt, retrieved_chunks):
        self.prompt = prompt
        self.retrieved_chunks = retrieved_chunks
        self.augmented_prompt = ""
        self.used_sources = ""
        self.create_augmented_prompt()
        
    def create_augmented_prompt(self):
        augmented_prompt = f"{self.prompt}\n\nRelevant Information:\n"
        
        used_sources = {}
        chunk_count = 0
        
        # Sort results by relevance score if available
        sorted_chunks = self._sort_results(self.retrieved_chunks)
        
        for result, metadata, id, score in sorted_chunks:
            source = metadata["source"]
            chunk_id = id.split('_')[-1]  # Assuming id format is "source_chunknum"
            # Add chunk to augmented prompt with metadata
            augmented_prompt += f"[{chunk_count + 1}] (Source: {source}, Chunk: {chunk_id}, Relevance: {1 - score:.2f})\n{result}\n\n"
            
            if source not in used_sources:
                used_sources[source] = []
            used_sources[source].append(chunk_id)
            
            chunk_count += 1

        # add sources to list
        self.used_sources = used_sources
        
        # Add instruction for using the information
        augmented_prompt += "\nBased on the above information and your own knowledge of the subject, please answer the following question. If the information provided is insufficient, please state so.\n\n"
        augmented_prompt += f"Question: {self.prompt}\n\nAnswer:"
        
        self.augmented_prompt = augmented_prompt
        
    def _sort_results(self, results):
        return sorted(zip(results["documents"][0], results["metadatas"][0], results["ids"][0], results.get("distances", [[1]] * len(results["documents"][0]))[0]), 
                      key=lambda x: x[3])  # Sort by distance/score
    
 
