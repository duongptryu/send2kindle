from fastapi import FastAPI, Request, Response, HTTPException, status, Header, BackgroundTasks, Body
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
import logging

from model import User
from functions.search import search
from functions.registration import registration_update
from functions.download import pre_download
from functions.guide import guide
from functions.process_file_send_by_user import process

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from viberbot.api.viber_requests import ViberDeliveredRequest
from viberbot.api.viber_requests import ViberSeenRequest

app = FastAPI()

viber = Api(
    BotConfiguration(
        name='PythonSampleBot',
        avatar='http://site.com/avatar.jpg',
        auth_token='4cf24aa8c427dec0-fdf401a1da0b2abb-c74184dd9ac8b1c'))

message_guide = '''
    Welcome 🦠🦠🦠! ✨
This bot can send files to your Kindle.
The maximum file size is 50 MB.

1️⃣ Setup your Kindle account with this command:
/email YourEmail@kindle.com

2️⃣ Go to your Amazon account → Preferences tab → Personal Document Settings and add duongptryu@gmail.com to approved e-mail list (no mistake, you need to approve the whole domain)

👆 This is necessary step to allow your Kindle account to receive files!

3️⃣ All set up! 🎉

This bot support extension .pdb, .mobi, .asw3 and .epub. 

Syntax
1. Help: /help
2. Registration/ update mail: /mail your_kindl_email@kindle.com
4. Type and send message to search book
5. Download book: Click GET button

    
    '''

logger = logging.getLogger()

err_message = "Incorrect syntax, using '/help' to help"


@app.post('/')
async def incoming(request: Request, response: Response, sig: str,
                   background_tasks: BackgroundTasks):
    data = await request.body()
    logger.debug("received request. post data: {0}".format(data))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(data, sig):
        response.status_code = 403
        return response

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(data)

    if isinstance(viber_request, ViberMessageRequest):
        try:
            if viber_request.message.media:
                background_tasks.add_task(process,viber, viber_request)
        except:
            message = viber_request.message.text
            # check message
            syntax = message.split(" ")
            command_list = ["/help", "/email", "/GET"]
            if syntax[0].lower() in command_list:
                if syntax[0].lower() == "/help":
                    guide(viber, viber_request)
                elif len(syntax) < 2:
                    return viber.send_messages(
                        viber_request.sender.id,
                        TextMessage(text="Need to have valid value"))
                elif syntax[0].lower() == '/email':
                    background_tasks.add_task(registration_update, viber_request,
                                            viber)
                elif syntax[0].lower() == '/GET':
                    background_tasks.add_task(pre_download,message,viber_request, background_tasks, viber)
            else:
                viber.send_messages(
                        viber_request.sender.id,
                        TextMessage(text="Please wait a seconds, we are processing"))
                background_tasks.add_task(search, message, viber_request, background_tasks, viber)

    elif isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id,
                            [TextMessage(text=message_guide)])
    # elif isinstance(viber_request, ViberUnsubscribedRequest):
    #     background_tasks.add_task(unsup, viber_request)
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id,
                            [TextMessage(text="thanks for subscribing!")])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(
            viber_request))

    response.status_code = 200
    return response