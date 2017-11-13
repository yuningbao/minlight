from .outils2 import solutions_formule_quadratique
from .entites_mathemathiques import Vecteur3D
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame,sys
from pygame.locals import *

class DimensionsPave():

    def __init__(self, longueur, largeur, hauteur):
        self._dimensions = {'longueur': longueur, 'largeur': largeur, 'hauteur': hauteur}


    def __getitem__(self, key):
        return self._dimensions[key]


    def get_tuple_dimensions(self):
        return self._dimensions['longueur'], self._dimensions['largeur'], self._dimensions['hauteur']


class ConfigurationCable():

    def __init__(self, point_ancrage, nom_sommet_source):
        self._nom_sommet_source = nom_sommet_source
        self._point_ancrage     = point_ancrage


    def get_point_ancrage(self):
        return self._point_ancrage


    def get_nom_sommet_source(self):
        return self._nom_sommet_source


    def __getitem__(self, key):
        if key == 'nom_sommet_source':
            return self._nom_sommet_source

        elif key == 'point_ancrage':
            return self._point_ancrage

        else:
            raise KeyError('nom_sommet_source ou point_ancrage')


class ConfigurationAncrage():

    def __init__(self, configs_cables):
        if len(configs_cables) != 8:
            raise Exception('Une config dancrage doit avoir 8 configs de cable')

        self._configs_cables = configs_cables


    def get_config_cable(self, nom_sommet_source):
        return next(config_cable
                    for config_cable in self._configs_cables
                    if config_cable['nom_sommet_source'] == nom_sommet_source)


    def get_cables(self, sommets_source, diametre_cable):
        return [
            Cable(
                nom_sommet_source = nom_sommet,
                point_ancrage     = self.get_config_cable(nom_sommet).get_point_ancrage(),
                sommet_source     = sommets_source[nom_sommet],
                diametre          = diametre_cable
            )
            for nom_sommet in Pave.noms_sommets_pave
        ]


class Cable():

    def __init__(self, point_ancrage, nom_sommet_source, sommet_source,diametre):
        self.nom_sommet_source = nom_sommet_source
        self.point_ancrage     = point_ancrage
        self.sommet_source     = sommet_source
        self.diametre          = diametre
        self.vecteur           = Vecteur3D.vecteur_depuis_difference_deux_vecteurs(
                                   vecteur_depart  = self.point_ancrage,
                                   vecteur_arrivee = self.sommet_source
                                 )


    def longueur(self):
        return self.vecteur.norme()


    def get_generator_points_discretisation(self, nombre_points=300, inclure_sommet_ancrage=False, inclure_sommet_source=False):
        range_min = 0 if inclure_sommet_ancrage else 1

        range_max = nombre_points + (1 if inclure_sommet_source else 0)  # 1 pour compenser l'intervalle ouvert

        linear_range = range(range_min, range_max)

        return (self.point_ancrage + (i / nombre_points) * self.vecteur for i in linear_range)


    def intersects_cable(self, cable2):

        origin = self.point_ancrage
        direction = self.point_ancrage - self.sommet_source
        direction = direction.get_vecteur_diretion()

        normalePlane1 = cable2.point_ancrage - cable2.sommet_source
        pointPlane1 = cable2.point_ancrage

        normalePlane2 = cable2.sommet_source - cable2.point_ancrage
        pointPlane2 = cable2.sommet_source

        axis = normalePlane2
        centre = pointPlane1

        radius = cable2.diametre/2 + self.diametre/2

        a = direction.scalar_product(direction) - direction.scalar_product(axis)**2
        b = 2*(direction.scalar_product(origin - centre )   - direction.scalar_product(axis)*axis.scalar_product(origin - centre))
        c = (origin - centre).scalar_product(origin - centre )   - axis.scalar_product(origin - centre)**2 - radius**2

        if(b*b - 4*a*c < 0):
              return False

        solution1,solution2 = solutions_formule_quadratique(a,b,c)
        point1 = origin + solution1*direction
        point2 = origin + solution2*direction

        if( (normalePlane1.scalar_product(point1 - pointPlane1) <= 0 ) \
            and (normalePlane2.scalar_product(point1 - pointPlane2) <= 0) ):
            return True

        if( (normalePlane1.scalar_product(point2 - pointPlane1) <= 0 ) \
                and (normalePlane2.scalar_product(point2 - pointPlane2) <= 0) ):
                return True

        return False


    def intersection_avec_pave(self, pave,
                               nombre_points_discretisation = 100,
                               inclure_sommet_ancrage       = False,
                               inclure_sommet_source        = False):

        generateur_points = self.get_generator_points_discretisation(nombre_points = nombre_points_discretisation,
                                                                     inclure_sommet_ancrage = inclure_sommet_ancrage,
                                                                     inclure_sommet_source  = inclure_sommet_source)

        return any(pave.point_appartient_pave(point) for point in generateur_points)


    def entierement_dans_pave(self, pave,
                              nombre_points_discretisation = 100,
                              inclure_sommet_ancrage       = False,
                              inclure_sommet_source        = False):

        generateur_points = self.get_generator_points_discretisation(nombre_points = nombre_points_discretisation,
                                                                     inclure_sommet_ancrage = inclure_sommet_ancrage,
                                                                     inclure_sommet_source  = inclure_sommet_source)

        return all(pave.point_appartient_pave(point) for point in generateur_points)

    def draw(self,origin):
        edge = (0,1)
        verticies = (
            self.sommet_source - origin,self.point_ancrage - origin
            )
        glBegin(GL_LINES)
        for vertex in edge:
                glVertex3fv(verticies[vertex])
        glEnd()


