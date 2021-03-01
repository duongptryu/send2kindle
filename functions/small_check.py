from model import User
import time
import os
from viberbot.api.messages.text_message import TextMessage

def clear_search(user):
    user.search_temporary = [1]
    user.save()


def add_search(user, result):
    user.search_temporary = result
    user.save()

def delete(name_book):
    os.remove(name_book)

def increase_process(user):
    user.status = 1
    user.time = time.time()
    user.save()

def decrease_process(user):
    user.status = 0
    user.time = 0
    user.save()

def check_status(user):
    if user.status == 0:
        return True
    else:
        return False

def check_time(viber_request):
    try:
        user = User.objects.get({"_id": viber_request.sender.id})
        if time.time() - user.time > 600:
            decrease_process(user)
    except:
        pass

def check_register(viber_request):
    try:
        user = User.objects.get({'_id': viber_request.sender.id})
        return user
    except User.DoesNotExist:
        return None