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
from functions.get_info import get_info
from functions.small_check import check_time

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from viberbot.api.viber_requests import ViberDeliveredRequest
from viberbot.api.viber_requests import ViberSeenRequest
import config

app = FastAPI()

viber = Api(
    BotConfiguration(
        name=config.BOT_NAME,
        avatar=config.AVATAR,
        auth_token=config.TOKEN))



logger = logging.getLogger()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('system.log', 'a', 'utf-8')
logger.addHandler(handler)


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
    check_time(viber_request)
    if isinstance(viber_request, ViberMessageRequest):
            # import pdb; pdb.set_trace()
            if hasattr(viber_request.message, 'media'):
                background_tasks.add_task(process,viber, viber_request)
            elif hasattr(viber_request.message, 'text'):
                message = viber_request.message.text
                syntax = message.split(" ")
                
                if syntax[0].lower() in config.COMMAND_LIST:
                    if syntax[0].lower() == "/help":
                        guide(viber, viber_request)
                    elif syntax[0].lower() == '/info':
                        background_tasks.add_task(get_info, viber, viber_request)
                    elif len(syntax) < 2:
                        viber.send_messages(
                            viber_request.sender.id,
                            TextMessage(text="Must have valid values"))
                    elif syntax[0].lower() == '/email':
                        background_tasks.add_task(registration_update, viber_request,
                                                viber)
                    elif syntax[0].lower() == '/get':
                        background_tasks.add_task(pre_download,message,viber_request, background_tasks, viber)
                else:
                    viber.send_messages(
                            viber_request.sender.id,
                            TextMessage(text="Please wait a moment, we are working on it"))
                    background_tasks.add_task(search, message, viber_request, background_tasks, viber)
            else:
                viber.send_messages(
                            viber_request.sender.id,
                            TextMessage(text="Invalid input, please try again, use '/help' to help"))

    elif isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id,
                            [TextMessage(text=config.MESSAGE_GUIDE("broooo"))])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id,
                            [TextMessage(text="Thanks for subscribing!")])
        viber.send_messages(viber_request.user.id,
                            [TextMessage(text=config.MESSAGE_GUIDE(viber_request.sender.name))])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(
            viber_request))
#
    response.status_code = 200
    return response