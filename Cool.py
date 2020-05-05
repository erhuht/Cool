import time
import math

#open in cmd full screen
divisor = 10000 #larger number ---> slower rate of change

i = 0
while i < divisor*3.14159:
    try:
        print(" "*round(math.sin(i*i/divisor)*90+90)+"#")
        i += 1
        time.sleep(0.001)
    except KeyboardInterrupt:
        print(i)
        exit()