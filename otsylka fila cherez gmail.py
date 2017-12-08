# Import smtplib for the actual sending function
import smtplib


from smtplib import SMTP

from email.message import Message
from email.header import Header, make_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

from base64 import b64encode
import time
# For guessing MIME type
import os
import sys
import mimetypes

# Import the email modules we'll need
import email
# import email.mime.application
#
# # Create a text/plain message
# msg = email.mime.Multipart.MIMEMultipart()
# msg['Subject'] = 'Greetings'
# msg['From'] = 'toropov0014@gmail.com'
# msg['To'] = 'toropov0014@mail.ru'
#
# # The main body is just another attachment
 body = email.mime.Text.MIMEText("""Hello, how are you? I am fine.
# #This is a rather nice letter, don't you think?""")
# #msg.attach(body)
#
# # PDF attachment
filename='WindowPlace.txt'
fp=open(filename,'rb')
att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)

# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate.
s = smtplib.SMTP('smtp.mail.com:587')
#s.set_debuglevel(1)
s.starttls()
#time.sleep(0.5)
s.login('888toropov888@gmail.com','kirgudu0014')
s.sendmail("888toropov888@gmail.com","888toropov888@gmail.com","go to bed!")
#s.sendmail('toropov0014@gmail.com',['toropov0014@gmail.com'], msg.as_string())
s.quit()