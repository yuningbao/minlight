# -*- coding: utf-8 -*-
import pygame,sys
from pygame.locals import *
from modeles.entites_systeme_minlight import Cable,DimensionsPave,Pave,Chambre,Source
from modeles.entites_mathemathiques import Vecteur3D,TupleAnglesRotation
from modeles.entite_cable_robot import *
#from simulation.setups.parametres_objets import source

from OpenGL.GL import *
from OpenGL.GLU import *


from modeles.enums import UniteAngleEnum

from modeles.entites_mathemathiques import \
    Vecteur3D,                                \
    TupleAnglesRotation,                      \
    SpaceRechercheAnglesLimites,              \
    IntervalleLineaire,                       \
    SystemeRepereSpherique

from modeles.entites_systeme_minlight import \
    DimensionsPave,                             \
    Pave,                                       \
    ConfigurationAncrage,                       \
    ConfigurationCable


'''
Parametres
'''

''' ************************ Chambre ************************ '''

# dimensions
dimensions_chambre = \
    DimensionsPave(
        # on considere le sisteme a partir de l'avaporateur
        longueur=8500,  # mm
        largeur=5000,   # mm
        hauteur=4000    # mm
    )

# centre
centre_chambre = \
    Vecteur3D(
        x=dimensions_chambre['longueur'] / 2,  # mm
        y=dimensions_chambre['largeur' ] / 2,  # mm
        z=dimensions_chambre['hauteur' ] / 2   # mm
    )

# pavé
chambre = \
    Chambre(
        centre=centre_chambre,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_chambre
    )


''' ************************ Maisonette ************************ '''

distance_evaporateur_maisonette = 3500  # mm

# dimensions
dimensions_maisonette = \
    DimensionsPave(
        longueur=5000,  # mm
        largeur=2500,   # mm
        hauteur=2900    # mm
    )

# centre
centre_maisonette = \
    Vecteur3D(
        x=distance_evaporateur_maisonette + dimensions_maisonette['longueur'] / 2,
        y=dimensions_chambre['largeur'] / 2,
        z=dimensions_maisonette['hauteur'] / 2
    )

# pave
maisonette = \
    Pave(
        centre=centre_maisonette,
        ypr_angles=TupleAnglesRotation.ZERO(),
        dimensions=dimensions_maisonette
    )


''' ************************ Source ************************ '''

# dimensions
dimensions_source = \
    DimensionsPave(
        longueur=1000,  # mm
        largeur=1600,   # mm
        hauteur=1600    # mm
    )

centre_source = \
    Vecteur3D(
        x=dimensions_chambre['longueur'] / 2,  # mm
        y=dimensions_chambre['largeur' ] / 2,  # mm
        z=dimensions_chambre['hauteur' ] / 2   # mm
    )

source = \
    Source(
        centre = centre_source,
        ypr_angles = TupleAnglesRotation.ZERO(),
        dimensions = dimensions_source
    )


''' ************************ Systeme Spherique Baie Vitrée ************************ '''

# centre - supposé dans le centre de la face d'intérêt de la maisonette
centre_systeme_spherique = \
    Vecteur3D(
        x=distance_evaporateur_maisonette,
        y=dimensions_chambre['largeur'] / 2,
        z=dimensions_maisonette['hauteur'] / 2
    )

# rotation
rotation_systeme_spherique = \
    TupleAnglesRotation(
        yaw=180,  # degrés
        pitch=0,  # degrés
        row=0,    # degrés
        unite=UniteAngleEnum.DEGRE,
    )

# systeme sphérique
systeme_spherique_baie_vitree = SystemeRepereSpherique(
    centre=centre_systeme_spherique,
    ypr_angles=rotation_systeme_spherique
)







def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glLineWidth(2.0)

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
    glScalef(0.001,0.001,0.001)
    origin = centre_chambre

    my_robot = Cable_robot(chambre,maisonette,source,5)
    my_robot.create_cables(Config_Cables.clock_wise,Config_Cables.clock_wise,Config_Cables.haut_haut)

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

        if(translate_source_X_neg == True):
            my_robot.translate_source(-5,0,0)
        if(translate_source_X_pos == True):
            my_robot.translate_source(5,0,0)

        if(rotate_source_yaw_pos == True):
            my_robot.rotate_source(1,0,0)
        if(rotate_source_yaw_neg == True):
            my_robot.rotate_source(-1,0,0)
        if(rotate_source_pitch_pos == True):
            my_robot.rotate_source(0,1,0)
        if(rotate_source_pitch_neg == True):
            my_robot.rotate_source(0,-1,0)
        if(rotate_source_row_pos == True):
            my_robot.rotate_source(0,0,1)
        if(rotate_source_row_neg == True):
            my_robot.rotate_source(0,0,-1)


        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        my_robot.draw(origin)
        #chambre2.draw(origin)
        pygame.display.flip()
        pygame.time.wait(10)


main()
