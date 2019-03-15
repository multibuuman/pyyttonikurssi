from __future__ import print_function

import datetime
import os
import sys
import time
from urllib import urlencode
#import threading tulostamiseen, mutta ei toimikkaan...

import urllib2
from sense_hat import SenseHat

# Vakiot
# Kuinka usein mitataan lampotila
MEASUREMENT_INTERVAL = 1 # minuuttia

b = [0, 0, 255]  # sininen
r = [255, 0, 0]  # punainen
e = [0, 0, 0]  # tyhja
# kuviot nuolille
arrow_up = [
    e, e, e, r, r, e, e, e,
    e, e, r, r, r, r, e, e,
    e, r, e, r, r, e, r, e,
    r, e, e, r, r, e, e, r,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e
]
arrow_down = [
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    b, e, e, b, b, e, e, b,
    e, b, e, b, b, e, b, e,
    e, e, b, b, b, b, e, e,
    e, e, e, b, b, e, e, e
]
bars = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e
]


def get_cpu_temp():
    # otetaan huomioon prosessorin C
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))

# Kaytetaan liikkuva keskiarvoa tasoittamaan tuloksia
def get_smooth(x):
    # onko oliota t
    if not hasattr(get_smooth, "t"): # argumentteina olio ja teksti. Jos totta niin True, False jos ei
        # tehdaan se
        get_smooth.t = [x, x, x]
    # siirretaan arvot
    get_smooth.t[2] = get_smooth.t[1]
    get_smooth.t[1] = get_smooth.t[0]
    get_smooth.t[0] = x
    # kolmen viime lukeman keskiarvo
    xs = (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3
    return xs


def get_temp():

    # http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
    # Otetaan kosteus ja ilmanpaine lukema
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    # olio t on molempien sensorien arvojen keskiarvo
    
    t = (t1 + t2) / 2
    # prosessorin C
    t_cpu = get_cpu_temp()
    # lasketaan oikea lampo, eli otetaan huomioon prosessorin lampo
    t_corr = t - ((t_cpu - t) / 1.5)
    # keskiarvoistetaan kolme viimeisinta lukemaa
    t_corr = get_smooth(t_corr)
    # palautetaan korjattu lampotila
    return t_corr


def main():
    global last_temp

    # viimeisin mittaus
    last_minute = datetime.datetime.now().minute
    # kaynnistyksessa kaytetaan viimeisinta mittausta
    last_minute -= 1
    if last_minute == 0:
        last_minute = 59

    # ikuinen looppi lammon tarkastamiseen
    # current_second = datetime.datetime.now().second
    while 1:
        # C mittauksen tarkkuus perustuu siis nyt keskiarvojen keskiarvo algoritmiin joten C mitataan 5 sekunnin valein
        # naytetaan vain "korjattu" C
        # https://raspberrypi.stackexchange.com/questions/45788/why-does-the-sense-hat-astro-pi-show-the-wrong-temperature-and-humidity
        # tassa syy miksi lampotilan mittaus sensehatilla on ongelmallista ja miksi hankalaa
        # saatiedosto.py on pelkka lampotilan haku
        current_second = datetime.datetime.now().second
        #current_minute = datetime.datetime.now().second
        if (current_second == 0) or ((current_second % 5) == 0):
            calc_temp = get_temp()
            temp_c = round(calc_temp, 1)
            humidity = round(sense.get_humidity(), 0)
            pressure = round(sense.get_pressure())
            time.sleep(1)
            print(current_second, "Lampotila: %sC, Ilmanpaine: %s Mbar, Kosteus: %s%%" % (temp_c, pressure, humidity))

            # nykyinen kellonaika
            current_minute = datetime.datetime.now().minute
            # tarkastetaan onko se sama kuin viimeksi
            if current_minute != last_minute:
                last_minute = current_minute
                # onko minuutti 0, vai jaollinen maaratylla mittausvalilla
                # otetaan mittaus vain maaratyn mittausvalin mukaan
                if (current_minute == 0) or ((current_minute % MEASUREMENT_INTERVAL) == 0):
                    # lukeman ajankohta
                    now = datetime.datetime.now()
                    print("\n%d minuutin ajankohta (%d @ %s)" % (MEASUREMENT_INTERVAL, current_minute, str(now)))
                    # nousiko vai laskiko C
                    if last_temp != temp_c:
                        if last_temp > temp_c:
                            # jos aleni, sininen nuoli
                            sense.set_pixels(arrow_down)
                        else:
                            # jos kasvoi punanen nuoli
                            sense.set_pixels(arrow_up)
                    else:
                        # jos C pysyi samana naytetaan punainen ja sininen viiva
                        sense.set_pixels(bars)
                    # asetetaan viimeisin lampotila nykyiseksi lampotilaksi
                    last_temp = temp_c


# mittausvali ei saa olla yli 60
if (MEASUREMENT_INTERVAL is None) or (MEASUREMENT_INTERVAL > 60):
    print("Mittausvali ei saa olla yli 60min")
    sys.exit(1)


try:
    print("Kaynnistetaan SenseHAT saasema")
    sense = SenseHat()
    # sense.set_rotation(180)
    # aloitus teksti
    sense.show_message("Kaynnistetaan", text_colour=[255, 102, 255], back_colour=[0, 102, 0])
    # tyhjennetaan
    sense.clear()
    # tulostetaan C
    last_temp = get_temp()
    print("Nykyinen lampotila:", last_temp)
except:
    print("Virhe kirjastossa:", sys.exc_info()[0])
    sys.exit(1)

print("Valmis")

# lopetetaan ohjhelma
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting application\n")
        sys.exit(0)

# urlencode ilmeisesti rpi:n oma kirjasto joka valmiina kayttojarjestelmassa, siksi suoritus ei toimi shellin kautta vaan terminaalin...
