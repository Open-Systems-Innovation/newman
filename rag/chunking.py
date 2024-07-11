import re
from pathlib import Path

def read_latex_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_paragraphs(latex_content):
    latex_content = re.sub(r'%.*$', '', latex_content, flags=re.MULTILINE)
    latex_content = re.sub(r'\\[a-zA-Z]+(\[.*?\])?(\{.*?\})?', '', latex_content)
    latex_content = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', '', latex_content, flags=re.DOTALL)
    paragraphs = re.split(r'\n\s*\n', latex_content)
    return [p.strip() for p in paragraphs if p.strip()]

def create_chunks(paragraphs, max_chunk_size=1000, overlap=100):
    chunks = []
    current_chunk = ""
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= max_chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
            if chunks and len(chunks[-1]) > overlap:
                current_chunk = chunks[-1][-overlap:] + current_chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def process_tex_files(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    all_chunks = []
    for tex_file in input_path.glob('*.tex'):
        latex_content = read_latex_file(tex_file)
        paragraphs = extract_paragraphs(latex_content)
        chunks = create_chunks(paragraphs)
        all_chunks.extend(chunks)

        # Save individual file chunks
        file_chunks_path = output_path / f"{tex_file.stem}_chunks.txt"
        with open(file_chunks_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(f"Chunk {i}:\n{chunk}\n\n{'='*50}\n\n")

    # Save all chunks to a single file
    all_chunks_path = output_path / "all_chunks.txt"
    with open(all_chunks_path, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(all_chunks, 1):
            f.write(f"Chunk {i}:\n{chunk}\n\n{'='*50}\n\n")

    print(f"Processed {len(list(input_path.glob('*.tex')))} files")
    print(f"Created {len(all_chunks)} total chunks")
    print(f"Saved all chunks to {all_chunks_path}")

if __name__ == "__main__":
    process_tex_files("./data", "./chunks")
