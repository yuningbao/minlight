from .entites_systeme_minlight import Cable,Pave
import copy
from enum import Enum




class Config_Cables(Enum):
    clock_wise = 1
    simple = 2
    counter_clock_wise = 3
    corners = 4
    half_height = 5



class Cable_robot():
    def __init__(self,chambre,maisonette,source,cables):
        self._chambre = copy.deepcopy(chambre)
        self._maisonette = copy.deepcopy(maisonette)
        self._source = copy.deepcopy(source)
        self._cables = copy.deepcopy(cables)

    def draw(self,origin):
        for cable in self._cables:
            cable.draw(origin)
        self._maisonette.draw(origin,(0.95,0.95,0.95),True)
        self._source.draw(origin,(0.95,0.95,0),True)
        self._chambre.draw(origin,(0,0,0),False)


    def rotate_source(self,delta_yaw,delta_row,delta_pitch):
        self._source.rotate(delta_yaw,delta_pitch,delta_row)


    def translate_source(self,delta_x,delta_y,delta_z):
        self._source.translate(delta_x,delta_y,delta_z)
    def create_cables(self,configuration_source_up,configuration_source_down,configuration_walls):

        cable_000,cable_001,cable_010,cable_011,cable_100,cable_101,cable_110,cable_111
        ancrage_walls = self._chambre.get_dictionnaire_sommets()
        ancrage_source = self._source.get_dictionnaire_sommets()
        if(configuration_source_up == Config_Cables.simple):
            a = 2
        if(configuration_source_down == Config_Cables.simple):
            a = 2
        if(configuration_walls == Config_Cables.simple):
            a =2
