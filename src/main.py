"""
Main script for running the assistant and all of the logic behind it's 'thinking'
"""
from utility.assistant import Assistant

if __name__ == "__main__":
    buddy = Assistant() 
    buddy.chat()
