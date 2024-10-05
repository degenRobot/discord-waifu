import chromadb
import os
from typing import List
from together import Together
import json
import time

from helpers import get_embeddings

from dotenv import load_dotenv

with open('tech/context.json', 'r') as data:
    docs= json.load(data)


load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Use a writable directory in the user's home folder
chroma_db_path = os.path.join(os.getcwd(), "chromadb")
client = chromadb.PersistentClient(path=chroma_db_path)
togetherClient = Together()

maxLen = 1000
overlap = 400

#txts = []
ids = []
metadata = []

fileName = "Tech"
collectionName = "Rise"
#print(txts[0])

### Loop through the txts and get embeddings
embeddings = []
inputTxts = []
finalTxts = []
print("Getting embeddings for : " + fileName)

while (len(info) > maxLen):
    inputTxts.append(info[0:maxLen])
    info = info[overlap:]

print(len(inputTxts))


for i in range(len(inputTxts)):
    try : 
            #print(txts[i]) 
            newEmbeddings = get_embeddings([inputTxts[i]], model='togethercomputer/m2-bert-80M-8k-retrieval')
            # Note some txts may fail to embed i.e. empty strings 
            #ids.append(fileName + str(i))
            embeddings = embeddings + newEmbeddings
            finalTxts.append(inputTxts[i])
    except : 
        time.sleep(1)
        print("API Failed")
        print(inputTxts[i])
        print("Retrying")



ids = [fileName + str(i) for i in range(len(finalTxts))]
try : 
    collection = client.get_collection(collectionName)
except :
    collection = client.create_collection(collectionName)


collection.add(
    embeddings=embeddings,
    documents=finalTxts,
    ids = ids
)
print("Added Data : " + collectionName)


