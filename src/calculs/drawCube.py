# -*- coding: utf-8 -*-
import pygame,sys
from pygame.locals import *
from modeles.entites_systeme_minlight import Cable,DimensionsPave,Pave,Chambre,Source
from modeles.entites_mathemathiques import Vecteur3D,TupleAnglesRotation
from modeles.entite_cable_robot import *
from simulation.setups.parametres_objets import source,maisonette,chambre,centre_chambre

from OpenGL.GL import *
from OpenGL.GLU import *



def setShaders():
    v = glCreateShader(GL_VERTEX_SHADER)
    f = glCreateShader(GL_FRAGMENT_SHADER)

    with open ("shaders/simpleshader.frag", "r") as myfile:
        ftext=myfile.readlines()
    with open ("shaders/simpleshader.vert", "r") as myfile:
        vtext=myfile.readlines()

    glShaderSource(v, vtext)
    glShaderSource(f, ftext)

    glCompileShader(v)
    glCompileShader(f)

    p = glCreateProgram()
    glAttachShader(p,v)
    glAttachShader(p,f)

    glLinkProgram(p)
    glUseProgram(p)

    return p


def main():

    #sets display
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    #setting line smooth parameters
    glEnable (GL_LINE_SMOOTH)
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA_SATURATE, GL_ONE)
    glHint (GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth (1.5)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #setting viewers parameters
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0,0,-5)
    glRotatef(-90, 1, 0, 0)
    glScalef(0.001,0.001,0.001)
    origin = centre_chambre

    setShaders();
    
    #creates robot object
    my_robot = Cable_robot(chambre,maisonette,source,5)
    my_robot.create_cables(Config_Cables.simple,Config_Cables.simple,Config_Cables.haut_haut)

    #sets keyboard control variables
    rotateX_CW = False
    rotateX_CCW = False
    rotateY_CW = False
    rotateY_CCW = False
    zoomIn = False
    zoomOut = False
    translate_source_X_pos = False
    translate_source_X_neg = False
    rotate_source_yaw_neg = False
    rotate_source_yaw_pos = False
    rotate_source_pitch_neg = False
    rotate_source_pitch_pos = False
    rotate_source_row_neg = False
    rotate_source_row_pos = False

    #rendering loop
    while True:
        #event handling, keyboard handling
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
                elif event.key == pygame.K_z:
                    zoomIn = True
                elif event.key == pygame.K_x:
                    zoomOut = True
                elif event.key == pygame.K_m:
                    rotate_source_pitch= True
                elif event.key == pygame.K_w:
                    translate_source_X_pos= True
                elif event.key == pygame.K_s:
                    translate_source_X_neg= True
                elif event.key == pygame.K_i:
                    rotate_source_yaw_pos = True
                elif event.key == pygame.K_j:
                    rotate_source_yaw_neg = True
                elif event.key == pygame.K_u:
                    rotate_source_pitch_pos = True
                elif event.key == pygame.K_h:
                    rotate_source_pitch_neg = True
                elif event.key == pygame.K_y:
                    rotate_source_row_pos = True
                elif event.key == pygame.K_g:
                    rotate_source_row_neg = True
                elif event.key == pygame.K_r:
                    glLoadIdentity()
                    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
                    glTranslatef(0,0,-5)
                    glRotatef(-90, 1, 0, 0)
                    glScalef(0.001,0.001,0.001)

            elif event.type == pygame.KEYUP or event.type == KEYUP:
                if event.key == pygame.K_p:
                    rotateX_CW = False
                elif event.key == pygame.K_l:
                    rotateX_CCW = False
                elif event.key == pygame.K_o:
                    rotateY_CW = False
                elif event.key == pygame.K_k:
                    rotateY_CCW = False
                elif event.key == pygame.K_z:
                    zoomIn = False
                elif event.key == pygame.K_x:
                    zoomOut = False
                elif event.key == pygame.K_w:
                    translate_source_X_pos= False
                elif event.key == pygame.K_s:
                    translate_source_X_neg= False
                elif event.key == pygame.K_m:
                    rotate_source_pitch = False
                elif event.key == pygame.K_i:
                    rotate_source_yaw_pos = False
                elif event.key == pygame.K_j:
                    rotate_source_yaw_neg = False
                elif event.key == pygame.K_u:
                    rotate_source_pitch_pos = False
                elif event.key == pygame.K_h:
                    rotate_source_pitch_neg = False
                elif event.key == pygame.K_y:
                    rotate_source_row_pos = False
                elif event.key == pygame.K_g:
                    rotate_source_row_neg = False

        if(rotateX_CW == True):
            glRotatef(2, 1, 0, 0)
        elif(rotateX_CCW == True):
            glRotatef(-2, 1, 0, 0)
        elif(rotateY_CW == True):
            glRotatef(2, 0, 0, 1)
        elif(rotateY_CCW == True):
            glRotatef(-2, 0, 0, 1)
        elif(zoomIn == True):
            glScalef(1.1,1.1,1.1)
        elif(zoomOut == True):
            glScalef(0.9,0.9,0.9)

        elif(translate_source_X_neg == True):
            my_robot.translate_source(-5,0,0)
        elif(translate_source_X_pos == True):
            my_robot.translate_source(5,0,0)

        elif(rotate_source_yaw_pos == True):
            my_robot.rotate_source(1,0,0)
        elif(rotate_source_yaw_neg == True):
            my_robot.rotate_source(-1,0,0)
        elif(rotate_source_pitch_pos == True):
            my_robot.rotate_source(0,1,0)
        elif(rotate_source_pitch_neg == True):
            my_robot.rotate_source(0,-1,0)
        elif(rotate_source_row_pos == True):
            my_robot.rotate_source(0,0,1)
        elif(rotate_source_row_neg == True):
            my_robot.rotate_source(0,0,-1)

        #clears buffer, draws new one, switches, takes a pause
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        my_robot.draw(origin)
        pygame.display.flip()
        pygame.time.wait(10)


main()
