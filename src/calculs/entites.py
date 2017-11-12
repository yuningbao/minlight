from numpy import cos, sin, pi, matrix, sqrt, nan, arange
from numpy.linalg import pinv
import numpy as np
from pprint import pprint
from enum import *
from outils2 import solutions_formule_quadratique

class Vecteur3D(matrix):
    def __new__(cls, x, y, z):
        return super(Vecteur3D, cls).__new__(cls, "{}; {}; {}".format(x, y, z))

    @staticmethod
    def vecteur_depuis_difference_deux_vecteurs(vecteur_depart, vecteur_arrivee):
        return vecteur_arrivee - vecteur_depart

    def get_coordonnees(self):
        return self.item(0), self.item(1), self.item(2)

    def norme(self):
        return sqrt((self.T *self).item((0,0)))

    def get_vecteur_diretion(self):
        return self.copy() / self.norme()
    def scalar_product(self,v):
        return self.item(0)*v.item(0) + self.item(1)*v.item(1) + self.item(2)*v.item(2)


class UniteAngleEnum(Enum):
    INCONU = 0
    RADIAN = 1
    DEGRE  = 2


class AngleRotationEnum(Enum):
    INCONU = 0
    ROW    = 1
    PITCH  = 2
    YAW    = 3


class SequenceAnglesRotationEnum(Enum):
    INCONU = 0
    RPY = 1
    YPR = 2


class TupleAnglesRotation():
    def __init__(self, row, pitch, yaw,
                 sequence = SequenceAnglesRotationEnum.YPR,
                 unite    = UniteAngleEnum.DEGRE):

        self._row      = row
        self._pitch    = pitch
        self._yaw      = yaw
        self._sequence = sequence
        self._unite    = unite

        self._matrix_x = MatriceRotation3D(
            angle  = AngleRotationEnum.ROW,
            valeur = self._row,
            unite  = self._unite
        )

        self._matrix_y = MatriceRotation3D(
            angle  = AngleRotationEnum.PITCH,
            valeur = self._pitch,
            unite  = self._unite
        )

        self._matrix_z = MatriceRotation3D(
            angle  = AngleRotationEnum.YAW,
            valeur = self._yaw,
            unite  = self._unite
        )

        if self._sequence == SequenceAnglesRotationEnum.RPY:
            self._matrice_rotation = self._matrix_x.dot(self._matrix_y.dot(self._matrix_z))

        elif self._sequence == SequenceAnglesRotationEnum.YPR:
            self._matrice_rotation = self._matrix_z.dot(self._matrix_y.dot(self._matrix_x))

        else:
            raise Exception('SequenceAnglesRotationEnum inconu')


    def get_angles(self):
        def rpy(): return self._row, self._pitch, self._yaw

        def ypr(): return self._yaw, self._pitch, self._row

        switch = {
            SequenceAnglesRotationEnum.RPY : rpy,
            SequenceAnglesRotationEnum.YPR : ypr
        }

        return switch[self._sequence]()

    def get_unite(self):
        return self._unite

    def get_matrice_rotation(self):
        return self._matrice_rotation

    def get_tuple_angles_pour_inverser_rotation(self):
        return TupleAnglesRotation(
            row      = -self._row,
            pitch    = -self._pitch,
            yaw      = -self._yaw,
            sequence = SequenceAnglesRotationEnum.RPY if self._sequence == SequenceAnglesRotationEnum.YPR else
                       SequenceAnglesRotationEnum.YPR if self._sequence == SequenceAnglesRotationEnum.RPY else
                       SequenceAnglesRotationEnum.INCONU,
            unite    = self._unite
        )



class MatriceRotation3D(matrix):

    ROTATION_X_STR = '1,   0,    0 ;' +\
                     '0, {c}, -{s} ;' +\
                     '0, {s},  {c}  '

    ROTATION_Y_STR = ' {c}, 0, {s} ;' + \
                     '   0, 1,   0 ;' + \
                     '-{s}, 0, {c}  '

    ROTATION_Z_STR = '{c}, -{s}, 0 ;' + \
                     '{s},  {c}, 0 ;' + \
                     '  0,    0, 1  '

    ROTATION_STR_SWITCH = {
        AngleRotationEnum.ROW   : ROTATION_X_STR,
        AngleRotationEnum.PITCH : ROTATION_Y_STR,
        AngleRotationEnum.YAW   : ROTATION_Z_STR
    }

    def __new__(cls, angle, valeur, unite = UniteAngleEnum.DEGRE):
        radians = valeur if unite == UniteAngleEnum.RADIAN else valeur * pi / 180

        str = cls.ROTATION_STR_SWITCH[angle].format(s = sin(radians), c = cos(radians))

        return super(MatriceRotation3D, cls).__new__(cls, str)

    def __init__(self, angle, valeur, unite):
        self._angle  = angle
        self._valeur = valeur
        self._unite  = unite


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

    def intersects_cable(self,cable2):

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
        return False;


class Pave():
    noms_sommets_pave = ('S000', 'S100', 'S010', 'S110', 'S001', 'S101', 'S011', 'S111')


    def __init__(self, centre, ypr_angles, dimensions):
        self.centre     = centre
        self.ypr_angles = ypr_angles
        self.dimensions = dimensions


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

class CoordonnesSpherique():
    def __init__(self, roh, theta, phi, unite):
        self.roh   = roh
        self.theta = theta
        self.phi   = phi
        self.unite = unite

    def get_coordonnees_spheriques(self, unite_desiree = UniteAngleEnum.INCONU):
        if unite_desiree == self.unite or unite_desiree == UniteAngleEnum.INCONU:
            return self.roh, self.theta, self.phi

        elif unite_desiree == UniteAngleEnum.DEGRE and self.unite == UniteAngleEnum.RADIAN:
            return self.roh, self.theta * 180 / pi, self.phi * 180 / pi

        elif unite_desiree == UniteAngleEnum.RADIAN and self.unite == UniteAngleEnum.DEGRE:
            return self.roh, self.theta * pi / 180, self.phi * pi / 180

        else:
            raise Exception('pbm dunité')

class SystemeRepereSpherique():
    def __init__(self, centre, ypr_angles):
        self.centre     = centre
        self.ypr_angles = ypr_angles

    def get_centre_et_ypr_angles(self):
        return self.centre, self.ypr_angles

    def convertir_en_cartesien(self, coordonnees_spheriques):
        roh, theta, phi = coordonnees_spheriques.get_coordonnees_spheriques(unite_desiree=UniteAngleEnum.RADIAN)

        return Vecteur3D(roh * cos(phi) * cos(theta),
                         roh * cos(phi) * sin(theta),
                         roh * sin(phi))


class IntervalleLineaire():
    def __new__(cls, min, max, pas):
        return np.arange(start=min, stop=max, step=pas)


class SpaceRechercheAnglesLimites():
    def __init__(self, intervalle_rho, intervalle_phi, intervalle_theta, unite):
        self.intervalle_rho   = intervalle_rho
        self.intervalle_phi   = intervalle_phi
        self.intervalle_theta = intervalle_theta
        self.unite            = unite

    def get_intervalles(self):
        return self.intervalle_rho, self.intervalle_phi, self.intervalle_theta
