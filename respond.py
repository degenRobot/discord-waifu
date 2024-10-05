from openai import OpenAI
import os
from dotenv import load_dotenv
import chromadb
import random
import json
from helpers import get_embeddings
import persona
useTogether = True

load_dotenv()
chroma_db_path = os.path.join(os.getcwd(), "chromadb")

chroma = chromadb.PersistentClient(path=chroma_db_path)
# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url=persona.openRouterUrl,
  api_key=os.getenv("OPENROUTER_API_KEY")

)

together_client = OpenAI(
  base_url=persona.togetherUrl,
  api_key=os.getenv("TOGETHER_API_KEY")
)

def getExampleMessages():

    #Load 5 Random examples from json 
    samples = "/n Below are some examples of some previous messages you sent - use these to help style your response. Note these cover a wide range of topics. Examples : "
    loadedExamples = json.load(open("exampleMessages.json"))
    nExamples = 10
    for i in range(nExamples):
        samples += random.choice(loadedExamples["messages"])

    return samples

def create_prompt(message, context, sender, additional_context=""):
    samples = getExampleMessages()

    
    return context + samples + additional_context + "\n" + "###Reply to the following message from " + sender + " : " + message + "\n" + "Stay in Character. Keep your response short & concise\n"



def openRouterCompletion(prompt, model = persona.openRouterModel):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": prompt,
            },
        ],
        max_tokens=1000
    )
    return completion.choices[0].message.content


def togetherCompletion(prompt, model = persona.togetherModel):
    completion = together_client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": prompt,
            },
        ],
        max_tokens=1000
    )

    return completion.choices[0].message.content


def get_response(message, context, sender, model="openai/gpt-3.5-turbo", fetch_context=False):
    #additional_context = fetch_context(message)

    prompt = create_prompt(message, context, sender)
    prompt += "###Your Response : "
    try : 
        completion = openRouterCompletion(prompt)
    except Exception as e:
        print(e)
        completion = togetherCompletion(prompt)

    if completion:
        return completion
    else:
        return "I'm broken uWu feed me more rice plz"