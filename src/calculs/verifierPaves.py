
def verifierPaves(pave1,pave2,k = 50)
#k = nombre de points par ligne
#return true si il y une intersection
      points_to_be_tested = []
      for i in range (k + 1):
        for j in range (k + 1):
          y = i*pave1['largeur']/k
          z = j*pave1['hauteur']/k
          points_to_be_tested.append(point_3d(0,y,z))
          points_to_be_tested.append(point_3d(pave1['longueur'],y,z))
      for i in range (k + 1):
        for j in range(k + 1):
          x = i*pave1['longueur']/k
          z = j*pave1['hauteur']/k
          points_to_be_tested.append(point_3d(x,0,z))
          points_to_be_tested.append(point_3d(x,pave1['largeur'],z))

      for i in range(k + 1):
        for j in range(k + 1):
          x = i*pave1['longueur']/k
          y = j*pave1['largeur']/k
          points_to_be_tested.append(point_3d(x,y,0))
          points_to_be_tested.append(point_3d(x,y,pave1['hauteur']))

      for point in points_to_be_tested:
        point = matrice_rotation_z1_y2_x3(pave1['ypr_angles'])*point
        point = point + pave1['centre']- point_3d(pave1['longueur']/2,pave1['largeur']/2,pave1['hauteur']/2)

      dimensions = [pave1['longueur'],pave1['largeur'],pave1['hauteur']]
      for point in points_to_be_tested:
          if(point_appartient_pave(point,pave1['centre'],pave1['ypr_angles'],dimensions)):
              return True

      return False
