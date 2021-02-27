import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import os
from viberbot.api.messages.text_message import TextMessage

fromaddr = "send2kindle.ncsc@gmail.com"

   
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
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, "!@#123456789aA")
    text = msg.as_string()
    viber.send_messages(viber_request.sender.id, TextMessage(text="Sending the mail"))
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
