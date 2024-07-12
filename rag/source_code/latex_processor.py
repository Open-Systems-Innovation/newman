import re
from pathlib import Path
from pylatexenc.latex2text import LatexNodes2Text

class LatexProcessor:

    def read_latex_file(self, file_path):
        """
        Reads the content of the LaTeX file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def extract_paragraphs(self, latex_content):
        min_character_length = 100

        try:
            # Convert LaTeX content to plain text
            parsed_text = LatexNodes2Text().latex_to_text(latex_content)
        except Exception as e:
            print(f"An error occurred while parsing LaTeX content: {e}")
            return []
        
        # Split text into paragraphs based on double line breaks
        paragraphs = re.split(r'\n\s*\n', parsed_text)
        
        # Filter paragraphs longer than min_character_length
        paragraphs = [par.strip() for par in paragraphs if len(par.strip()) > min_character_length]
        #breakpoint()

        return paragraphs

    def process_document(self, file_path):
        """
        Processes the LaTeX file, extracting paragraphs.
        """
        latex_content = self.read_latex_file(file_path)
        paragraphs = self.extract_paragraphs(latex_content)
        return paragraphs

    
if __name__ == "__main__":
    document_path = "../data/RAG_FACTS_NVIDIA.tex"
    processor = LatexProcessor(document_path)
    processor.process_document()
