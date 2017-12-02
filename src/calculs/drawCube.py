from modeles.entite_cable_robot import *
from simulation.setups.parametres_objets import source,maisonette,chambre,centre_chambre
from graphics.robot_visualization import *


def main():

    my_robot = CableRobot(chambre,maisonette,source,5)
    my_robot.create_cables(ConfigCables.simple,ConfigCables.simple,ConfigCables.haut_bas)
    my_drawer = Robot_Visualization(my_robot)
    my_drawer.light_on()
    my_drawer.show()

main()
