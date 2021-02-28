import requests
import os
from functions.small_check import check_register, increase_process, decrease_process, check_status, clear_search, delete
from viberbot.api.messages.text_message import TextMessage
from functions.convert import convert_to_mobi
from functions.send_mail import send_mail
from fastapi import HTTPException
import time
import config

def process(viber, viber_request):
    viber.send_messages(viber_request.sender.id, TextMessage(text="We are processing, please wait a seconds"))
    #check user register
    user = check_register(viber_request)
    if user == None:
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Account didn't registraded with kindle mail. Please registration with syntax: \n /register yourkindlemail@kindle.com"))
    if check_status(user) == False:
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Please comeback later, We are working on your previous request"))
    increase_process(user)

    ext = viber_request.message.file_name.split(".")[-1]

    if ext in config.EXT_LIST:
        if int(viber_request.message.size) < int(50000000):
            name_book = download_file(viber_request.message.media, viber, viber_request, user)
            if name_book.split(".")[-1] in config.CONVERT_LIST:
                try:
                    new_name = convert_to_mobi(name_book, viber, viber_request)
                    name_book = new_name
                except:
                    decrease_process(user)
                    return  viber.send_messages(viber_request.sender.id, TextMessage(text="Fail to convert"))
                    delete(name_book)
            try:
                send_mail(name_book, user, viber, viber_request)
                viber.send_messages(viber_request.sender.id, TextMessage(text="Book was sent through kindle mail, please check after 30 - 60 minutes. If can't not received book, please check again your kindle mail and steps that we recommended"))
                delete(name_book)
            except:
                decrease_process(user)
                return  viber.send_messages(viber_request.sender.id, TextMessage(text="Couldn't send mail, please try again"))
            decrease_process(user)
        else:
            decrease_process(user)
            return viber.send_messages(viber_request.sender.id, TextMessage(text="File too large" ))
    else:
        decrease_process(user)
        return viber.send_messages(viber_request.sender.id, TextMessage(text="We are not support this extension" ))


def download_file(url, viber, viber_request, user):
    res = requests.get(url, allow_redirects=True)
    name = viber_request.message.file_name.split(".")
    if res.status_code == 200:
        viber.send_messages(viber_request.sender.id, TextMessage(text="Downloading" ))
        name_book = name[0] + "_" + str(time.time()) +"." + name[-1]

        with open(name_book, 'wb') as f:
            f.write(res.content)
        viber.send_messages(viber_request.sender.id, TextMessage(text="Downloaded, we are processing the book to send it to you."))
        return name_book
    else:
        viber.send_messages(viber_request.sender.id, TextMessage(text="Couldn't download. Please try again" ))
        decrease_process(user)
        raise HTTPException(status=403)