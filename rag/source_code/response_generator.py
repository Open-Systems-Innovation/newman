import ollama

class ResponseGenerator:

    def run(self, augmented_prompt):
        response = ollama.generate(model='llama3', prompt=augmented_prompt)
        print(response["response"])


if __name__ == "__main__":
    augmented_prompt = "This is a sample augmented prompt."
    generator = ResponseGenerator()
    generator.run(augmented_prompt)
