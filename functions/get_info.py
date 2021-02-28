from model import User
from viberbot.api.messages.text_message import TextMessage

def get_info(viber, viber_request):
    try:
        user = User.objects.get({'_id': viber_request.sender.id})
        return viber.send_messages(
                            viber_request.sender.id,
                            TextMessage(text="Your kindle mail is: " + user.kindle_mail))
    except User.DoesNotExist:
        return viber.send_messages(
                            viber_request.sender.id,
                            TextMessage(text="Unregistered account. To register, follow syntax: /email your_kindle_mail@kindle.com. Using '/ help' for help. "))