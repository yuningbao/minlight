from .entites_systeme_minlight import Cable,Pave
import copy

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
