import re
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Chunker:
    def __init__(self, path_to_textbook_txt, max_chunk_size, vector_db, similarity_threshold ):
      self.path_to_textbook_txt = path_to_textbook_txt 
      self.max_chunk_size = max_chunk_size
      self.vector_db = vector_db
      self.similarity_threshold = similarity_threshold
      self.chunks = []
      self.raw_text = ""
      self.sentences = []
      self.source_name = ""
      self.get_source_name()
      self.get_raw_text()
      self.parse_sentences()
      self.sentence_ids = [f"{self.source_name}_{i}" for i in range(len(self.sentences))]
      self.sentence_metadatas = [{"source": self.source_name} for _ in self.sentences]
      self.create_semantic_chunks()

    def get_raw_text(self):
        with open(self.path_to_textbook_txt, 'r') as file:
            self.raw_text = file.read()

    def get_source_name(self):
        # Get the base name (filename with extension) from the path
        base_name = os.path.basename(self.path_to_textbook_txt)
        # Remove the file extension
        name_without_extension = os.path.splitext(base_name)[0]
        self.source_name = name_without_extension

    def parse_sentences(self):
        # Preprocess the text to handle newlines and other issues
        processed_text = self.raw_text.replace('\n', ' ').replace('\r', '')
        
        # Use regular expressions to split the text into sentences
        sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
        sentences = sentence_endings.split(processed_text)

        # Strip leading and trailing spaces from each sentence
        self.sentences = [sentence.strip() for sentence in sentences if sentence]

    def create_semantic_chunks(self):
        print(f"length of sentences is: {len(self.sentences)}")
        self.embed_sentences()
        sentence_id = 0
        while sentence_id < len(self.sentences)-1:
            current_chunk = ""
            character_count = 0
            while character_count < self.max_chunk_size: 
                if sentence_id >= len(self.sentences)-1:
                    break
                current_chunk += self.sentences[sentence_id]
                character_count += len(self.sentences[sentence_id])
                embedding_1 = self.get_embedding_vector(sentence_id)
                embedding_2 = self.get_embedding_vector(sentence_id + 1)
                similarity_value = self.cosine_similarity(embedding_1, embedding_2)
                if similarity_value > self.similarity_threshold:
                    sentence_id += 1
                    continue
                else:
                    self.chunks.append(current_chunk)
                    sentence_id += 1
                    current_chunk = ""
                    break

    def get_embedding_vector(self, sentence_number):
         return self.vector_db.sentence_collection.get(ids=f"{self.source_name}_{sentence_number}",
                                                   include = ['embeddings'])['embeddings'][0]

    def embed_sentences(self):
        # Add sentences to the Chroma sentence_collection
        self.vector_db.sentence_collection.add(
            documents=self.sentences,
            ids=self.sentence_ids,
            metadatas= self.sentence_metadatas
            )

    def cosine_similarity(self, embedding_1, embedding_2):
        return np.dot(embedding_1, embedding_2) / (np.linalg.norm(embedding_1) * np.linalg.norm(embedding_2))
