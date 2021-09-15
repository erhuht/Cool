import random
import time
import os

WIDTH = 90 #Width of console
HEIGHT = 50 #Height of console
RESOLUTION = 200

WIDTH, HEIGHT = os.get_terminal_size()
WIDTH //= 2

points = []
bezier = []

def output(l, p=[]):
    output_string = ""
    for y in range(HEIGHT, -1, -1):
        for x in range(WIDTH*2):
            if [x, y] in p:
                output_string += "@"
            elif [x, y] in l:
                output_string += "#"
            else:
                output_string += " "
        output_string += "\n"
    print(output_string, end="")

def animate_output(l, p=[], sleep_time=0.1):
    # contains the picture as a 1d array, does not include line breaks
    output_string = (" "*2*WIDTH + "\n") * HEIGHT
    # adds the control points
    for point in p:
        # strings are immutable so the entire string has to be redefined
        output_string = output_string[:(2*WIDTH+1)*(HEIGHT - point[1]) + point[0]] + "@" + output_string[(2*WIDTH+1)*(HEIGHT - point[1]) + point[0] + 1:]
    for i, point in enumerate(l):
        # adds point on the curve if not on control point
        if point not in p:
            output_string = output_string[:(2*WIDTH+1)*(HEIGHT - point[1]) + point[0]] + "#" + output_string[(2*WIDTH+1)*(HEIGHT - point[1]) + point[0] + 1:]
        print(output_string, end="")
        time.sleep(sleep_time)

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

animate_output(bezier, points, .1)
