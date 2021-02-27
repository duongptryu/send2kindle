from model import User
from functions.small_check import check_register, increase_process, decrease_process, check_status
from viberbot.api.messages.text_message import TextMessage
import re

def registration_update(viber_request, viber):
    kindle_email = re.search("[a-zA-Z0-9-_.]+@kindle.com", viber_request.message.text)
    if kindle_email == None:
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Email must be kindle mail, please check again"))
    kindle_email = kindle_email.group()
    try:
        import pdb; pdb.set_trace()
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
            viber.send_messages(viber_request.sender.id, TextMessage(text="Registration success with kindle mail " + kindle_email))
        except:
            viber.send_messages(viber_request.sender.id, TextMessage(text="Some errors, can't not registration. We will fix it as soon as possible"))
