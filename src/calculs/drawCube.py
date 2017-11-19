import pygame,sys
from pygame.locals import *
from modeles.entites_systeme_minlight import Cable,DimensionsPave,Pave,Chambre,Source
from modeles.entites_mathemathiques import Vecteur3D,TupleAnglesRotation
from modeles.entite_cable_robot import *

from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable (GL_LINE_SMOOTH)
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA_SATURATE, GL_ONE)
    glHint (GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth (1.5)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    i = 0
    longueur = 10
    largeur = 10
    hauteur = 10

    glTranslatef(0,0,-5)
    glRotatef(-90, 1, 0, 0)
    origin = Vecteur3D(longueur/2,largeur/2,hauteur/2)

    source = Source(origin , TupleAnglesRotation(0,0,0), DimensionsPave(1,1,1))
    chambre = Chambre(origin , TupleAnglesRotation(0,0,0), DimensionsPave(longueur,largeur,hauteur))
    maisonette = Pave(Vecteur3D(longueur/2,largeur/8,hauteur/8), TupleAnglesRotation(0,0,0), DimensionsPave(longueur/4,largeur/4,hauteur/4))
    my_robot = Cable_robot(chambre,maisonette,source,5)
    my_robot.create_cables(Config_Cables.clock_wise,Config_Cables.clock_wise,Config_Cables.simple)

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
                elif event.key == pygame.K_r:
                    glLoadIdentity()
                    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
                    glTranslatef(0,0,-5)
                    glRotatef(-90, 1, 0, 0)

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
            glRotatef(2, 1, 0, 0)
        if(rotateX_CCW == True):
            glRotatef(-2, 1, 0, 0)
        if(rotateY_CW == True):
            glRotatef(2, 0, 0, 1)
        if(rotateY_CCW == True):
            glRotatef(-2, 0, 0, 1)
        if(zoomIn == True):
            glScalef(1.1,1.1,1.1)
        if(zoomOut == True):
            glScalef(0.9,0.9,0.9)
        if(rotate_source_pitch == True):
            my_robot.rotate_source(0,2,0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        my_robot.draw(origin)
        #chambre2.draw(origin)
        pygame.display.flip()
        pygame.time.wait(10)


main()
