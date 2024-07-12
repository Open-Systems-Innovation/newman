import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from latex_processor import LatexProcessor

def test_latex_to_text(data_folder):
    error_log = open('error_log.txt', 'w')
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, 'paragraph_chunks')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    latex_processor = LatexProcessor()
    for filename in os.listdir(data_folder):
        print(f"testing file {filename}")
        if filename.endswith(".tex"):
            file_path = os.path.join(data_folder, filename)
            try:
               paragraphs = latex_processor.process_document(file_path)
               output_file_name = os.path.splitext(filename)[0] + '.txt'
               output_file_path = os.path.join(output_dir, output_file_name)
               with open(output_file_path, 'w') as output_file:
                   for paragraph in paragraphs:
                       output_file.write(paragraph + '\n' + '=' * 50 + '\n')
            except Exception as e:
                error_log.write(f"Error processing {filename}: {str(e)}\n")
    error_log.close()

test_latex_to_text('../../data/rag')
