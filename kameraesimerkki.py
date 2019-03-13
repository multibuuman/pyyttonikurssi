import picamera
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#maaritellaan kamera olio
camera = picamera.PiCamera()
# picamera kirjasto haettiin sudo-aptget install python-picamera
aika = datetime.datetime.now().minute
#kuvanottohetki = str(aika) # ettei tarvitse joka kerta nimetä itse jollei halua
#nimi = input("anna nimi: ")
camera.capture("kuva.jpg")

#camera.start_recording("esimvideo.h264")
#nauhoituksen aika (sekunttia)
#time.sleep(10)
#viiden sekunnin jalkeen lopetetaan nauhoitus
#camera.stop_recording


# tama kaikki on sahkopostin lahetysta varten
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = 'suolamyrttinen@gmail.com'
email_send = 'suolamyrttinen@gmail.com'
email_password = 'myrttinen'
subject = 'kuvan lahetys'

msg = MIMEMultipart()
msg ['From'] = email_user
msg ['To'] = email_send
msg ['Subject'] = subject

body = 'Tama viesti on lahetetty pythonilla ja sisaltaa kuvan :D'
msg.attach(MIMEText (body, 'plain'))
filename = 'kuva.jpg'
attachment = open(filename, 'rb')

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename = " + filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email_user,email_password)

server.sendmail(email_user,email_send,text)
server.quit()

