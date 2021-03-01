from model import User
from functions.small_check import check_register, increase_process, decrease_process, check_status, clear_search, delete
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.file_message import FileMessage
import requests
import os
import time
import re
import config
from fastapi import HTTPException
from functions.send_mail import send_mail
from functions.convert import convert_to_mobi

def download(book_title, book_ext, book_size, viber_request, url_download, background_tasks, viber, user):
    url = url_download
    res = requests.get(url, allow_redirects=True)
    # import pdb; pdb.set_trace()
    if res.status_code == 200:
        viber.send_messages(viber_request.sender.id, TextMessage(text="Downloading"))
        name_book =book_title + "_" + str(time.time()) +"." + book_ext

        # try:
        # except Exception as e:
        #     import pdb; pdb.set_trace()
        #open file
        with open(name_book, 'wb') as f:
            f.write(res.content)
        viber.send_messages(viber_request.sender.id, TextMessage(text="Downloaded, we're working on sending you the book."))
        size = book_size.split(" ")
        try:
            name = name_book.split("_")[0] + "." + name_book.split(".")[-1]
            #send  file via viber
            viber.send_messages(viber_request.sender.id, FileMessage(media="file:///" + os.getcwd() + name_book, size=os.path.getsize(name_book), file_name=name))
        except:
            viber.send_messages(viber_request.sender.id, TextMessage(text="Cannot send files via viber"))

        return name_book
    else:
        viber.send_messages(viber_request.sender.id, TextMessage(text="Cannot download. Please try again" ))
        decrease_process(user)
        raise HTTPException(status=403)



def pre_download(message,viber_request, background_tasks, viber):
    viber.send_messages(viber_request.sender.id, TextMessage(text="We're working on it, please wait a moment"))
    #check user register
    user = check_register(viber_request)
    if user == None:
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Accounts are not registered by kindle mail. Please register with the following syntax: \n /register yourkindlemail@kindle.com"))
    if check_status(user) == False:
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Please come back later, We are working on your previous request"))
    increase_process(user)
    if user.search_temporary == [1]:
        decrease_process(user)
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Please search before downloading, user '/ help' to help" ))

    books = user.search_temporary

    number = message.split(" ")[1].strip()
    check = number.isnumeric()
    if check == False:
        decrease_process(user)
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Invalid index"))
    if int(number) - 1 < 0 or int(number) > len(books):
        decrease_process(user)
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Invalid index"))

    try:
        book = books[int(number) - 1]
        if book['Extension'] not in config.EXT_LIST:
            decrease_process(user)
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Sorry, we do not currently support this extension" ))
        if int(book['Size'].split(" ")[0]) > 25 and book['Size'].split(" ")[1] == 'Mb':
            decrease_process(user)
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Cannot convert. The size should be less than 25 Mb" ))
        elif int(book['Size'].split(" ")[0]) > 200000 and book['Size'].split(" ")[1] == 'Kb':
            decrease_process(user)
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Cannot convert. The size should be less than 25 Mb" ))
        #

        background_tasks.add_task(clear_search, user)
        res = requests.get(book["Mirror_1"], allow_redirects=True)
        res  = res.content.decode('utf-8')

        urls = re.findall(r'href=[\'"]?([^\'" >]+)', res)
        url_download = urls[1]
        try:
            name_book = download(book['Title'],book['Extension'], book['Size'], viber_request, url_download, background_tasks, viber, user)

            if book['Extension'] in config.CONVERT_LIST:
                try:
                    new_name = convert_to_mobi(name_book, viber, viber_request)
                    name_book = new_name
                except:
                    decrease_process(user)
                    return  viber.send_messages(viber_request.sender.id, TextMessage(text="Failure to convert, please try again"))
        except:
            decrease_process(user)
            return  viber.send_messages(viber_request.sender.id, TextMessage(text="Cannot download, please try again"))
        try:
            send_mail(name_book, user, viber, viber_request)
            viber.send_messages(viber_request.sender.id, TextMessage(text="Books are sent by kindle mail, please check in after 30-60 minutes. If you do not receive the book, please check your kindle mail and the steps we recommend to receive the book"))
            delete(name_book)
        except:
            decrease_process(user)
            return  viber.send_messages(viber_request.sender.id, TextMessage(text="Cannot send mail, please try again"))
    except:
        decrease_process(user)
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Some errors, please check the input. Use '/ help' to help" ))
    decrease_process(user)
