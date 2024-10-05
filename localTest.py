from respond import get_response
from helpers import log_message, fetch_history, get_context

sender = "Matt"

print("### Response ###")
#print(get_response(inputMessage, context, sender, model="meta-llama/llama-3.1-8b-instruct:free"))

testModel = "microsoft/wizardlm-2-8x22b"

while True:
    inputMessage = input("Enter a message: ")



    context = get_context(inputMessage, fetchAdditionalContext=True)
    context += fetch_history(sender)
    response = get_response(inputMessage, context, sender, model=testModel)
    print("### Response ###")
    print(response)
    #await message.channel.send(response)
    log_message(inputMessage, response, "TESTING","TEST","TEST")
