# Discord Waifu Bot 

This is a simplified example of a discord bot that can easily be deployed on fly.io & respond directly to users in a server

## Setup 

Install dependencies 

can be done with poetry 

```
poetry install
```

Once done run 

```
poetry shell
```

You can test out the bots responses by running 

```
python3 localTest.py
```

### Setting up discord bot 

To setup discord bot you can follow instructions here : https://discordpy.readthedocs.io/en/stable/discord.html


## Config 

You can edit the config.json file to change the models, number of examples, etc.
Additionally you'll need to setup the .env file with the correct API keys.

The persona.py file contains the persona of the bot - this is used for the bot to be able to respond in character 

### Notes

For bots to work well specific examples can be provided in interest variable of persona.py 
for example excerpts from whitepaper / specific explanations of technical concepts can be added to make the bot more accurate 

## Hosting 

The bot can be hosted via fastAPI 

to test locally run 

```
fastapi dev
```

Additionally you can host simply on fly.io using 

fly launch 

Simple walkthough here : https://fly.io/docs/python/

## Context 

Custom context can be added using addDataSimple.py 
This will load context to the local chromadb database & can be fetched by the bot during conversations 

Additinally some simple logic is implemented in helpers.py to fetch conversational history between users & maintain a history of interactions

