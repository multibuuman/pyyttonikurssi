import picamera
import time
import datetime

#maaritellaan kamera olio
camera = picamera.PiCamera()
# picamera kirjasto haettiin sudo-aptget install python-picamera
aika = datetime.datetime.now().minute
kuvanottohetki = str(aika) # ettei tarvitse joka kerta nimetä itse jollei halua
nimi = input("anna nimi: ")
camera.capture(nimi + '.jpg')

#camera.start_recording("esimvideo.h264")
#nauhoituksen aika (sekunttia)
#time.sleep(10)
#viiden sekunnin jalkeen lopetetaan nauhoitus
#camera.stop_recording
