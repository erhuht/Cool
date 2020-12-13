import random
import time
import numpy
from math import sqrt
from ctypes import windll

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1) #Time resolution to 1 ms

# This thing turned out very spaghetti-y :(

WIDTH = 95
HEIGHT = 45
TAILS = False
BOIDS = 20

directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

class Boid():
    def __init__(self, x, y, see_range=25):
        self.x = x
        self.y = y
        self.direction = random.choice(directions)

        self.see_range = see_range
    
    def update(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.see()
    
    def see(self):
        possible_directions = {}
        chosen_directions = []

        index1 = (directions.index(self.direction)-1) % len(directions)
        index2 = (directions.index(self.direction)+2) % len(directions)

        if index1 > index2:
            n_directions = directions[index1:-1] + [directions[-1]] + directions[0:index2] # There's probably a better way of doing this
        else:
            n_directions = directions[index1:index2]
        
        # Avoids collisions with walls. This gets priority, because otherwise it would crash
        for d in n_directions:
            x = self.x
            y = self.y
            for i in range(self.see_range):
                x += d[0]
                y += d[1]

                if x > 0 and x < WIDTH and y > 0 and y < HEIGHT:
                    possible_directions[d] = i
                else:
                    break
        try:
            max_value = max(possible_directions.values())
        except ValueError: # It has to do a 180 degree turn, shouldn't happen
            for d in directions:
                x = self.x
                y = self.y
                for i in range(self.see_range):
                    x += d[0]
                    y += d[1]

                    if x >= 0 and x <= WIDTH and y >= 0 and y <= HEIGHT:
                        possible_directions[d] = i
                    else:
                        break
            max_value = max(possible_directions.values())

        for key in possible_directions.keys():
            if possible_directions[key] == max_value:
                chosen_directions.append(key)
        
        if not self.direction in chosen_directions:
            # Looks for the best chosen direction
            for i in range(len(directions)*2):
                i = i * ((i % 2)*2-1) // 2 # Goes through like so: 0; 0; -1; 1; -2; 2; -3 and so on
                if directions[(directions.index(self.direction)+i) % len(directions)] in chosen_directions:
                    self.direction = directions[(directions.index(self.direction)+i) % len(directions)]
                    break
        else:
            # Here we can do the separation, cohesion and allignment
            # http://www.vergenet.net/~conrad/boids/pseudocode.html

            nearby_boids = []

            vector = list(self.direction)

            for boid in boids:
                if boid != self:
                    if sqrt((boid.x-self.x)**2+(boid.y-self.y)**2) < self.see_range:
                        nearby_boids.append(boid)

            # Cohesion
            center = [0,0]
            if len(nearby_boids) > 0:
                for nearby_boid in nearby_boids:
                    center[0] += nearby_boid.x
                    center[1] += nearby_boid.y
                
                center[0] /= len(nearby_boids)
                center[1] /= len(nearby_boids)
                center = tuple(center)

                vector[0] += center[0] / 100
                vector[1] += center[1] / 100
            

            # Separation
            s = [0,0]

            for nearby_boid in nearby_boids:
                if sqrt((nearby_boid.x-self.x)**2+(nearby_boid.y-self.y)**2) < (self.see_range/5):
                    s[0] += self.x - nearby_boid.x
                    s[1] += self.y - nearby_boid.y

            vector[0] += s[0]
            vector[1] += s[1]
            
            # Alignment
            if len(nearby_boids) > 0:
                nearby_direction = [0, 0]
                for nearby_boid in nearby_boids:
                    nearby_direction[0] += nearby_boid.direction[0]
                    nearby_direction[1] += nearby_boid.direction[1]
                nearby_direction[0] /= len(nearby_boids)
                nearby_direction[1] /= len(nearby_boids)

                vector[0] += nearby_direction[0] / 8
                vector[1] += nearby_direction[0] / 8


            # Combine the rules
            vector = tuple(vector)
            
            e_directions = n_directions.copy()
            for i in range(len(e_directions)):
                e_directions[i] = abs(vector[0]-e_directions[i][0] + vector[1]-e_directions[i][1])
            

            chosen_directions = []
            min_value= min(e_directions)
            for i in range(len(e_directions)):
                if e_directions[i] == min_value:
                    chosen_directions.append(n_directions[i])

            if not self.direction in chosen_directions:
                # Looks for the best chosen direction
                for i in range(len(directions)*2):
                    i = i * ((i % 2)*2-1) // 2 # Goes through like so: 0; 0; -1; 1; -2; 2; -3 and so on
                    if directions[(directions.index(self.direction)+i) % len(directions)] in chosen_directions:
                        self.direction = directions[(directions.index(self.direction)+i) % len(directions)]
                        break


                
                
                


boids = []
for _ in range(BOIDS):
    boids.append(Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)))


pre_format = numpy.empty((HEIGHT+3, WIDTH+3), str)
formatted = """"""

while True:
    print("\n"*2*HEIGHT)

    pre_format = numpy.empty((HEIGHT+3, WIDTH+3), str)
    formatted = """"""
    for boid in boids:
        pre_format[boid.y][boid.x] = "#"
        if TAILS:
            pre_format[boid.y-boid.direction[1]][boid.x-boid.direction[0]] = "+"
        boid.update()

    for y in pre_format:
        if any(y):
            for x in y:
                if x == "":
                    formatted += "  "
                elif x == "+":
                    formatted += "+ "
                else:
                    formatted += "# "
            formatted += "\n"
        else:
            formatted += "\n"

    print(formatted)

    time.sleep(0.01)