import ollama

def generate_response(augmented_prompt):
    # Generate a response using Llama3
    response = ollama.generate(model='llama3', prompt=augmented_prompt)
    print(response["response"])

def main():
    input_file = "./augmented_prompts/augmented_prompts.txt"
    output_file = "./generated_responses/generated_responses.txt"

    with open(input_file, 'r', encoding='utf-8') as f:
        augmented_prompt = f.read()

    with open(output_file, 'w', encoding='utf-8') as f:
        response = generate_response(augmented_prompt)
            #f.write(response + "\n\n")

    print(f"Generated responses and saved to {output_file}")

if __name__ == "__main__":
    main()
