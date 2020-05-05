import time
import math
import random


#open in cmd full screen
HEIGHT = 50
WIDTH = 90
SNOW = 15

number = HEIGHT//2
previous = 0
weights = [5, 1, 5]
printing = [" "*WIDTH*2]*HEIGHT



class Mountains:
    @staticmethod
    def generate(previous, number):
        if number < HEIGHT-1 and number > 0:
            weights = [5, 1, 5]
            if previous == 0:
                weights[1] += 15 #Flat mountain tops look boring
            else:
                weights[1+previous] += 95
        #Makes sure it doesn't go over the limits
        elif number >= HEIGHT-1:
            weights = [1, 0, 0]
            number = HEIGHT-1
        else:
            weights = [0, 0, 1]
            number = 0

        previous = random.choices([-1, 0, 1], weights=weights)[0]

        return previous
    
    @staticmethod
    def output(printing, number):
        #Adds a # to the line corresponding to the number
        printing[number] = printing[number][:-1] + "#"
        if number < SNOW:
            for i in range(number, SNOW + random.choice([1, 0, -1])):
                printing[i] = printing[i][:-1] + "#"
        
        return printing

class Grasslands:
    @staticmethod
    def generate(previous, number):
        if number < HEIGHT-1 and number > 0:
            previous = random.choices([-1, 0, 1], [1, 2, 1])[0]
        elif number >= HEIGHT-1:
            previous = random.choices([-1, 0], [1, 2])[0]
        else:
            previous = random.choices([0, 1], [2, 1])[0]
        return previous

    @staticmethod
    def output(printing, number):
        #Adds a # to the line corresponding to the number
        printing[number] = printing[number][:-1] + "#"

        return printing

biome = Mountains
lowland_biomes = [Mountains, Grasslands]
anywhere_biomes = [Mountains]

while True:
    try:
        print("\n"*(HEIGHT*2)) # Flushes the text
        if random.random() > 0.99:
            if number > HEIGHT//2:
                biome = random.choice(lowland_biomes)
            else:
                biome = random.choice(anywhere_biomes)
        

        #Random generates where the new symbol should be. The weights make it go longer in the same direction 
        previous = biome.generate(previous, number)
        number += previous
        
        #Moves every line to the left
        for s in range(len(printing)):
            printing[s] = printing[s][1:]
            printing[s] += " "
        
        #Adds a # to the line corresponding to the number
        printing = biome.output(printing, number)
        
        formatted = """"""
        for i in printing:
            if i != " "*WIDTH*2:
                formatted += i + "\n"
            else:
                formatted += "\n"
        print(formatted)
        time.sleep(0.01)
    except KeyboardInterrupt:
        exit()