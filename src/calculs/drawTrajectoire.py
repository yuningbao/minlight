from modeles.entite_cable_robot import CableRobot
from src.calculs.graphics.robotvisualization import *
from setups import parametres_ancrage, configuration_ancrage
from src.calculs.setups.parametres_objets import source, maisonette, chambre
from src.calculs.dynamique.trajectoire import Trajectoire, Configuration

points_fixes = parametres_ancrage.Ideal.get_haut_haut()

config_ancrage = configuration_ancrage.get_simple(points_fixes)


def main():
    my_robot = CableRobot(chambre, maisonette, source, 5, config_ancrage)
    my_drawer = RobotVisualization(my_robot,True)
#    my_drawer.light_on()
    my_trajectoire = Trajectoire('03/03','0.3/N','8:01','15:00',100,2000)
    trajectory = my_trajectoire.get_configurations()
    for p in trajectory:
        print("ponto + " + str(p.get_centre()))
    speed = 2000
    my_drawer.draw_trajectory(trajectory, my_trajectoire.intervalle,speed)

main()
