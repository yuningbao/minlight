import pygame,sys
from pygame.locals import *
from entites_systeme_minlight import Cable,DimensionsPave,Pave
from entites_mathemathiques import Vecteur3D,TupleAnglesRotation

from OpenGL.GL import *
from OpenGL.GLU import *


longueur = 0
hauteur = 0
largeur = 0

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    edges = (
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,7),
        (6,3),
        (6,4),
        (6,7),
        (5,1),
        (5,4),
        (5,7)
        )
    verticies = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
        )
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def getchar():
   #Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch



def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    cable = Cable(Vecteur3D(0,0,0),"a",Vecteur3D(1,1,1),5)

    pave = Pave(Vecteur3D(longueur/2,largeur/2,hauteur/2) , TupleAnglesRotation(0,0,0), DimensionsPave(1,1,1))

    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == KEYDOWN:
                print("pegou algo")
                if event.key == pygame.K_LEFT:
                    print("pegou algo")
                if event.key == pygame.K_RIGHT:
                    print("pegou algo aqui")
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cable.draw()
<<<<<<< HEAD
        pave.draw(False)
=======
>>>>>>> 2f87f2b1ed13591a1cc867bb2e69f2ad714a36e1
        pygame.display.flip()
        pygame.time.wait(10)


main()
