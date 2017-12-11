from os import system
from time import sleep



for i in range(0, 10):
    system("fswebcam -r 1280x720 --no-banner image" + str(i) + ".jpg")
    sleep(1)