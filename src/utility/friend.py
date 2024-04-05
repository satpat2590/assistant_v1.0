"""
Main file for Assistant Project.
Assistant is initialized through here and then run through it's mental logical flow. 
"""
import ollama 
import pandas as pd
import datetime
from utility.shortmem import ShortMemory
from colorama import init, Fore, Back, Style 
init(autoreset=True)

# Define ANSI escape codes for colors and styles
class Colors:
    RED = '\033[31m'  # Red text
    GREEN = '\033[32m'  # Green text
    YELLOW_BACKGROUND = '\033[43m'  # Yellow background
    BOLD = '\033[1m'  # Bold text
    RESET = '\033[0m'  # Reset to default

# Function to highlight specific parts of text
def highlight_text(highlight, color):
    return f"{color} {highlight} {Colors.RESET}"

# Example usage
message = "Warning: This action cannot be undone."
highlighted_message = highlight_text("Warning:", Colors.RED + Colors.BOLD + Colors.YELLOW_BACKGROUND)
print(highlighted_message)

class Friend():
    def __init__(self):
      # Assistant start time
        self.prog_s = datetime.datetime.now()

      # Memory for the agent
        self.memory = ShortMemory()

      # System prompt
        self.sys = """
          You will be given the following: [CONTEXT] and a [PROMPT]. 
          Your goal is to use the context to answer the prompt. 

          The [CONTEXT] will show previous chat logs (or previous interactions between us). 
          This will aid in giving you memory as to what happened in our discussion so far. 
          They are all stored in a Python dictionary with the following keys [timestamp, query, response], where query is [PROMPT] and response is what you answer with. 

          You will act however you wish, but be sure to answer all of the questions and concerns of the user's [PROMPT] precisely. 
          If you do not know what the [PROMPT] means, then be sure to ask so that the user can clarify and reaffirm their [PROMPT]. 
        """
    def message(self, req: str):
      # Grab the context from the cache logs
        context = self.memory.retrieve()

      # Format the prompt
        prompt = f"""
            {self.sys}


            [CONTEXT]: {context}
            
            [PROMPT]: {req}

            Think on this. How should I respond? What would make the best response?  
        """
      # Get response from LLM by inputting prompt, context, and system commands
        response = ollama.chat(model='llama2-uncensored', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        print(f"\nThoughts >  {response['message']['content']}\n")
        self.cognitive_step(req, response['message']['content'])

    def cognitive_step(self, req, step):
      # Grab the context from the cache logs
        context = self.memory.retrieve()

      # Format the prompt
        prompt = f"""
            {self.sys}

            [THOUGHTS] is what you thought would make the best response to the [PROMPT].

            You must use your [THOUGHTS] to respond.   


            [CONTEXT]: {context}

            [PROMPT]: {req}

            My thoughts on this: {step}

            Use your [THOUGHTS] to respond to the [PROMPT]. Remember, you are speaking to the user now. 
        """
      # Get response from LLM by inputting prompt, context, and system commands
        response = ollama.chat(model='llama2', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        print(f"\nLLM > {response['message']['content']}")
      # Store this interaction within the logs
        self.memory.log_interaction(req, response['message']['content'])

    def chat(self):
        print("\n")
        prompt = input("> ")
        while prompt != "exit":
            self.message(prompt)
            print("\n")
            prompt = input("> ")
        
    