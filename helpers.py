from typing import List
from together import Together
from dotenv import load_dotenv
import os
import persona
import chromadb
import random

chroma_db_path = os.path.join(os.getcwd(), "chromadb")
chroma = chromadb.PersistentClient(path=chroma_db_path)

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

togetherClient = Together()

def get_embeddings(texts: List[str], model: str) -> List[List[float]]:
    texts = [text.replace("\n", " ") for text in texts]
    outputs = togetherClient.embeddings.create(model=model, input=texts)
    return [outputs.data[i].embedding for i in range(len(texts))]

def log_message(message, response, user, channel, timestamp) : 
    # Here we want to log message into Chroma 
    # Meta Data should include user, channel, timestamp, message, etc. 
    chroma_db_path = os.path.join(os.getcwd(), "chromadb")
    chroma = chromadb.PersistentClient(path=chroma_db_path)
    collection = chroma.get_or_create_collection(user + "messages")

    input = user + " : " + message + " \n" + "your response : " + response

    collection.add(documents=[input], metadatas=[{"user": user, "channel": channel, "timestamp": str(timestamp)}], ids=[str(timestamp)])


def fetch_history(user, maxLength=500):
    chroma_db_path = os.path.join(os.getcwd(), "chromadb")
    chroma = chromadb.PersistentClient(path=chroma_db_path)
    
    col_exists = True
    try:
        coll =  chroma.get_collection(user + "messages")
    except:
        col_exists = False
    
    # Check if collection exists
    if col_exists:

        collection = chroma.get_or_create_collection(user + "messages")
        
        # Get all documents from the collection
        info = collection.get()
        documents = info["documents"]
        if (len(documents) == 0):
            return ""
        # Concatenate all documents into a single string
        histInstr = "\nUse this history to help inform your response. "
        chat_history_string = "History of previous conversation with " + user + histInstr + " : \n"
        for doc in documents:
            chat_history_string += doc + "\n"
            print(doc)

        if (len(chat_history_string) > maxLength):
            chat_history_string = chat_history_string[-maxLength:]
        return chat_history_string
    else:
        return ""


def fetch_context(message):
    ### Here we want to fetch any other relevant context from vector DB 
    try : 
        collection = chroma.get_or_create_collection("Rise")

        embedding = get_embeddings([message], model='togethercomputer/m2-bert-80M-8k-retrieval')

        results = collection.query(query_embeddings=embedding, n_results=1)
        docs = results['documents'][0]
        
        context = "Here is some additional context from either the Rise Whitepaper or Articles : \n"
        for doc in docs: 
            context += doc + "\n"

    except Exception as e:
        context = ""
            #print(doc)
    return context


#context = "You are : " + background + ". you have the following personality : " + personality + ", you have the following interest : " + interest +", you have the following way of responding : " + speach
def get_context(message, fetchAdditionalContext=True):
    if fetchAdditionalContext:
        additional_context = fetch_context(message)
    else:
        additional_context = ""
    persona = random.choice(persona.personas)
    context = "You are : " + persona.background + ". you have the following personality : " + persona.personality + persona + ", you have the following interest : " + persona.interest + additional_context + ", you have the following way of responding : " + persona.speech

    nPhrases = 3
    phrases = random.sample(persona.phrases, nPhrases)
    context += "\nHere are some example phrases that you can use to help respond : " + str(phrases) + "\n"
    context += "Note - use the above phrases as a guide, feel free to ignore them if you don't want to use them."


    return context


    




