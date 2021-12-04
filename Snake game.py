# Name: Mitchell Brown
# 11/30/2021
# biscuitbob13337@gmail.com
# CSC 2280
''' I will practice academic and personal integrity and excellence of character and expect the
    same from others.'''

# Code Imports
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from pygame import mixer 

# Food Object Class
class cube(object):
    a = 500
    columns = 20
    
    # initialization, starting positition and color
    # dx is direction x axis and dy is direction y axis
    def __init__(self, start, dx = 1, dy = 0, color = (0, 128, 0)):
        self.position = start
        self.color = color
        self.dx = 1
        self.dy = 0


    # Snake moving direction  
    def move(self, dx, dy):
        
        # Saving x and y to snake
        self.dx = dx
        self.dy = dy
        # Where the snake is on the board
        self.position = (self.position[0] + self.dx, self.position[1] + self.dy)
        
        
    # Drawing Cubes and eyes on head of snake
    def draw(self, surface, eyes = False):
        
        # Distance between 
        dis = self.a // self.columns
        
        # Row and Column
        r = self.position[0]
        c = self.position[1]
        
        # Drawing actual snake shapes
        pygame.draw.rect(surface, self.color, (r * dis + 1, c * dis + 1, dis - 2, dis - 2))
        
        # Eyes on the head
        if eyes:
            # center of head
            center = dis // 2
            # size of eyes
            radius = 3
            
            # Math for position of eyes 
            mid_of_circ1 = (r * dis + center - radius, c * dis + 8)
            mid_of_circ2 = (r * dis + dis - radius * 2, c * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), mid_of_circ1, radius)
            pygame.draw.circle(surface, (0, 0, 0), mid_of_circ2, radius)
       
  
# Snake Class
class snake(object):
    body = []
    rotate = {}
    
    # Snake Initialization, color and starting point
    def __init__(self, color, position):
        self.color = color
        
        # Starting position (of head
        self.head = cube(position)
        self.body.append(self.head)
        self.dx = 0
        self.dy = 1
        
    # Snake movement
    def move(self):
        
        # Loop for keeping the snake moving
        for event in pygame.event.get():
            
            # If user clicks red x
            if event.type == pygame.QUIT:
                pygame.quit()
                message_box("You quit.", "Thanks for playing! Goodbye!")
                exit()
                
            # Keys that move the snake
            keys = pygame.key.get_pressed()
            
            # Loops moving snake with keys
            for key in keys:
                
                # Quit (Q)
                if keys[ord('q')]:
                    message_box("You quit.", "Thanks for playing! Goodbye!")
                    exit()
                    
                # Left (A)
                if keys[ord('a')]:
                    self.dx = -1
                    self.dy = 0
                    # Moves tail with head
                    self.rotate[self.head.position[:]] = [self.dx, self.dy]
                    
                # Right (D)
                elif keys[ord('d')]:
                    self.dx = 1
                    self.dy = 0
                    # Moves tail with head
                    self.rotate[self.head.position[:]] = [self.dx, self.dy]
                    
                # Up (W)
                elif keys[ord('w')]:
                    self.dx = 0
                    self.dy = -1
                    # Moves tail with head
                    self.rotate[self.head.position[:]] = [self.dx, self.dy]
                    
                # Down (S)
                elif keys[ord('s')]:
                    self.dx = 0
                    self.dy = 1
                    # Moves tail with head
                    self.rotate[self.head.position[:]] = [self.dx, self.dy]
                    
                    
        # Tail following snake 
        for i, c in enumerate(self.body):
            
            # Tail variable 
            p = c.position[:]
            
            # Snake turns tail with head
            if p in self.rotate:
                rotate = self.rotate[p]
                c.move(rotate[0], rotate[1])
                
                # moving last cube of tail
                if i == len(self.body) -1:
                    self.rotate.pop(p)
                    
            # Checking if snake is at edge of screen and moving it to opposite side if it is
            else:
                if c.dx == -1 and c.position[0] <= 0: c.position = (c.columns-1, c.position[1])
                elif c.dx == 1 and c.position[0] >= c.columns-1: c.position = (0, c.position[1])
                elif c.dy == 1 and c.position[1] >= c.columns-1: c.position = (c.position[0], 0)
                elif c.dy == -1 and c.position[1] <= 0: c.position = (c.position[0], c.columns - 1)
                else: c.move(c.dx, c.dy)
                
       
    # Resetting snake function
    def reset(self, position):
        self.head = cube(position)
        self.body = []
        self.body.append(self.head)
        self.rotate = {}
        self.dx = 0
        self.dy = 1


    # Adding length as snake eats food function
    def add_tail(self):
        
        # Tail position
        tail = self.body[-1]
        dnx, dny = tail.dx, tail.dy

        # Checking what direction snake is moving so tail can follow
        if dnx == 1 and dny == 0:
            self.body.append(cube((tail.position[0] -1, tail.position[1])))
        elif dnx == -1 and dny == 0:
            self.body.append(cube((tail.position[0] + 1, tail.position[1])))
        elif dnx == 0 and dny == 1:
            self.body.append(cube((tail.position[0], tail.position[1] -1)))
        elif dnx == 0 and dny == -1:
            self.body.append(cube((tail.position[0], tail.position[1] +1)))

        # Set direction of tail so cube can be added 
        self.body[-1].dx = dnx
        self.body[-1].dy = dny
        
        
    # Drawing snake
    def draw(self, surface):
        
        # Checking snake for head
        for i, c in enumerate(self.body):
            
            # Drawing eyes on head
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
        
       
# Redrawing window function
def redraw_window(surface):

    # Global variables
    global columns, width, s, food
    
    # Drawing board
    pygame.display.update()
    
    # Board color
    surface.fill((0, 0, 0))
    
    # Snake Drawing
    s.draw(surface)
    
    # Food drawing
    food.draw(surface)

 
