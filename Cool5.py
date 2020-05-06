import random
import time
import numpy

WIDTH = 90
HEIGHT = 50


directions = [(x, y) for x in range(-1, 2) for y in range(-1, 2)] # [(1, 0), (1, 1), (0, 1), (-1, 1) ...]
directions.remove((0,0))

class Boid():
    def __init__(self, x, y, see_range=5):
        self.x = x
        self.y = y
        self.direction = random.choice(directions)

        self.see_range = see_range
    
    def update(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.see()
    
    def see(self):
        # Has to be made so, that it sees in every direction. Major changes are necessary

        possible_directions = []
        for d in directions:
            x = self.x
            y = self.y
            possible = True
            for _ in range(self.see_range):
                x += d[0]
                y += d[1]

                if x <= 0 or x >= WIDTH or y <= 0 or y >= HEIGHT:
                    possible = False
                
                for boid in boids:
                    if boid.x == x and boid.y == y:
                        possible = False
                
                if not possible:
                    break
            if possible:
                possible_directions.append(d)


        if not self.direction in possible_directions:
            self.direction = random.choice(possible_directions)
                    
                
                
                


boids = []
for _ in range(5):
    boids.append(Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)))


pre_format = numpy.empty((HEIGHT, WIDTH), str)
formatted = """"""

while True:
    print("\n"*2*HEIGHT)

    pre_format = numpy.empty((HEIGHT, WIDTH), str)
    formatted = """"""
    for boid in boids:
        pre_format[boid.y][boid.x] = "#"
        pre_format[boid.y-boid.direction[1]][boid.x-boid.direction[0]] = "#"
        boid.update()

    for y in pre_format:
        if any(y):
            for x in y:
                if x == "":
                    formatted += " "
                else:
                    formatted += "#"
            formatted += "\n"
        else:
            formatted += "\n"

    print(formatted)

    time.sleep(0.1)