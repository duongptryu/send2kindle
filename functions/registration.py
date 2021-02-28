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
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Couldn't register now, please try later"))
    try:
        user = User.objects.get({'_id': viber_request.sender.id})
        if check_status(user) == False:
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Please comeback later, We are working on your previous request"))
        try:
            user.kindle_mail = kindle_email
            user.save()
            viber.send_messages(viber_request.sender.id, TextMessage(text="Update kindle mail successfull with kindle mail " + kindle_email))
        except:
            viber.send_messages(viber_request.sender.id, TextMessage(text="Some errors, can't not update mail. We will fix it as soon as possible"))
    except User.DoesNotExist:
        try:
            user = User(viber_id=viber_request.sender.id,kindle_mail=kindle_email, search_temporary=[1], history=[1], status=0)
            user.save()
            viber.send_messages(viber_request.sender.id, TextMessage(text="Register success with kindle mail " + kindle_email))
        except:
            viber.send_messages(viber_request.sender.id, TextMessage(text="Some errors, can't not registration. We will fix it as soon as possible"))
