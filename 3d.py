import pygame
import random
import math

#The maximum and minimum x and y coordinates
xMin, yMin, zMin = -7,-7,-7
xMax,yMax,zMax = 7,7,7
#Coordinate info for bounding cube and coordinate axes
bounding_cube = [[xMin,yMin,zMin],[xMin,yMin,zMax],[xMin,yMax,zMin],[xMin,yMax,zMax],[xMax,yMin,zMin],[xMax,yMin,zMax],[xMax,yMax,zMin],[xMax,yMax,zMax],]
edges = [[0,1],[0,2],[0,4],[1,3],[1,5],[2,3],[2,6],[3,7],[7,6],[7,5],[4,5],[4,6]]
axes = [  [[0,0,zMax],[0,0,zMin]]  ,[[0,yMax,0],[0,yMin,0]],  [[xMax,0,0],[xMin,0,0]]  ]


#The actual plane of points has the above range
#The pygame display has the above range multiplied by the coord scalar
#Decrease coord scalar and increase x/y min/max to increase point density
coord_scalar = 200/7

#Radius of each dot
dot_rad = 0.1*coord_scalar

#Tick lifespan of each dot. Pygame runs at 120 tps
tick = 0
dot_lifetime_range = (5,100)
LIFE = True #Whether or not dots should have a lifespan
#Whether or not to kill dots that exit the view
CLIP = True
#Angle of rotation along z axis
theta = 0
#Angle of rotation along x axis
phi = 0
FOV = 100

dots = [[i,j,k,random.randint(dot_lifetime_range[0],dot_lifetime_range[1])] for i in range(xMin,xMax+1) for j in range(yMin,yMax) for k in range(zMin,zMax)]
count = len(dots)

#How much each dot is changed by its flow vector
#Higher value = faster, less accurate movements
movement_scalar = 0.5

#Pygame initialization
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Vector Field Motion Simulator")
clock = pygame.time.Clock()
pygame.font.init()
font_size = 20
font = pygame.font.SysFont('Consolas', font_size)

x_eq = "-y/(x**2 + y**2 + z**2+0.01)" #Change this equation to change the x component
def x_component(point): #X component of the vector field
    x=point[0]
    y=point[1]
    z = point[2]


    return eval(x_eq)

y_eq = "x/(x**2 + y**2 + z**2+0.01)" #Change this equation to change the y component
def y_component(point): #Y component of the vector field
    x = point[0]
    y = point[1]
    z = point[2]


    return eval(y_eq)

z_eq = "z/(x**2 + y**2 + z**2+0.01)" #Change this equation to change the z component
def z_component(point): #Z component of the vector field
    x = point[0]
    y = point[1]
    z = point[2]


    return eval(z_eq)

def to2d(point): #Converts 3d coordinates to 2d screen coordinates
    x = point[0]
    y = point[1]
    z = point[2]
    #z axis rotations
    #|cosA -sinA 0
    #|sinA  cosA 0
    #|  0     0  1
    x1,y1,z1 = x,y,z
    x =x1 * math.cos(theta) - y1 * math.sin(theta)
    y = x1 * math.sin(theta) + y1 * math.cos(theta)

    #x axis rotations
    # |1  0     0
    # |0 cosA -sinA
    # |0 sinA  cosA
    x1, y1, z1 = x, y, z

    y = y1 * math.cos(phi) - z1 * math.sin(phi)
    z = y1*math.sin(phi) + z1*math.cos(phi)

    #Z is offset to start the simulation at an angle
    return x*FOV/(y+FOV),-(z-20)*FOV/(y+FOV)-20,y

def conv_coords(point): #Converts a coordinate from the vector field's coordinate system to that of Pygame's
    x = point[0]
    y = point[1]
    x *= coord_scalar
    y *= coord_scalar
    x+=width/2
    y+=height/2

    return [x,y]

def display_dots(): #Displays dots and other lines

    #The bounding cube
    for pair in edges:
        i,ii = pair
        p1 = bounding_cube[i]
        p2 = bounding_cube[ii]
        p1 = to2d(p1)
        p2 = to2d(p2)
        p1 = conv_coords(p1)
        p2 = conv_coords(p2)
        pygame.draw.line(screen,(255,255,255),p1,p2)
    #The coordinate axes
    for axis in axes:
        p1,p2 = axis
        p1 = to2d(p1)
        p2 = to2d(p2)
        p1 = conv_coords(p1)
        p2 = conv_coords(p2)
        pygame.draw.line(screen, (255, 255, 255), p1, p2)

    for dot in dots:
        twod = to2d(dot)
        #Dot color is darker based on its lifespan. For better clarity
        pygame.draw.circle(screen,[255*dot[-1]/100]*3,conv_coords(to2d(dot)[:2]),dot_rad)

def update_dots():

    for i,dot in enumerate(dots):
        xc,yc,zc = x_component(dot),y_component(dot),z_component(dot)
        dot[0]+=movement_scalar*xc
        dot[1] += movement_scalar * yc
        dot[2] += movement_scalar * zc
        dot[3]-=1
        dots[i]=dot

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    #handles rotations via key presses
    if keys[pygame.K_LEFT]:
        theta -= .1
    if keys[pygame.K_RIGHT]:
        theta += .1
    if keys[pygame.K_UP]:
        phi -= .1
    if keys[pygame.K_DOWN]:
        phi += .1


    display_dots()

    replacing = count - len(dots)
    for i in range(replacing):
        dots.append([random.randint(xMin, xMax), random.randint(yMin, yMax), random.randint(zMin, zMax), random.randint(dot_lifetime_range[0], dot_lifetime_range[1])])
    update_dots()


    #gets rid of dots that are out of bounds and whose lifespan has ended
    if CLIP:
        dots = [dots[i] for i in range(len(dots)) if xMin<=dots[i][0]<=xMax and yMin<=dots[i][1]<=yMax and zMin<=dots[i][2]<=zMax]
    if LIFE:
        dots = [dots[i] for i in range(len(dots)) if dots[i][3]>0]




    #Adds info display
    text_surface = font.render(f"x={x_eq}", False, (255, 255, 0))
    screen.blit(text_surface, (0, font_size*0))
    text_surface = font.render(f"y={y_eq}", False, (255, 255, 0))
    screen.blit(text_surface, (0, font_size*1))
    text_surface = font.render(f"z={z_eq}", False, (255, 255, 0))
    screen.blit(text_surface, (0, font_size * 2))
    text_surface = font.render(f"yaw={theta:.1f}", False, (255, 0, 255))
    screen.blit(text_surface, (0, font_size * 3))
    #Have to adjust the pitch for the fact it starts at an angle
    text_surface = font.render(f"pitch={-phi-0.2:.1f}", False, (255, 0, 255))
    screen.blit(text_surface, (0, font_size * 4))
    text_surface = font.render(f"tick={tick}", False, (255, 0, 255))
    screen.blit(text_surface, (0, font_size*5))
    text_surface = font.render(f"Lifespan={LIFE}", False, (0, 255, 255))
    screen.blit(text_surface, (0, font_size*6))
    text_surface = font.render(f"Clipping={CLIP}", False, (0, 255, 255))
    screen.blit(text_surface, (0, font_size*7))
    tick+=1
    pygame.display.flip()
    screen.fill((0, 0, 0))
    clock.tick(120)
pygame.quit()