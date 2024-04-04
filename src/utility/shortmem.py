import os
import datetime
import json

class ShortMemory():
    def __init__(self):
        logp = os.path.join(os.getcwd(), "log")

        if not os.path.exists(logp):
            os.makedirs(logp, exist_ok=True)
        
        self.log = logp

        # Grab current date to create file
        self.currfile = os.path.join(self.log, f"{datetime.datetime.now().strftime('%Y%m%d')}.hap.log")

        if not os.path.exists(self.currfile):
            with open(os.path.join(self.log, self.currfile), 'w') as cf:
                pass 
        else:
            print(f"\n[SMEMORY] {datetime.datetime.now()} {self.currfile} exists already!")
    
    def log_interaction(self, query: str, response: str):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(), 
            "query": query,
            "response": response
        }
        with open(self.currfile, "a") as lf:
            lf.write(json.dumps(log_entry) + "\n")
    
    def retrieve(self):
        interactions = []
        with open(self.currfile, 'r') as file:
            for line in file:
                try:
                    interaction = json.loads(line)
                    interactions.append(interaction)
                except json.JSONDecodeError:
                    print("Error decoding JSON from:", line)
        return interactions



        