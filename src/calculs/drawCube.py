import pygame,sys
from pygame.locals import *
from modeles.entites_systeme_minlight import Cable,DimensionsPave,Pave
from modeles.entites_mathemathiques import Vecteur3D,TupleAnglesRotation

from OpenGL.GL import *
from OpenGL.GLU import *




def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    longueur = 10
    largeur = 10
    hauteur = 10

    glTranslatef(0,0,-5)
    origin = Vecteur3D(longueur/2,largeur/2,hauteur/2)

    cable = Cable(Vecteur3D(0,0,0),"a",Vecteur3D(1,1,1),5)
    source = Pave(origin , TupleAnglesRotation(0,0,0), DimensionsPave(1,1,1))
    chambre = Pave(origin , TupleAnglesRotation(0,0,0), DimensionsPave(longueur,largeur,hauteur))


    rotateX_CW = False
    rotateX_CCW = False
    rotateY_CW = False
    rotateY_CCW = False
    zoomIn = False
    zoomOut = False
    rotate_source_pitch = False


    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == KEYDOWN:
                if event.key == pygame.K_p:
                    rotateX_CW = True
                elif event.key == pygame.K_l:
                    rotateX_CCW = True
                elif event.key == pygame.K_o:
                    rotateY_CW = True
                elif event.key == pygame.K_k:
                    rotateY_CCW = True
                elif event.key == pygame.K_w:
                    zoomIn = True
                elif event.key == pygame.K_s:
                    zoomOut = True
                elif event.key == pygame.K_m:
                    rotate_source_pitch= True

            elif event.type == pygame.KEYUP or event.type == KEYUP:
                if event.key == pygame.K_p:
                    rotateX_CW = False
                elif event.key == pygame.K_l:
                    rotateX_CCW = False
                elif event.key == pygame.K_o:
                    rotateY_CW = False
                elif event.key == pygame.K_k:
                    rotateY_CCW = False
                elif event.key == pygame.K_w:
                    zoomIn = False
                elif event.key == pygame.K_s:
                    zoomOut = False
                elif event.key == pygame.K_m:
                    rotate_source_pitch = False

        if(rotateX_CW == True):
            glRotatef(3, 1, 0, 0)
        if(rotateX_CCW == True):
            glRotatef(-3, 1, 0, 0)
        if(rotateY_CW == True):
            glRotatef(3, 0, 1, 0)
        if(rotateY_CCW == True):
            glRotatef(-3, 0, 1, 0)
        if(rotateY_CCW == True):
            glRotatef(-3, 0, 1, 0)
        if(zoomIn == True):
            glScalef(1.1,1.1,1.1)
        if(zoomOut == True):
            glScalef(0.9,0.9,0.9)
        if(rotate_source_pitch == True):
            source.rotate(2,3,1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cable.draw(origin)
        source.draw(origin,True)
        chambre.draw(origin,False)
        pygame.display.flip()
        pygame.time.wait(10)


main()
