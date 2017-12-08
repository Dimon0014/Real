import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
fromaddr = "toropov0014@mail.ru"
toaddr = "toropov0014@mail.ru"
mypass = "kirgudu0014"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Привет от питона"
#
body = "Это пробное сообщение"
#msg.attach(MIMEText(body, 'plain'))

filename='WindowPlace.txt'
fp=open(filename,'rb')
att = MIMEApplication(fp.read(),_subtype="txt")
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)

server = smtplib.SMTP('smtp.mail.ru')
server.set_debuglevel(1)
server.starttls()
server.login(fromaddr, mypass)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()