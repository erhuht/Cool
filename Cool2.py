import time
import math
import sys

s = ""
i = 0
WIDTH = 90 #Width of console
HEIGHT = 50 #Height of console
SPEED = 10 #Speed of printing
BASIC_F = 50 #Frequency of slowest part --> also affects the delta frequency
RATEOFCHANGE = 0.001 # Lower number --> higher

SPEED = 1/(SPEED*SPEED)

while i <= 3.14159265/RATEOFCHANGE*2:
    print("\n"*100)
    try:
        s = ""
        for f in range(BASIC_F, BASIC_F+HEIGHT):
            s += " "*int(math.sin(i*f*RATEOFCHANGE)*WIDTH+WIDTH)+"#\n"
        print(s)
        i += 1
        time.sleep(SPEED)
    except KeyboardInterrupt:
        print(i)
        exit()