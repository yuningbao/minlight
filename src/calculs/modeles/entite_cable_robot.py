from .entites_systeme_minlight import Cable
from src.calculs.simulation.setups.parametres_ancrage import Ideal
import copy
from enum import Enum


class ConfigCables(Enum):
    clock_wise = 1
    simple = 2
    counter_clock_wise = 3
    haut_bas = 4
    haut_mid = 5
    haut_haut = 6


class CableRobot:
    def __init__(self, chambre, maisonette, source, diametre_cables, config_ancrage):
        self._chambre = copy.deepcopy(chambre)
        self._maisonette = copy.deepcopy(maisonette)
        self._source = copy.deepcopy(source)
        self._cables = []  # copy.deepcopy(cables)
        self._diametre_cables = diametre_cables
        self._config_ancrage = copy.deepcopy(config_ancrage)

    def draw(self, origin):
        for cable in self._cables:
            cable.draw(origin)
        self._chambre.draw(origin)
        self._maisonette.draw(origin)
        self._source.draw(origin)

    def rotate_source(self, delta_yaw, delta_row, delta_pitch):
        self._source.rotate(delta_yaw, delta_pitch, delta_row)

    def translate_source(self, delta_x, delta_y, delta_z):
        self._source.translate(delta_x, delta_y, delta_z)

    def set_source_position(self, centre):
        self._source.set_position(centre)

    def set_source_angles(self, angles):
        self._source.set_angles(angles)

    def get_light_centre(self):
        return self._source.get_light_centre()

    def get_light_direction(self):
        return self._source.get_light_direction()

    def get_light_radius(self):
        return self._source.get_light_radius()

    def get_centre(self):
        return self._chambre.get_centre()

    def create_cables(self, configuration_source_down, configuration_source_up, configuration_walls):
        sommets_source = self._source.get_sommets_pave()

        self._cables = self._config_ancrage.get_cables(sommets_source, self._diametre_cables)

    '''
        ancrage_walls_haut_haut = Ideal.get_haut_haut()
        ancrage_walls_haut_mid = Ideal.get_haut_mid()
        ancrage_walls_haut_bas = Ideal.get_haut_bas()
        ancrage_walls = {}
        ancrage_source = self._source.get_dictionnaire_sommets()

        # setting points de ancrage walls
        if configuration_walls == ConfigCables.haut_haut:
            ancrage_walls['S000'] = ancrage_walls_haut_haut['PF_000']
            ancrage_walls['S001'] = ancrage_walls_haut_haut['PF_001']
            ancrage_walls['S010'] = ancrage_walls_haut_haut['PF_010']
            ancrage_walls['S011'] = ancrage_walls_haut_haut['PF_011']
            ancrage_walls['S100'] = ancrage_walls_haut_haut['PF_100']
            ancrage_walls['S101'] = ancrage_walls_haut_haut['PF_101']
            ancrage_walls['S110'] = ancrage_walls_haut_haut['PF_110']
            ancrage_walls['S111'] = ancrage_walls_haut_haut['PF_111']

        elif configuration_walls == ConfigCables.haut_bas:
            ancrage_walls['S000'] = ancrage_walls_haut_bas['PF_000']
            ancrage_walls['S001'] = ancrage_walls_haut_bas['PF_001']
            ancrage_walls['S010'] = ancrage_walls_haut_bas['PF_010']
            ancrage_walls['S011'] = ancrage_walls_haut_bas['PF_011']
            ancrage_walls['S100'] = ancrage_walls_haut_bas['PF_100']
            ancrage_walls['S101'] = ancrage_walls_haut_bas['PF_101']
            ancrage_walls['S110'] = ancrage_walls_haut_bas['PF_110']
            ancrage_walls['S111'] = ancrage_walls_haut_bas['PF_111']

        elif configuration_walls == ConfigCables.haut_mid:
            ancrage_walls['S000'] = ancrage_walls_haut_mid['PF_000']
            ancrage_walls['S001'] = ancrage_walls_haut_mid['PF_001']
            ancrage_walls['S010'] = ancrage_walls_haut_mid['PF_010']
            ancrage_walls['S011'] = ancrage_walls_haut_mid['PF_011']
            ancrage_walls['S100'] = ancrage_walls_haut_mid['PF_100']
            ancrage_walls['S101'] = ancrage_walls_haut_mid['PF_101']
            ancrage_walls['S110'] = ancrage_walls_haut_mid['PF_110']
            ancrage_walls['S111'] = ancrage_walls_haut_mid['PF_111']

        #setting cables down

        if(configuration_source_down == ConfigCables.simple):
            self._cables.append(Cable(ancrage_walls['S000'],'S000',ancrage_source['S000'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S010'],'S010',ancrage_source['S010'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S110'],'S110',ancrage_source['S110'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S100'],'S100',ancrage_source['S100'],self._diametre_cables))

        elif(configuration_source_down == ConfigCables.clock_wise):
            self._cables.append(Cable(ancrage_walls['S000'],'S010',ancrage_source['S010'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S010'],'S110',ancrage_source['S110'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S110'],'S100',ancrage_source['S100'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S100'],'S000',ancrage_source['S000'],self._diametre_cables))

        elif(configuration_source_down == ConfigCables.clock_wise):
            self._cables.append(Cable(ancrage_walls['S000'],'S100',ancrage_source['S010'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S010'],'S000',ancrage_source['S110'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S110'],'S010',ancrage_source['S100'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S100'],'S110',ancrage_source['S000'],self._diametre_cables))

        #setting cables up

        if(configuration_source_up == ConfigCables.simple):
            self._cables.append(Cable(ancrage_walls['S111'],'S111',ancrage_source['S111'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S011'],'S011',ancrage_source['S011'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S001'],'S001',ancrage_source['S001'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S101'],'S101',ancrage_source['S101'],self._diametre_cables))

        elif(configuration_source_up == ConfigCables.counter_clock_wise):
            self._cables.append(Cable(ancrage_walls['S111'],'S011',ancrage_source['S011'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S011'],'S001',ancrage_source['S001'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S001'],'S101',ancrage_source['S101'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S101'],'S111',ancrage_source['S111'],self._diametre_cables))

        elif(configuration_source_up == ConfigCables.clock_wise):
            self._cables.append(Cable(ancrage_walls['S111'],'S101',ancrage_source['S101'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S011'],'S111',ancrage_source['S111'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S001'],'S011',ancrage_source['S011'],self._diametre_cables))
            self._cables.append(Cable(ancrage_walls['S101'],'S001',ancrage_source['S001'],self._diametre_cables))
    '''