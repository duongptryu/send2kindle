from viberbot.api.messages.text_message import TextMessage
import config
from viberbot import Api

def guide(viber, viber_request):
    message = config.MESSAGE_GUIDE(viber_request.sender.name)
    return viber.send_messages(viber_request.sender.id, TextMessage(text=message))