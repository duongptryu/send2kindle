import smtplib 
import config
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import os
from viberbot.api.messages.text_message import TextMessage

fromaddr = config.EMAIL
password = config.PASSWORD

   
msg = MIMEMultipart() 

def send_mail(name_book, user, viber, viber_request):
    toaddr = user.kindle_mail
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = "convert"
    filename = name_book
    attachment = open(filename, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    name = name_book.split("_")[0] + "." + name_book.split(".")[-1]
    p.add_header('Content-Disposition', "attachment; filename= %s" % name) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, password)
    text = msg.as_string()
    viber.send_messages(viber_request.sender.id, TextMessage(text="Sending the mail"))
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
