from model import User
from functions.small_check import check_register, increase_process, decrease_process, check_status
from viberbot.api.messages.text_message import TextMessage
import re

def registration_update(viber_request, viber):
    try:
        kindle_email = re.findall("[a-zA-Z0-9-_.]+@kindle.com", viber_request.message.text)
        if kindle_email == None or len(kindle_email) == 0:
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Email must be kindle mail, please check again"))
        kindle_email = kindle_email[0]
    except:
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Cannot register now, please try again later"))
    try:
        user = User.objects.get({'_id': viber_request.sender.id})
        if check_status(user) == False:
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Please come back later, We are working on your previous request"))
        try:
            user.kindle_mail = kindle_email
            user.save()
            viber.send_messages(viber_request.sender.id, TextMessage(text="The kindle mail update is successful with the kindle mail " + kindle_email))
        except:
            viber.send_messages(viber_request.sender.id, TextMessage(text="Some errors, the mail cannot be updated. We will fix it as soon as possible"))
    except User.DoesNotExist:
        try:
            user = User(viber_id=viber_request.sender.id,kindle_mail=kindle_email, search_temporary=[1], time=0, status=0)
            user.save()
            viber.send_messages(viber_request.sender.id, TextMessage(text="Successful registration with kindle mail " + kindle_email))
        except:
            viber.send_messages(viber_request.sender.id, TextMessage(text="Some bugs, could not fail to register. We will fix it as soon as possible"))
