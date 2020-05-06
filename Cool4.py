import time
import math
import random

# open in cmd full screen

ACTUAL_HEIGHT = 50
HEIGHT = ACTUAL_HEIGHT-10
WIDTH = 98
SNOW = 15

sun = """
        \\  |  /
         ##### 
        #######
    --  #######  --
        #######  
         ##### 
        /  |  \\
"""

class Biome:
    stoppable = True
    @staticmethod
    def generate(previous, number):
        return previous

    @staticmethod
    def output(printing, number):
        printing[number] = printing[number][:-1] + "#"
        
        return printing


class Mountains(Biome):
    @staticmethod
    def generate(previous, number):
        if number < HEIGHT-1 and number > 0:
            weights = [5, 1, 5]
            if previous == 0:
                weights[1] += 15 # Flat mountain tops look boring
            else:
                weights[1+previous] += 95
        # Makes sure it doesn't go over the limits
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
        # Adds a # to the line corresponding to the number
        printing[number] = printing[number][:-1] + "#"
        if number < SNOW:
            for i in range(number, SNOW + random.choice([1, 0, -1])):
                printing[i] = printing[i][:-1] + "#"
        
        return printing

class Grasslands(Biome):
    tree_bool = False
    tree_index = 0
    tree = ["   ##   ",
            " ###### ",
            "########",
            "   ||   ",
            "   ||   "]
    tree.reverse()

    @classmethod
    def generate(cls, previous, number):
        if not cls.tree_bool:
            if number < HEIGHT-1 and number > 0:
                previous = random.choices([-1, 0, 1], [1, 25, 1])[0]
            elif number >= HEIGHT-1:
                previous = random.choices([-1, 0], [1, 25])[0]
            else:
                previous = random.choices([0, 1], [25, 1])[0]
        else:
            previous = 0
        return previous

    @classmethod
    def output(cls, printing, number):
        # Adds a # to the line corresponding to the number
        printing[number] = printing[number][:-1] + "#"
        if number > 0:
            printing[number-1] = printing[number-1][:-1] + random.choices([" ", ",", ".", "v", "u"], [20, 2, 1, 5, 2])[0]
        
        # Tree
        if  random.random() > 0.98 and number > len(cls.tree) and cls.stoppable:
            cls.stoppable = False
            cls.tree_bool = True
        
        if cls.tree_bool:
            for i in range(len(cls.tree)):
                printing[number-(1+i)] = printing[number-(1+i)][:-1] + cls.tree[i][cls.tree_index]
            cls.tree_index += 1
        
        if cls.tree_index >= len(cls.tree[0]):
            cls.stoppable = True
            cls.tree_bool = False
            cls.tree_index = 0

        return printing


class Farm(Biome):
    field_bool = False
    field = ["|", "i", "|"]
    field_len = 0
    field_index = 0


    cow_bool = False
    cow_index = 0
    cow =  ["      _  ",
            "  __/|_|\\",
            "/|___|   ",
            " |   |   "]
    cow.reverse()
    cow_mirror_bool = False
    cow_mirror = ["  _      ",
                  "/|_|\\__  ",
                  "   |___|\\",
                  "   |   | "]
    cow_mirror.reverse()

    house_bool = False
    house_index = 0
    house = ["                          +&-           ",
             "                         _.-^-._    .--.",
             "                      .-'   _   '-. |__|",
             "                     /     |_|     \\|  |",
             "                    /               \\  |",
             "                   /|     _____     |\\ |",
             "                    |    |==|==|    |  |",
             "|---|---|---|---|---|    |--|--|    |  |",
             "|---|---|---|---|---|    |==|==|    |  |",]
    house.reverse()

    @classmethod
    def generate(cls, previous, number):
        if cls.stoppable:
            if number < HEIGHT-1 and number > 0:
                previous = random.choices([-1, 0, 1], [1, 45, 1])[0]
            elif number >= HEIGHT-1:
                previous = random.choices([-1, 0], [1, 45])[0]
            else:
                previous = random.choices([0, 1], [45, 1])[0]
        else:
            previous = 0

        return previous

    @classmethod
    def output(cls, printing, number):
        printing[number] = printing[number][:-1] + "#"


        if random.random() > 0.98 and number > 3 and cls.stoppable:
            cls.stoppable = False
            decide = random.randint(0, 2)
            if decide == 0:
                cls.field_bool = True
                cls.field_len = random.randint(10, 30)
            if decide == 1:
                cls.cow_bool = True
                cls.cow_mirror_bool = random.choice([True, False])
            if decide == 2:
                cls.house_bool = True
        
        #Fields
        if cls.field_bool and cls.field_index == 0:
            printing[number-1] = printing[number-1][:-1] + cls.field[0]
            cls.field_index += 1
        elif cls.field_bool and cls.field_index == cls.field_len:
            printing[number-1] = printing[number-1][:-1] + cls.field[-1]
            cls.field_bool = False
            cls.stoppable = True
            cls.field_index = 0
        elif cls.field_bool:
            printing[number-1] = printing[number-1][:-1] + random.choice(cls.field[1:-1])            
            cls.field_index += 1
        
        #Cow
        if cls.cow_bool:
            for i in range(len(cls.cow)):
                if cls.cow_mirror_bool:
                    printing[number-(1+i)] = printing[number-(1+i)][:-1] + cls.cow_mirror[i][cls.cow_index]
                else:
                    printing[number-(1+i)] = printing[number-(1+i)][:-1] + cls.cow[i][cls.cow_index]
            cls.cow_index += 1
        
        if cls.cow_index >= len(cls.cow[0]):
            cls.stoppable = True
            cls.cow_bool = False
            cls.cow_index = 0

        #House
        if cls.house_bool:
            for i in range(len(cls.house)):
                printing[number-(1+i)] = printing[number-(1+i)][:-1] + cls.house[i][cls.house_index]
            cls.house_index += 1
        
        if cls.house_index >= len(cls.house[0]):
            cls.stoppable = True
            cls.house_bool = False
            cls.house_index = 0

        if cls.stoppable:
            printing[number-1] = printing[number-1][:-1] + random.choices([" ", ",", ".", "_"], [20, 1, 1, 1])[0]

        return printing


# possible future biome: https://ascii.co.uk/art/farms
all_biomes = [Mountains, Grasslands, Farm]
lowland_biomes = [Mountains, Grasslands, Farm]
anywhere_biomes = [Mountains]
biome = random.choice(all_biomes)

number = HEIGHT//2
previous = 0
weights = [5, 1, 5]
printing = [" "*WIDTH*2]*HEIGHT


while True:
    try:
        print("\n"*(HEIGHT*2)) # Flushes the text
        if random.random() > 0.995:
            if biome.stoppable:
                if number > HEIGHT//2:
                    biome = random.choice(lowland_biomes)
                else:
                    biome = random.choice(anywhere_biomes)
        

        # Random generates where the new symbol should be. The weights make it go longer in the same direction 
        previous = biome.generate(previous, number)
        number += previous
        
        # Moves every line to the left
        for s in range(len(printing)):
            printing[s] = printing[s][1:] + " "
        
        # Adds a # to the line corresponding to the number
        printing = biome.output(printing, number)
        
        formatted = """"""
        for i in printing:
            if i != " "*WIDTH*2:
                formatted += i + "\n"
            else:
                formatted += "\n"
        print(sun)
        print(formatted)
        time.sleep(0.01)
    except KeyboardInterrupt:
        exit()