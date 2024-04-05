import os
import re
import datetime
import json
import pandas as pd
from pandas.errors import EmptyDataError

class ShortMemory():
    def __init__(self):
        logp = os.path.join(os.getcwd(), "log")

        if not os.path.exists(logp):
            os.makedirs(logp, exist_ok=True)
        
        self.log = logp

        # Grab current date to create file
        self.currfile = os.path.join(self.log, f"{datetime.datetime.now().strftime('%Y%m%d')}.hap.log")

        if not os.path.exists(self.currfile):
            pd.DataFrame(columns=['Timestamp', 'Prompt', 'Response']).to_csv(self.currfile, mode='w', header=True, index=False)
    
    def clean_text(self, text): 
        ctext = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        ctext = re.sub(' +', ' ', ctext) 
        return ctext
    
    def log_interaction(self, query: str, response: str):
        logdf = pd.DataFrame([(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.clean_text(str(query)), self.clean_text(response))], columns=['Timestamp', 'Prompt', 'Response'])
        logdf.to_csv(self.currfile, mode='a', header=False, index=False)
    
    def retrieve(self):
        try:
            df = pd.read_csv(self.currfile)
            formatted_text = ''
            if not df.empty:
                for index, row in df.iterrows():
                    text_chunk = f"{row['Timestamp']}: Prompt: {row['Prompt']} - Response: {row['Response']}\n"
                    formatted_text += text_chunk
                return formatted_text
            else:
                return ""
        except EmptyDataError:
            return ""
    
if __name__ == "__main__":
    memory = ShortMemory()
    memory.retrieve()



        