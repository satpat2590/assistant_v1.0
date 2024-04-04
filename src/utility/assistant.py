"""
Main file for Assistant Project.
Assistant is initialized through here and then run through it's mental logical flow. 
"""
import ollama 
import pandas as pd
import datetime
from utility.shortmem import ShortMemory

class Assistant():
    def __init__(self):
      # Assistant start time
        self.prog_s = datetime.datetime.now()

      # Memory for the agent
        self.memory = ShortMemory() 

      # System prompt
        self.sys = "My name is Satyam Patel. I am trying to give you limitless memory in an efficient way. Please tell me how I can assist you today. Answer everything brief and concise. Do not express emotions and answer everything straightforwardly."
    def message(self, req: str):
      # Grab the context from the cache logs
        context = self.memory.retrieve()

      # Format the prompt
        prompt = f"""
            {self.sys}
            Based on our previous conversations: {context}
            User has asked: "{req}"
            How should I respond?
        """
      # Get response from LLM by inputting prompt, context, and system commands
        response = ollama.chat(model='llama2', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
      # Store this interaction within the logs
        self.memory.log_interaction(prompt, response['message']['content'])

        self.cognitive_step(req, response['message']['content'])

    def cognitive_step(self, req, step):
      # Grab the context from the cache logs
        context = self.memory.retrieve()

      # Format the prompt
        prompt = f"""
            {self.sys}
            Based on our previous conversations: {context}
            User has asked: "{req}"
            My thoughts on this: "{step}"

            ONLY OUTPUT THE RESPONSE TO THE USER QUERY AND NOTHING MORE
        """
      # Get response from LLM by inputting prompt, context, and system commands
        response = ollama.chat(model='llama2', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        print(response['message']['content'])

    def chat(self):
        prompt = input("> ")
        while prompt != "exit":
            self.message(prompt)
            prompt = input("> ")
        
    