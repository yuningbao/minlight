from math import cos, sin, asin, atan2, pi
#from src.calculs.modeles.entites_mathemathiques import *


def x_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle)*sin(longitude_angle)


def y_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle)*cos(longitude_angle)


def z_sph(latitude_angle):
    return sin(latitude_angle)

# secondes dans un horaire donné
def secondes_dans_horaire (heure1):
    return 60* (int(heure1.split(':')[0])*60 + int(heure1.split(':')[1]))


# angle en degrés entre le nord et le point donné (sens horaire)
def point_azimut (x, y, x_error=0.001, y_error=0.001):
    if abs(x) < x_error:
        if y >= 0:
            return 0
        else:
            return 180

    elif abs(y) < y_error:
        if x >= 0:
            return 90
        else:
            return 270

    else:
        if x > 0 and y > 0:
            return atan2(x, y)
        elif x > 0 and y < 0:
            return atan2(-y, x) * 180 / pi + 90
        elif x < 0 and y < 0:
            return atan2(-x, -y) * 180 / pi + 180
        else:
            return atan2(y, -x) * 180 / pi + 270



class Trajectoire():

    def __init__(self, date, latitude, heure_initiale, heure_finale,
                intervalle, orientation_nord = 0.0, orientation_zenit=0.0):
        self.date = date
        self.latitude = latitude
        self.heure_initiale =heure_initiale
        self.heure_finale = heure_finale
        self.intervalle = intervalle
        self.orientation_nord = orientation_nord
        self.orientation_zenit = orientation_zenit

# coord spheriques prenant y comme nord





    '''
    Fonction qui donne la position du soleil vue par un observeur sur Terre.

    :param date: String en format '29/07'
    :param latitude: string en format '63.2/N', ou '63.2/S'
    :param heure: string en format '18:48'
    :param orientation_nord: float entre 0.0 et 360.0
    :param orientation_zenit: float entre 0.0 et 90.0
    :return: coordonnees [sol_azimut, sol_altitude] pour la position solaire vue.

    '''

    def position_soleil (self, heure):
        secs = 60 * (int(heure.split(':')[0]) * 60 + int(heure.split(':')[1]))
        return self.position_soleil_secondes(secs)

    def position_soleil_secondes (self, secs):

        dic_mois = \
             {
                 '01': 31,
                 '02': 28,
                 '03': 31,
                 '04': 30,
                 '05': 31,
                 '06': 30,
                 '07': 31,
                 '08': 31,
                 '09': 30,
                 '10': 31,
                 '11': 30,
                 '12': 31
             }

        # calcule le nombre n de jours dans la date (n=1 si date == '01/01')

        n = int(self.date.split('/')[0])

        for key in list(dic_mois.keys()):
            if key != self.date.split('/')[1]:
                n += dic_mois[key]
            else:
                break

        # recuperer la valeur de latitude

        if self.latitude.split('/')[1] == 'N':
            lat = pi/180*float(self.latitude.split('/')[0])
        else:
            lat = -1*pi/180*float(self.latitude.split('/')[0])


        # declin = angle de declinaison, calculé à partir de n
        declin = -pi / 180 * 23.45 * cos(2 * pi * (n + 10) / 365)


        # determiner la position [soleil_aizmut, soleil_altitude] du soleil:
        w_Terre = 2*pi/(24*60*60)  #en rad/seconde

        x = x_sph(declin, w_Terre*secs)
        y = y_sph(declin, w_Terre*secs) * sin(lat) + z_sph(declin) * cos(lat)
        z = -y_sph(declin, w_Terre*secs) * cos(lat) + z_sph(declin) * sin(lat)

        soleil_altitude = asin(z)*180/pi  # en degres
        soleil_azimut = point_azimut(x, y)

        return [soleil_azimut-self.orientation_nord, soleil_altitude-self.orientation_zenit]



    # Como resolver o problema de que  metodo position_soleil_seconds não vai mais variar? (o return agora é constante)
    # definir um metodo separado que transforma '13:21' em segundos
    def get_trajectoire (self):
        points_trajectoire = []

        n_points = int((secondes_dans_horaire(self.heure_finale)-secondes_dans_horaire(self.heure_initiale))/self.intervalle)
        for i in range(n_points):
            points_trajectoire.append(
                self.position_soleil_secondes(secondes_dans_horaire(self.heure_initiale) + i* self.intervalle));
        return points_trajectoire



# test

traj = Trajectoire('03/03', '15.3/N', '12:01', '16:00', 600)
a = traj.position_soleil('12:01')
print(a)

print(traj.get_trajectoire())
'''
print(position_soleil('03/03', '15.3/N', '12:01'))
print('')
for i in range(0, 23):
    print(position_soleil('03/03', '15.3/N', '{}:00'.format(i), 40, 30))
'''

#print(get_trajectoire('03/03', '15.3/N', '12:01', '16:30', 600))
