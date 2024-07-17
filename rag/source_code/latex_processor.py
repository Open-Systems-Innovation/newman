import re
from pathlib import Path
from pylatexenc.latex2text import LatexNodes2Text

class LatexProcessor:
    def __init__(self):
        self.latex_content = ""
        self.chunks = []

    def read_document(self, document_path):
        with open(document_path, 'r') as file:
            self.latex_content = file.read()

    def extract_abstract(self):
        abstract_match = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', self.latex_content, re.DOTALL)
        if abstract_match:
            return abstract_match.group(1).strip()
        return ""

    def extract_sections(self):
        sections = re.split(r'\\section{', self.latex_content)[1:]
        section_texts = []
        for section in sections:
            section_title, section_body = section.split('}', 1)
            section_texts.append((section_title.strip(), section_body.strip()))
        return section_texts

    def latex_to_text(self, latex_content):
        return LatexNodes2Text().latex_to_text(latex_content)

    def chunk_text(self, text, chunk_size=512):
        words = text.split()
        return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    def process_document(self, document_path, chunk_size=512):
        self.read_document(document_path)

        self.chunks = []  # Clear previous chunks

        # Extract and process abstract
        abstract = self.extract_abstract()
        if abstract:
            abstract_text = self.latex_to_text(abstract)
            self.chunks.append(abstract_text)

        # Extract and process sections
        sections = self.extract_sections()
        for title, body in sections:
            plain_text = self.latex_to_text(body)
            section_chunks = self.chunk_text(plain_text, chunk_size)
            self.chunks.extend(section_chunks)

        return self.chunks

if __name__ == "__main__":
    data_path = Path("../data/")
    latex_processor = LatexProcessor()
    for tex_file in data_path.glob('*.tex'):
        chunks = latex_processor.process_document(tex_file)
        print(f"Document: {tex_file}")
        for idx, chunk in enumerate(chunks):
            print(f"Chunk {idx + 1}:\n{chunk}\n")
