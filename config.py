import os

COMMAND_LIST = ["/help", "/email", "/GET"]
MONGO_URL = os.environ('mongo_url')
BOT_NAME = "Send2Kindle"
EMAIL = os.environ('email')
PASSWORD = os.environ('password')
AVATAR = "https://botostore.com/netcat_files/6/7/preview_148877_1587232924.jpg"
TOKEN = os.environ('token')

EXT_LIST = ['epub', 'fb2', 'cbz', 'cbr', 'mobi', 'pdf', 'docx', 'html', 'txt', 'odt', 'chm', 'djvu', 'rtf']

CONVERT_LIST = ['epub', 'fb2', 'cbz', 'cbr', 'docx', 'html', 'txt', 'odt', 'chm', 'djvu', 'rtf']



def MESSAGE_GUIDE(name):
    return  f'''
        Welcome {name}! ✨
    Thanks for use own service.

    This bot can send files to your Kindle.
    The maximum file size is 25 MB.

    1️⃣ Setup your Kindle account with this command:
    /email YourEmail@kindle.com

    2️⃣ Go to your https://www.amazon.com/mn/dcw/myx.html/ref=kinw_myk_surl_1#/home/settings/payment&context=Amazon Amazon account→ Preferences tab → Personal Document Settings and add send2kindle.ncsc@gmail.com to approved e-mail list (no mistake, you need to approve the whole domain)

    👆 This is necessary step to allow your Kindle account to receive files!

    3️⃣ All set up! 🎉

    This bot support extensions .pdb, .mobi, .asw3 .epub  .chm .djvu .txt .html .docx .cbr .fb2 .rtf .odt

    Syntax
    1. Help: /help
    2. Register/ update mail: /email your_kindl_email@kindle.com
    4. Type and send message to search book
    5. Download book: Click GET button

    Have fun <3  🦠🦠🦠
        '''