from math import cos, sin, asin, atan2, pi


# coord spheriques prenant y comme nord

def x_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle)*sin(longitude_angle)


def y_sph(latitude_angle, longitude_angle):
    return cos(latitude_angle)*cos(longitude_angle)


def z_sph(latitude_angle):
    return sin(latitude_angle)

# adicionar angulo entre o observador e o norte e também o angulo do observador olhando pra cima
# basta adicionar os angulos em cada saída, aparentemente...


def position_soleil (date, latitude, heure, orientation_nord = 0.0, orientation_zenit=0.0):
    '''

    Fonction qui donne la position du soleil vue par un observeur sur Terre.

    :param date: String en format '29/07'
    :param latitude: string en format '63.2/N', ou '63.2/S'
    :param heure: string en format '18:48'
    :param orientation_nord: float entre 0.0 et 360.0
    :param orientation_zenit: float entre 0.0 et 90.0
    :return: coordonnees [sol_azimut, sol_altitude] pour la position solaire vue.

    '''
    dic_mois = \
        {
            '00': 0,
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
    date2 = date.split('/')
    i = 0
    n = int(date2[0])
    while (date2[1] != list(dic_mois.keys())[i]):
        n += dic_mois[list(dic_mois.keys())[i]]
        i += 1


    # recuperer la valeur de latitude
    if latitude.split('/')[1] == 'N':
        lat = pi/180*float(latitude.split('/')[0])
    else:
        lat = -1*pi/180*float(latitude.split('/')[0])


    # nombre de minutes dans l'horaire informé
    mins = int(heure.split(':')[0])*60 + int(heure.split(':')[1])


    # declin = angle de declinaison, calculé à partir de n
    declin = -pi / 180 * 23.45 * cos(2 * pi * (n + 10) / 365)


    # determiner la position [soleil_aizmut, soleil_altitude] du soleil:
    w_Terre = 2*pi/(24*60)  #en rad/mminute

    x = x_sph(declin, w_Terre*mins)
    y = y_sph(declin, w_Terre*mins) * sin(lat) + z_sph(declin) * cos(lat)
    z = -y_sph(declin, w_Terre*mins) * cos(lat) + z_sph(declin) * sin(lat)

    soleil_altitude = asin(z)*180/pi  # en degres

    x_error = 0.001
    y_error = 0.001
    if abs(x)<x_error:
        if y>=0:
            soleil_azimut = 0
        else:
            soleil_azimut = 180

    elif abs(y)<y_error:
        if x>=0:
            soleil_azimut = 90
        else:
            soleil_azimut = 270

    else:
        if x>0 and y>0:
            soleil_azimut = atan2(x, y)
        elif x>0 and y<0:
            soleil_azimut = atan2(-y, x)*180/pi + 90
        elif x<0 and y<0:
            soleil_azimut = atan2(-x, -y)*180/pi + 180
        else:
            soleil_azimut = atan2(y, -x)*180/pi + 270


    return [soleil_azimut-orientation_nord, soleil_altitude-orientation_zenit]


# test


print(position_soleil('03/03', '15.3/N', '12:01'))
print('')
for i in range(0, 23):
    print(position_soleil('03/03', '15.3/N', '{}:00'.format(i), 40, 30))