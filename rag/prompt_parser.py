import sys
import os

class PromptParser:
    def __init__(self, arguments):
        self.arguments = arguments
        self.prompt = ""
        self.sanitize_input()
        self.extract_prompt()

    def sanitize_input(self):
        # make sure a prompt (or prompt .txt file) was given
        if len(self.arguments) < 2:
            print("Please provide a prompt or a .txt file as the first command-line argument.")
            sys.exit(1)

    def extract_prompt(self):
        # Check if the first argument is a file
        if os.path.isfile(self.arguments[1]) and self.arguments[1].endswith('.txt'):
            # if so, set the prompt to be its conents
            with open(self.arguments[1], 'r') as file:
                self.prompt = file.read()
        else:
            # otherwise, let the prompt be the string that is passed
            self.prompt = arguments[1]

 
    
