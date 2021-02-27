import os
import subprocess
from functions.small_check import delete
from viberbot.api.messages.text_message import TextMessage

def convert_to_mobi(file_name, viber, viber_request):
    file_name = file_name.split(".")
    if len(file_name) == 2:
        name_book = file_name[0]
    else:
        name_book = file_name[0] + "." + file_name[1]
    try:
        viber.send_messages(viber_request.sender.id, TextMessage(text="Converting" ))
        # os.system('ebook-convert ' + '"' + os.getcwd() + '\\download\\' + name_book +'.epub" ' + '"' + os.getcwd() + '\\download\\' + name_book + '.mobi"')
        subprocess.call(["ebook-convert",name_book + "." + file_name[-1],name_book +'.mobi']) 
        viber.send_messages(viber_request.sender.id, TextMessage(text="Converted" ))
        delete(name_book + file_name[-1])
        return name_book + ".mobi"
    except Exception as e:
        raise
