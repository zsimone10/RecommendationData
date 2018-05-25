import requests
import json
from flask import Flask, request
import random
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = "EAAEnRScMXk8BAJOlhar5dvtZB7UkKIXCcylgPzDMSgEaTFBC3f0M6EOUbn2vtGH90YDd5nCmGKZCUZArJOk5NZCdMWJtPZCz68W8F6C2UlCU9UM9vS14wUdck9zxp1WL3hoxZCIpUo0W3gBAANZCsVT7cb0gfZCpxUC6ZBnxe8TNjALwOKJV1knQv"

VERIFY_TOKEN = 'testtest'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    print recipient_id
    resp = requests.get("https://graph.facebook.com/v2.6/{}?fields=first_name,last_name,locale,gender,last_ad_referral,profile_pic&access_token={}".format(recipient_id, ACCESS_TOKEN))
    data = resp.json() #contains basic info
    print data
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
