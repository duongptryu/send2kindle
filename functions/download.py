from model import User
from functions.small_check import check_register, increase_process, decrease_process, check_status, clear_search, delete
from viberbot.api.messages.text_message import TextMessage
import requests
import os
import time
import re
from fastapi import HTTPException
from functions.send_mail import send_mail
from functions.convert import convert_to_mobi

def download(book_title, book_ext, viber_request, url_download, background_tasks, viber, user):
    url = url_download
    res = requests.get(url, allow_redirects=True)
    # import pdb; pdb.set_trace()
    if res.status_code == 200:
        viber.send_messages(viber_request.sender.id, TextMessage(text="Downloading"))
        name_book =book_title + "_" + str(time.time()) +"." + book_ext

        # try:
        # except Exception as e:
        #     import pdb; pdb.set_trace()
        with open(name_book, 'wb') as f:
            f.write(res.content)
        viber.send_messages(viber_request.sender.id, TextMessage(text="Downloaded, we are processing the book to send it to you."))
        return name_book
    else:
        viber.send_messages(viber_request.sender.id, TextMessage(text="Couldn't download. Please try again" ))
        decrease_process(user)
        raise HTTPException(status=403)



def pre_download(message,viber_request, background_tasks, viber):
    viber.send_messages(viber_request.sender.id, TextMessage(text="We are processing, please wait a seconds"))
    #check user register
    user = check_register(viber_request)
    if user == None:
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Account didn't registraded with kindle mail. Please registration with syntax: \n /register yourkindlemail@kindle.com"))
    if check_status(user) == False:
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Please comeback later, We are working on your previous request"))
    increase_process(user)
    if user.search_temporary == [1]:
        decrease_process(user)
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Please search before download, user '/help' to help" ))

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
        ext_list = ['epub', 'fb2', 'cbz', 'cbr', 'mobi', 'pdf', 'docx', 'html', 'txt', 'odt', 'chm', 'djvu', 'rtf']
        if book['Extension'] not in ext_list:
            decrease_process(user)
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Sorry, now we haven't yet support this extension" ))
        if int(book['Size'].split(" ")[0]) > 25 and book['Size'].split(" ")[1] == 'Mb':
            decrease_process(user)
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Can't convert. Size must be smaller than 25 Mb" ))
        elif int(book['Size'].split(" ")[0]) > 200000 and book['Size'].split(" ")[1] == 'Kb':
            decrease_process(user)
            return viber.send_messages(viber_request.sender.id, TextMessage(text="Can't convert. Size must be smaller than 25 Mb" ))
        #

        background_tasks.add_task(clear_search, user)
        res = requests.get(book["Mirror_1"], allow_redirects=True)
        res  = res.content.decode('utf-8')

        urls = re.findall(r'href=[\'"]?([^\'" >]+)', res)
        url_download = urls[1]
        try:
            name_book = download(book['Title'],book['Extension'], viber_request, url_download, background_tasks, viber, user)
            convert_list = ['epub', 'fb2', 'cbz', 'cbr', 'docx', 'html', 'txt', 'odt', 'chm', 'djvu', 'rtf']
            if book['Extension'] in convert_list:
                try:
                    new_name = convert_to_mobi(name_book, viber, viber_request)
                    name_book = new_name
                except:
                    decrease_process(user)
                    return  viber.send_messages(viber_request.sender.id, TextMessage(text="Fail to convert, please try again"))
        except:
            decrease_process(user)
            return  viber.send_messages(viber_request.sender.id, TextMessage(text="Couldn't download, please try again"))
        try:
            send_mail(name_book, user, viber, viber_request)
            viber.send_messages(viber_request.sender.id, TextMessage(text="Book was sent through kindle mail, please check after 30 - 60 minutes. If can't not received book, please check again your kindle mail and steps that we recommended"))
            delete(name_book)
        except:
            decrease_process(user)
            return  viber.send_messages(viber_request.sender.id, TextMessage(text="Couldn't send mail, please try again"))
    except:
        decrease_process(user)
        return viber.send_messages(viber_request.sender.id, TextMessage(text="Some errors, please check input. Using '/help' to help" ))
    decrease_process(user)
#