import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import os
import requests
from base64 import encodebytes

fromaddr = "send2kindle.ncsc@gmail.com"
   
msg = MIMEMultipart() 

def send_mail(res):
    toaddr = "test@gmail.com"
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = "convert"
    filename = "test.pdf"
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload(encodebytes(res.content).decode())
    encoders.encode_base64(p) 
    p.add_header('Content-Transfer-Encoding', 'base64')
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, "A123456789a@")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


res = requests.get("https://cloudflare-ipfs.com/ipfs/bafykbzacectm6uf6xccr3f5hj4hq73axtzo7nflv5ecis6z4r7kstqkb23equ?filename=%28For%20dummies%29%20Kevin%20Beaver%2C%20Peter%20T.%20Davis%2C%20Devin%20K.%20Akin%20-%20Hacking%20Wireless%20Networks%20For%20Dummies-Wiley%20Pub.%20Inc%20%282005%29.pdf")
send_mail(res)