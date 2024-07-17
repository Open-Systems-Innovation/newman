import ollama

class Generator:
    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt
        self.response = ""
    
    def run(self):
        self.response = ollama.generate(model=self.model, prompt=self.prompt)['response']
