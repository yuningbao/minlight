import copy


class CableRobot:

    def __init__(self, chambre, maisonette, source, diametre_cables, config_ancrage):
        self._chambre = copy.deepcopy(chambre)
        self._maisonette = copy.deepcopy(maisonette)
        self._source = copy.deepcopy(source)
        self._diametre_cables = diametre_cables
        self._config_ancrage = copy.deepcopy(config_ancrage)

        # create cables
        sommets_source = self._source.get_dictionnaire_sommets()
        self._cables = self._config_ancrage.get_cables(sommets_source, self._diametre_cables)

    def draw(self, origin,draw_maisonette):
        for cable in self._cables:
            cable.draw(origin)
        self._chambre.draw(origin)
        if( draw_maisonette):
            self._maisonette.draw(origin)
        self._source.draw(origin)

    def rotate_source(self, delta_yaw=0, delta_pitch=0, delta_roll=0):
        self._source.rotate(delta_yaw, delta_pitch, delta_roll)

    def translate_source(self, delta_x=0, delta_y=0, delta_z=0):
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
