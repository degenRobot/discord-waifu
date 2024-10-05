import discord
import os
from dotenv import load_dotenv
from respond import get_response
import json
from fastapi import FastAPI
import chromadb

from helpers import fetch_history, log_message, fetch_context, get_context
import persona

app = FastAPI()

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@app.get("/")
async def hello_fly():
    return 'hello from fly.io'

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):

    if bot.user.mentioned_in(message):
        
        print("Message received" + message.content)
        #print(config.context)
        try : 

            context = get_context(message.content, fetchAdditionalContext=True)
            context += fetch_history(message.author.display_name)
            response = get_response(message.content, context, message.author.display_name)
            #print(response)
            #print(message.channel.name)
            await message.channel.send(response)
        except Exception as e:
            print(e)


        try : 
            log_message(message.content, response, message.author.display_name, message.channel.name, message.created_at)
        except Exception as e:
            print(e)
	# if message.content == "hello":
	# 	# SENDS BACK A MESSAGE TO THE CHANNEL.
	# 	await message.channel.send("hey dirtbag")

bot.run(DISCORD_TOKEN)