class Pave():

    noms_sommets_pave = ('S000', 'S100', 'S010', 'S110', 'S001', 'S101', 'S011', 'S111')


    @staticmethod
    def point_appartient_pave_origine(point, dimensions):
        '''
        Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
        :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
        :return: False/True
        '''
        long, larg, haut = dimensions.get_tuple_dimensions()

        demi_long, demi_larg, demi_haut = long / 2, larg / 2, haut / 2

        x, y, z = point.get_coordonnees()

        return -demi_long <= x <= demi_long and \
               -demi_larg <= y <= demi_larg and \
               -demi_haut <= z <= demi_haut


    def __init__(self, centre, ypr_angles, dimensions):
        self.centre     = centre
        self.ypr_angles = ypr_angles
        self.dimensions = dimensions


    def rotate(self,delta_yaw,delta_pitch,delta_row):
        self.ypr_angles.incrementer(yaw,pitch,row)

        
    def move(self,delta_x,delta_y,delta_z):
        self.centre += Vecteur3D(delta_x,delta_y,delta_z)

    def changer_systeme_repere_pave_vers_globale(self, point):
        # matrice de rotation
        Rot = self.ypr_angles.get_matrice_rotation()

        res = (Rot * point) + self.centre

        # il faut faire ça sinon le retour est une matrice rot
        return Vecteur3D(res.__getitem__((0,0)), res.__getitem__((1,0)), res.__getitem__((2,0)))


    def sommets_pave_origine(self):
        # dimensions
        long, larg, haut = self.dimensions.get_tuple_dimensions()

        # sommets (coins) du pavé centré dans l'origine
        S000 = Vecteur3D(- long / 2, - larg / 2, - haut / 2)
        S100 = Vecteur3D(+ long / 2, - larg / 2, - haut / 2)
        S010 = Vecteur3D(- long / 2, + larg / 2, - haut / 2)
        S110 = Vecteur3D(+ long / 2, + larg / 2, - haut / 2)
        S001 = Vecteur3D(- long / 2, - larg / 2, + haut / 2)
        S101 = Vecteur3D(+ long / 2, - larg / 2, + haut / 2)
        S011 = Vecteur3D(- long / 2, + larg / 2, + haut / 2)
        S111 = Vecteur3D(+ long / 2, + larg / 2, + haut / 2)

        # sommets (coins) de la source repérés par rapport à son centre
        return [S000, S100, S010, S110, S001, S101, S011, S111]


    def sommets_pave(self):
        '''
        convention utilisé pour les rotations : z-y’-x″ (intrinsic rotations) = Yaw, pitch, and roll rotations
        http://planning.cs.uiuc.edu/node102.html
        http://planning.cs.uiuc.edu/node104.html
        https://en.wikipedia.org/wiki/Euler_angles#Tait.E2.80.93Bryan_angles
        https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix

        On suppose qu'on veut orienter le centre de la source par des angles
        et la position du centre, on calcule les positios des sommets (les coins de la source).
        :return: liste des sommets de la source par rapport au système de repère de la chambre
        '''

        # Sommets
        S_origine = self.sommets_pave_origine()

        return [self.changer_systeme_repere_pave_vers_globale(s) for s in S_origine]


    def get_dictionnaire_sommets(self):
        return {nom: sommet for nom, sommet in zip(self.noms_sommets_pave, self.sommets_pave())}


    def point_appartient_pave(self, point):
        '''
        Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
        :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
        :param centre: centre du pavé repéré dans le sys de coordonnées globale
        :return: False/True
        '''
        Rot = self.ypr_angles \
                  .get_tuple_angles_pour_inverser_rotation() \
                  .get_matrice_rotation()

        point_repere_pave = Rot * (point - self.centre)

        # il faut faire ça parce que l'operation cidessus renvoie une matrice rotation
        point_repere_pave = Vecteur3D(point_repere_pave.__getitem__((0,0)),
                                      point_repere_pave.__getitem__((1,0)),
                                      point_repere_pave.__getitem__((2,0)))

        return self.point_appartient_pave_origine(point_repere_pave, self.dimensions)


    def test_colision_en_autre_pave(self, pave2, k = 10):

        '''
        Tests if there are points on pave1's faces inside pave2.
        the function needs to be called twice to be sure that there are no intersections
        pave1: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
        k: (k+1)^2 = number of points to be tested on each face, the greater the k, the plus reliable the result
        '''
        longueur,largeur, hauteur = self.dimensions.get_tuple_dimensions()

        points_to_be_tested = []

        for i in range (k + 1):
            for j in range(k + 1):
              x = i*longueur/k
              z = j*hauteur/k
              points_to_be_tested.append(Vecteur3D(x,0,z))
              points_to_be_tested.append(Vecteur3D(x,largeur,z))

              x = i*longueur/k
              y = j*largeur/k
              points_to_be_tested.append(Vecteur3D(x,y,0))
              points_to_be_tested.append(Vecteur3D(x,y,hauteur))


              y = i*largeur/k
              z = j*hauteur/k
              points_to_be_tested.append(Vecteur3D(0,y,z))
              points_to_be_tested.append(Vecteur3D(longueur,y,z))

        for index in range(len(points_to_be_tested)):
              points_to_be_tested[index] = (self.ypr_angles.get_matrice_rotation())*points_to_be_tested[index]

              #next line converts from 3d rotation matrix to vecteur3d
              points_to_be_tested[index] = Vecteur3D(points_to_be_tested[index].__getitem__((0,0)),
                                                     points_to_be_tested[index].__getitem__((1,0)),
                                                     points_to_be_tested[index].__getitem__((2,0)))

              points_to_be_tested[index] = points_to_be_tested[index] + self.centre - Vecteur3D(longueur/2,largeur/2,hauteur/2)

              if( pave2.point_appartient_pave(points_to_be_tested[index])):
                      return True

        return False


    def intersection_avec_autre_pave(self, pave, k = 10):

        '''
        Tests if there are inserctions between pave1 and pave2,
        pave1: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
        pave2: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
        k: (k+1)^2 = number of points to be tested on each face, the greater the k, the more reliable the result
        return True if there are no intersections, returns False otherwise
        '''
        if(self.test_colision_en_autre_pave(pave, k)):
            return True

        if(pave.test_colision_en_autre_pave(self, k)):
            return True

        return False
        #FIX POINT_APPARTIENT_PAVE AND POINT_3d


    def est_dans_autre_pave(self, autre):
        return all(autre.point_appartient_pave(sommet) for sommet in self.sommets_pave())


    def changer_a_partir_de_coordonnes_spheriques(source, coordonnees_spheriques, systeme_spherique):
        roh, theta, phi = coordonnees_spheriques.get_coordonnees_spheriques(unite_desiree=UniteAngleEnum.DEGRE)

        # p = centre de la source pour le systeme cartesien à partir du quel le spherique est defini
        p = systeme_spherique.convertir_en_cartesien(coordonnees_spheriques)

        centre_systeme, ypr_angles_systeme = systeme_spherique.get_centre_et_ypr_angles()

        Rot = ypr_angles_systeme.get_tuple_angles_pour_inverser_rotation() \
            .get_matrice_rotation()

        res = Rot * p + centre_systeme

        # il faut faire ça sinon le retour est une matrice rot
        source.centre = Vecteur3D(res.__getitem__((0, 0)), res.__getitem__((1, 0)), res.__getitem__((2, 0)))

        source.ypr_angles = \
            TupleAnglesRotation(
                row=0,
                pitch=phi,
                yaw=theta,
                sequence=SequenceAnglesRotationEnum.YPR,
                unite=UniteAngleEnum.DEGRE  # !!!!!!!!!!!!!!!!!!!!!!!!
            )
    def draw(self,origin,drawFaces = True):
        edges = (
            (0,1),
            (0,2),
            (0,4),
            (1,3),
            (1,5),
            (7,3),
            (7,5),
            (7,6),
            (6,2),
            (6,4),
            (3,2),
            (5,4)
        )
        surfaces = (
            (0,2,6,4),
            (1,3,7,5),
            (5,7,6,4),
            (1,3,2,0),
            (7,3,2,6),
            (1,0,4,5)
        )


        verticies = self.sommets_pave()
        verticiesInOrigin = []

        for v in verticies:
            verticiesInOrigin.append(v - origin)

        color = (0.95,0.95,0)

        if(drawFaces):
            glBegin(GL_QUADS)
            for surface in surfaces:
                for vertex in surface:
                    glColor3fv(color)
                    glVertex3fv(verticiesInOrigin[vertex])
            glEnd()


        color = (0,0,0)

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor3fv(color)
                glVertex3fv(verticiesInOrigin[vertex])
        glEnd()
