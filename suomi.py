from sense_hat import SenseHat
sense = SenseHat()

#https://www.rapidtables.com/web/color/RGB_Color.html

b = [0, 0, 255]  # sininen
e = [0, 0, 0]  # tyhja
v = [255, 255, 255] #valkoinen

suami = [
    v, v, b, b, v, v, v, v,
    v, v, b, b, v, v, v, v,
    v, v, b, b, v, v, v, v,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    v, v, b, b, v, v, v, v,
    v, v, b, b, v, v, v, v,
    v, v, b, b, v, v, v, v
]

sense.show_message("Suomi :D")
sense.set_pixels(suami)
vastaus = input("jatketaanko y/n ")
if vastaus == "n":
    sense.clear()
if vastaus == "y":
    vastaus = input("jatketaanko y/n ")
    if vastaus == "n":
        sense.clear()
   
