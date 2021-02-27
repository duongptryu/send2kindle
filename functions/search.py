from functions.small_check import check_register, increase_process, decrease_process, check_status, add_search
from libgen_api import LibgenSearch
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.rich_media_message import RichMediaMessage
import requests
import re

s = LibgenSearch()


def search(message, viber_request, background_tasks, viber):
    #check user register
    try:
        user = check_register(viber_request)
        if user == None:
            return viber.send_messages(
                viber_request.sender.id,
                TextMessage(
                    text=
                    "Account didn't registration with kindle mail. Please registration with syntax: \n /email yourkindlemail@kindle.com"
                ))
        if check_status(user) == False:
            return viber.send_messages(
                viber_request.sender.id,
                TextMessage(
                    text=
                    "Please comeback later, We are working on your previous request"
                ))
        viber.send_messages(
            viber_request.sender.id,
            TextMessage(
                text=
                f"Please wait a seconds, we are searching the book with title '{message}'"
            ))
        increase_process(user)
    except Exception as e:
        return viber.send_messages(viber_request.sender.id,
                                   TextMessage(text="Error with check user"))
    # background_tasks.add_task(clear_search, user)

    # filters = {
    #     # "Author": "Brian Hatch",
    #     # "Extension": Extension,
    #     # "Publisher": Publisher,
    #     # "Year": Year,
    #     # "Language": Language,
    #     # "Pages": 2
    # }
    title = message.strip()

    try:
        result = s.search_title(title)
    except:
        decrease_process(user)
        return viber.send_messages(
            viber_request.sender.id,
            TextMessage(text="Couldn't search now, please try later"))

    if len(result) == 0:
        #
        decrease_process(user)
        return viber.send_messages(
            viber_request.sender.id,
            TextMessage(text="No result for search " + title +
                        ". Please try again, use '/help' to help"))
    else:
        background_tasks.add_task(add_search, user, result[:3])

        SAMPLE_RICH_MEDIA = {
            "ButtonsGroupColumns": 6,
            "ButtonsGroupRows": 7,
            "BgColor": "#FFFFFF",
            "Buttons": []
        }
        for index, book in enumerate(result[:3]):
            title_book = book['Title']
            name_book = title_book
            author_book = book['Author']
            num = str(index + 1)
            ext = book['Extension']
            size = book['Size']
            if len(title_book) > 70:
                title_book = title_book[:70] + "..."
            if len(author_book) > 20:
                author_book = author_book[:17] + " ..."

            res = requests.get(book["Mirror_1"])
            img_tag = re.search(r'<img[^>]+src="([^">]+)"', res.text)
            img_src = re.findall(r'(.*?)"', img_tag.group())[1]
            
            SAMPLE_RICH_MEDIA["Buttons"].append({
                "Columns":
                6,
                "Rows":
                4,
                "ActionType":
                "reply",
                "ActionBody":
                f"/GET {num}",
                "Image":f"http://library.lol{img_src}"
            })
            SAMPLE_RICH_MEDIA["Buttons"].append({
                "Columns": 6,
                "Rows": 2,
                "ActionType": "reply",
                "ActionBody": f"/GET {num}",
                "Text":
                f'<font color=\"#323232\"><b>{title_book}</b></font><font color=\"#777777\"><br>Author: </font><font color=#6fc133>{author_book}</font><br>Ext: <font color=\"#de1200\">{ext}</font>        Size: {size}',
                "TextSize": "medium",
                "TextVAlign": "middle",
                "TextHAlign": "left",
                "BgColor": "#a0b1d9"
            })
            SAMPLE_RICH_MEDIA["Buttons"].append({
                "Columns": 6,
                "Rows": 1,
                "ActionType": "reply",
                "ActionBody": f"/GET {num}",
                "Text": "<font color=\"#f50000\"><b>GET</b></font>",
                "TextSize": "large",
                "TextVAlign": "middle",
                "TextHAlign": "middle",
                "BgColor": "#e9f500"
            })

        SAMPLE_ALT_TEXT = "upgrade now!"
        # import pdb; pdb.set_trace()
        test = RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA,
                                min_api_version=2,
                                alt_text=SAMPLE_ALT_TEXT)
        viber.send_messages(viber_request.sender.id, test)
        viber.send_messages(
            viber_request.sender.id,
            TextMessage(
                text=
                "Click to GET button to get book to the kindle mail"
            ))
    decrease_process(user)