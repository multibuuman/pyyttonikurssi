from sense_hat import SenseHat
import time

sense = SenseHat()

v = (0, 255, 0) #vihreä
r = (102, 51, 0) # ruskea
vv = (178, 255, 102) # vaalean vihreä
vs = (51, 153, 255) #vaalean sininen
e = (0, 0, 0) # tyhjä

puu = [
    vs, vs, vs, vs, vs, vs, vs, vs,
    vs, vs, vs, v, v, vs, vs, vs,
    vs, vs, v, r, r, v, vs, vs,
    vs, v, v, r, r, v, v, vs,
    vs, v, v, r, r, v, v, vs,
    vs, vs, v, r, r, v, vs, vs,
    vv, vv, vv, r, r, vv, vv, vv,
    vv, vv, vv, r, r, vv, vv, vv
    ]
kaatunut = [
    vs, vs, vs, vs, vs, vs, vs, vs,
    vs, vs, vs, vs, vs, vs, vs, vs,
    vs, vs, vs, vs, vs, vs, vs, vs,
    vs, vs, vs, vs, vs, v, v, vs,
    vs, vs, vs, vs, v, v, v, v,
    vs, vs, vs, vs, r, r, r, r,
    vv, vv, vv, r, r, vv, vv, vv,
    vv, vv, vv, r, r, vv, vv, vv
    ]

sense.set_pixels(puu)

while True:
    acc = sense.get_accelerometer_raw() # haetaan kiihtyvyys // acc shelliin nayttaa oletusarvot
    if acc['x'] > 2 or acc['y'] > 2 or acc['z'] > 2: # jos kiihtyvyytta on 
        sense.set_pixels(kaatunut) 
        time.sleep(10) #kuinka kauan katsellaan kaatunutta puuta
        sense.clear() #tyhjenna
