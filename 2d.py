import pygame
import random
import math

#The maximum and minimum x and y coordinates
xMin, yMin = -20,-20
xMax,yMax = 20,20

#The actual plane of points has the above range
#The pygame display has the above range multiplied by the coord scalar
#Decrease coord scalar and increase x/y min/max to increase point density
coord_scalar = 20

#Radius of each dot
dot_rad = 0.1*coord_scalar

#Tick lifespan of each dot. Pygame runs at 120 tps
tick = 0
dot_lifetime_range = (5,1000)
LIFE = True #Whether or not dots should have a lifespan
#Whether or not to kill dots that exit the view
CLIP = True

dots = [[i,j,random.randint(dot_lifetime_range[0],dot_lifetime_range[1])] for i in range(xMin,xMax+1) for j in range(yMin,yMax)]
count = len(dots)

#How much each dot is changed by its flow vector
#Higher value = faster, less accurate movements
movement_scalar = 0.01

#Pygame initialization
width = (xMax-xMin)*coord_scalar
height = (yMax-yMin)*coord_scalar
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Vector Field Motion Simulator")
clock = pygame.time.Clock()
pygame.font.init()
font_size = 20
font = pygame.font.SysFont('Consolas', font_size)

x_eq = "-(x*y)" #Change this equation to change the x component
def x_component(point): #X component of the vector field
    x=point[0]
    y=point[1]
    return eval(x_eq)

y_eq = "x" #Change this equation to change the y component
def y_component(point): #Y component of the vector field
    x = point[0]
    y = point[1]
    return eval(y_eq)

def conv_coords(point): #Converts a coordinate from the vector field's coordinate system to that of Pygame's
    x = point[0]
    y = point[1]
    x-=xMin
    y-=yMin
    x*=coord_scalar
    y*=coord_scalar
    return [x,y]

def display_dots():
    #The coordinate axes
    pygame.draw.line(screen,"white",(width/2,0),(width/2,height))
    pygame.draw.line(screen,"white",(0,height/2),(width,height/2))

    for dot in dots:
        pygame.draw.circle(screen,"white",conv_coords(dot),dot_rad)

def update_dots():

    for i,dot in enumerate(dots):
        xc,yc = x_component(dot),y_component(dot)
        dot[0]+=movement_scalar*xc
        dot[1] += movement_scalar * yc
        dot[2]-=1
        dots[i]=dot

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    display_dots()
    #gets rid of dots that are out of bounds and whose lifespan has ended
    if CLIP:
        dots = [dots[i] for i in range(len(dots)) if xMin<=dots[i][0]<=xMax and yMin<=dots[i][1]<=yMax]
    if LIFE:
        dots = [dots[i] for i in range(len(dots)) if dots[i][2]>0]


    replacing = count-len(dots)
    for i in range(replacing):
        dots.append([random.randint(xMin,xMax),random.randint(yMin,yMax),random.randint(dot_lifetime_range[0],dot_lifetime_range[1])])
    update_dots()

    #Adds info display
    text_surface = font.render(f"x={x_eq}", False, (255, 255, 0))
    screen.blit(text_surface, (0, font_size*0))
    text_surface = font.render(f"y={y_eq}", False, (255, 255, 0))
    screen.blit(text_surface, (0, font_size*1))
    text_surface = font.render(f"tick={tick}", False, (255, 0, 255))
    screen.blit(text_surface, (0, font_size*2))
    text_surface = font.render(f"Lifespan={LIFE}", False, (0, 255, 255))
    screen.blit(text_surface, (0, font_size*3))
    text_surface = font.render(f"Clipping={CLIP}", False, (0, 255, 255))
    screen.blit(text_surface, (0, font_size*4))
    tick+=1
    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock.tick(120)
pygame.quit()