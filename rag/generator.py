import ollama

class Generator:
    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt
        self.response = ""
    
    def run(self, augmented_prompt):
        self.response = ollama.generate(model='llama3', prompt=augmented_prompt)
