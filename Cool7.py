import random
import time

WIDTH = 90 #Width of console
HEIGHT = 50 #Height of console
RESOLUTION = 200


points = []
bezier = []

def output(l, p=[]):
    for y in range(HEIGHT, -1, -1):
        for x in range(WIDTH*2):
            if [x, y] in p:
                print("@", end="")
            elif [x, y] in l:
                print("#", end="")
            else:
                print(" ", end="")
        print("\n", end="")

def animate_output(l, p=[]):
    for i in range(len(l)):
        output(l[0:i], p)
        time.sleep(0.1)

def line(p1, p2, t):
    x1, y1 = p1
    x2, y2 = p2
    return [x1 + (x2 - x1)*t, y1 + (y2 - y1)*t]

def get_points():
    index = 0
    while True:
        x = input(f"Point {index} x: ")
        if x == "random":
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
        else:
            x = int(x)
            y = int(input(f"Point {index} y: "))
        points.append([x*2, y])
        output(points)
        index += 1

        if input("Execute? (y/n) ") == "y":
            break



get_points()

for t in range(RESOLUTION):
    t /= RESOLUTION

    work_points = points
    while len(work_points) > 1:
        new_points = []
        for i in range(len(work_points)-1):
            new_points.append(line(work_points[i], work_points[i+1], t))
        work_points = new_points
    
    bezier.append([round(work_points[0][0]), round(work_points[0][1])])

output(bezier, points)