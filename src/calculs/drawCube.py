from modeles.entite_cable_robot import CableRobot
from graphics.robot_visualization import *
from setups import parametres_ancrage, configuration_ancrage
from setups.parametres_objets import source, maisonette, chambre

points_fixes = parametres_ancrage.Ideal.get_haut_haut()

config_ancrage = configuration_ancrage.get_simple(points_fixes)


def main():
    my_robot = CableRobot(chambre, maisonette, source, 5, config_ancrage)
    my_drawer = Robot_Visualization(my_robot)
    # my_drawer.light_on()
    my_drawer.show()

main()
