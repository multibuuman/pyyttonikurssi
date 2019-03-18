import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
# import both libraries pygame and openGL
verticies = ( # basicially corners or nodes of cube
    (1, -1, -1), # 1
    (1, 1, -1), # 2
    (-1, 1, -1), # 3
    (-1, -1, -1), # 4
    (1, -1, 1), # 5
    (1, 1, 1), # 6
    (-1, -1, 1), # 7
    (-1, 1, 1) # 8
    )
# thinking each 1 or -1 as x, y, z coordinate might help to understand this concept
# each node has 3 connections
edges = (
    (0,1), # 1 from node 0 to node 1 etc...
    (0,3), # 2
    (0,4), # 3
    (2,1), # 4
    (2,3), # 5
    (2,7), # 6
    (6,3), # 7
    (6,4), # 8
    (6,7), # 9
    (5,1), # 10
    (5,4), # 11
    (5,7)  # 12
    )


def Cube(): # lets define the cube
    # when using openGL you need to start with glBegin and end with glEnd
    glBegin(GL_LINES)# tell GL engine to draw lines
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex]) # glVertex3fv specifies a vertex, and here we ask to draw edge for each node in the verticies
    glEnd()


def main():
    pygame.init() # initialize the graphics engine
    display = (800,600) # size of the display
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # tell the pygame library that we are using OpenGL
    # doublebuffer manages the refresh rate of the monitor

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0) # field of view (45 degrees)
    # aspect ratio ( we already defined them as constants 800, 600 so the aspect ratio is just 800/600
    # clipping plane (basicially zoom)

    glTranslatef(0.0,0.0, -5) # x, y z parameters for viewing the cube

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() # so if we press quit (red x on window) the program dies

        glRotatef(1, 0, 0, 1)
        # 1 = speed, 2 = front view flip 3 = sideways flip 4 = "over the head" flip
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #clear the already drawn cube, try commenting this
        Cube()
        pygame.display.flip() # show the flip
        pygame.time.wait(10) # milliseconds

# real 3D vs 3D picture or drawn --> rotating, viewpoint, perspective etc.
main()