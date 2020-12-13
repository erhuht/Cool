#n-body simulation
import operator
import time
import math

HEIGHT = 44
WIDTH = 180
g = 39
s = 0.15

class Mass():
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0

        self.updateDrawPos()
    
    def updatePos(self):
        self.x += self.vx
        self.y += self.vy
    
        self.updateDrawPos()

    def updateDrawPos(self):
        self.drawx = round(self.x*2) + WIDTH//2
        self.drawy = round(self.y) + HEIGHT//2
    
    def updateVel(self):
        self.vx += self.ax
        self.vy += self.ay

    def updateAcc(self, bodies):
        ax = 0 #not self.ax
        ay = 0

        for body in bodies:
            if body != self:
                dx = body.x - self.x
                dy = body.y - self.y

                distSq = dx**2 + dy**2

                f = (g * body.mass) / (distSq * math.sqrt(distSq+s))

                ax += dx * f
                ay += dy * f

        self.ax += ax
        self.ay += ay

masses = [Mass(1, 0, 0, 0, 0), Mass(3.213e-7, 20, 0, 0, 2.5)]
masses = sorted(masses, key=operator.attrgetter("y", "x"))

while True:
    drawy = 0
    drawx = 0
    """
    for mass in masses:
        if mass.drawx > 0 and mass.drawx < WIDTH and mass.drawy > 0 and mass.drawy < HEIGHT:
            if mass.drawy-drawy == 0:
                print(" "*(mass.drawx-drawx)+"#", end="")
                drawx += mass.drawx-drawx+1
            else:
                print("\n"*(mass.drawy-drawy), end="")
                print(" "*mass.drawx+"#", end="")
                drawx = mass.drawx+1
            drawy += mass.drawy-drawy
    """
    for mass in masses:
        mass.updatePos()
        mass.updateAcc(masses)
        mass.updateVel()

    masses = sorted(masses, key=operator.attrgetter("y"))

    print("\n"*(HEIGHT-drawy))
    print(masses[1].x, masses[1].y)
    time.sleep(0.2)
    print("\n"*HEIGHT)