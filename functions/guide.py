from viberbot.api.messages.text_message import TextMessage
import config

def guide(viber, viber_request):
    message = config.MESSAGE_GUIDE
    return viber.send_messages(viber_request.sender.id, TextMessage(text=message))