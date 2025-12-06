import json
import random

def getQuote():
    with open("quotes.json","r",encoding='utf-8') as file:
        quotes = json.load(file)
    with open("quotehistory.txt","a+") as f2:
        f2.seek(0)
        line_count=0
        for i in f2:
            line_count+=1
        if line_count==14:
            f2.seek(0)
            f2.readline()
            temp=f2.read()
            f2.truncate(0)
            f2.seek(0)
            f2.write(temp)
        r=random.randint(0,2500)
        while str(r) in f2:
            r=random.randint(0,2500)
    
        f2.write(f"{r}\n")
        #print(quotes[r]["quote"])
        #print(quotes[r]["author"])
        return quotes[r]