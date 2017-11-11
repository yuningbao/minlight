from numpy import cos, sin, pi, matrix, sqrt, nan, arange
from numpy.linalg import pinv
import numpy as np
from pprint import pprint
from enum import *


class Vecteur3D(matrix):
    def __new__(cls, x, y, z):
        return super(Vecteur3D, cls).__new__(cls, "{}; {}; {}".format(x, y, z))

    def __new__(cls, vecteur_depart, vecteur_arrive):
        return vecteur_arrive - vecteur_depart

    def get_coordonnees(self):
        return self.item(0), self.item(1), self.item(2)

    def norme(self):
        return sqrt((self.T *self).item((0,0)))

    def get_vecteur_diretion(self):
        return self.copy() / self.norme()


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

        def rpy(): return self._matrix_x * self._matrix_y * self._matrix_z

        def ypr(): return self._matrix_z * self._matrix_y * self._matrix_x

        switch = {
            SequenceAnglesRotationEnum.RPY : rpy,
            SequenceAnglesRotationEnum.YPR : ypr
        }

        self._matrice_rotation = switch[self._sequence]


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
        self._point_ancrage = point_ancrage

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

    def get_cables(self, sommets_source):
        return [
            Cable(
                nom_sommet_source = nom_sommet,
                point_ancrage     = self.get_config_cable(nom_sommet).get_point_ancrage(),
                sommet_source     = sommets_source[nom_sommet]
            )
            for nom_sommet in Pave.noms_sommets_pave
        ]


class Cable():

    def __init__(self, point_ancrage, nom_sommet_source, sommet_source):
        self.nom_sommet_source = nom_sommet_source
        self.point_ancrage     = point_ancrage
        self.sommet_source     = sommet_source
        self.vecteur           = Vecteur3D(
                                   vecteur_depart  = self._point_ancrage,
                                   vecteur_arrivee = self._sommet_source
                                 )

    def longueur(self):
        return self.vecteur.norme()

    def get_generator_points_discretisation(self, nombre_points=300, inclure_sommet_ancrage=False, inclure_sommet_source=False):
        range_min = 0 if inclure_sommet_ancrage else 1

        range_max = nombre_points + (1 if inclure_sommet_source else 0)  # 1 pour compenser l'intervalle ouvert

        linear_range = range(range_min, range_max)

        return (self.point_ancrage + (i / nombre_points) * self.vecteur for i in linear_range)

class Pave():
    noms_sommets_pave = ('S000', 'S100', 'S010', 'S110', 'S001', 'S101', 'S011', 'S111')

    def __init__(self, centre, ypr_angles, dimensions):
        self.centre     = centre
        self.ypr_angles = ypr_angles
        self.dimensions = dimensions

    def sommets_pave_origine(self):
        # dimensions
        long, larg, haut = self._dimensions.get_tuple_dimensions()

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
        :param centreSoleil: centre de la source dans le système de repère de la chambre
        :param theta: remplir...
        :param phi: remplir...
        :param dimensionsSource: (dictionnaire) longueur, largeur, hauteur du pave de la source
        :return: liste des sommets de la source par rapport au système de repère de la chambre
        '''

        # Sommets
        S_origine = self.sommets_pave_origine()

        # matrice de rotation
        Rot = self._ypr_angles.get_matrice_rotation()

        # rotation
        S_origine_rot = [Rot * s for s in S_origine]

        # translation
        S = [s + self._centre for s in S_origine_rot]

        return S

    def get_dictionnaire_sommets(self):
        return {nom: sommet for nom, sommet in zip(self.noms_sommets_pave, self.sommets_pave())}


class CoordonnesSpherique():
    def __init__(self, roh, theta, phi):
        self.roh   = roh
        self.theta = theta
        self.phi   = phi

    def get_coordonnees_spheriques(self):
        return self.roh, self.theta, self.phi


class SystemeRepereSpherique():
    def __init__(self, centre, ypr_angles):
        self.centre     = centre
        self.ypr_angles = ypr_angles

    def get_centre_et_ypr_angles(self):
        return self.centre, self.ypr_angles

    def convertir_en_cartesien(self, coordonnees_spheriques):
        roh, theta, phi = coordonnees_spheriques.get_coordonnees_spheriques()

        return Vecteur3D(roh * cos(phi) * cos(theta),
                         roh * cos(phi) * sin(theta),
                         roh * sin(phi))


class IntervalleLineaire():
    def __new__(cls, min, max, pas):
        return np.arange(start=min, stop=max, step=pas)


class SpaceRechercheAnglesLimites():
    def __init__(self, intervalle_rho, intervalle_phi, intervalle_theta):
        self.intervalle_rho   = intervalle_rho
        self.intervalle_phi   = intervalle_phi
        self.intervalle_theta = intervalle_theta

    def get_intervalles(self):
        return self.intervalle_rho, self.intervalle_phi, self.intervalle_theta