from numpy import cos, sin, pi, matrix, sqrt, nan
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
    RADIAN = 0
    DEGRE  = 1


class AngleRotationEnum(Enum):
    ROW   = 0
    PITCH = 1
    YAW   = 2


class SequenceAnglesRotationEnum(Enum):
    RPY = 0
    YPR = 1


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