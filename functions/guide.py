from viberbot.api.messages.text_message import TextMessage

def guide(viber, viber_request):
    message = '''
    Welcome 🦠🦠🦠! ✨
This bot can send files to your Kindle.
The maximum file size is 25 MB.

1️⃣ Setup your Kindle account with this command:
/email YourEmail@kindle.com

2️⃣ Go to your Amazon account → Preferences tab → Personal Document Settings and add send2kindle.ncsc@gmail.com to approved e-mail list (no mistake, you need to approve the whole domain)

👆 This is necessary step to allow your Kindle account to receive files!

3️⃣ All set up! 🎉

This bot support extension .pdb, .mobi, .asw3 and .epub. 

Syntax
1. Help: /help
2. Registration/ update mail: /email your_kindl_email@kindle.com
4. Type and send message to search book
5. Download book: Click GET button

    
    '''
    return viber.send_messages(viber_request.sender.id, TextMessage(text=message))