# Food position and randomization function
def random_food(columns, item):
    
    # Define food variable as an item
    pos_food = item.body
    
    # Setting food cube
    while True:
        x = random.randrange(columns)
        y = random.randrange(columns)

        # If food isnt on snake 
        if len(list(filter(lambda z:z.position == (x,y), pos_food))) > 0:
            continue
        else:
            break       
    return (x,y)

 
# Message box
def message_box(subject, content):
    
    # Setting variable from input
    root = tk.Tk()
    
    # Setting window on top of all windows
    root.attributes("-topmost", True)
    root.withdraw()
    
    # Setting message box parameters
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


# Background music
pygame.mixer.init()
mixer.music.load('C:/Users/biscu/Downloads/background.wav')
mixer.music.play(-1)


# Main Function
def main():
    # Global Variables for size of board and how many columns
    global width, columns, s, food
    width = 500
    columns = 20

    # Needed for Main to start because it defines the games borders
    win = pygame.display.set_mode((width, width))
    
    # Starting position and color of snake
    s = snake((0,128,0), (10,10))
    
    # Setting food position and color
    food = cube(random_food(columns, s), color = (0, 0, 255))
    
    # Starting message
    message_box("Consume atleast 15 blocks to win!", "Press ENTER to play...(Turn your volume on!)")
    pass

    # Main loop
    main_snake = True
    # Game speed 
    clock = pygame.time.Clock()
    # Loop to keep snake moving 
    while main_snake:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        
        # If food spawns where snake spawns
        if s.body[0].position == food.position:
            s.add_tail()
            
            # Position of food after snake eats
            food = cube(random_food(columns, s), color = (0, 0, 255))
            
        # Loop for message box
        for x in range(len(s.body)):
            if s.body[x].position in list(map(lambda z:z.position, s.body[x + 1:])):
                
                # Snake length score
                message_box("Score", "Your snake was {} blocks long!".format(len(s.body)))
                
                # Winning message
                if len(s.body) >= 15:
                    message_box("You Won!", "Press ENTER to play again.")
                    s.reset((10,10))
                    break
                    
                # Losing message
                else: 
                    message_box("You Lost!", "Press ENTER to play again.")
                    s.reset((10,10))
                    break
 
        # Calling function   
        redraw_window(win)
    pass 
main()