from outils import point_3d, point_appartient_pave, matrice_rotation_z1_y2_x3
from math import radians

def verifierPaves(pave1,pave2,k = 5):
    '''
    Tests if there are inserctions between pave1 and pave2,
    pave1: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
    pave2: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
    k: (k+1)^2 = number of points to be tested on each face, the greater the k, the plus reliable the result
    return True if there are no intersections, returns False otherwise
    '''

    if(!testPave(pave1,pave2,k)):
        return False
    if(!testPave(pave2,pave1,k)):
        return False
    return True


def testPave(pave1,pave2,k):

    '''
    Tests if there are points on pave1's faces inside pave2.
    the function needs to be called twice to be sure that there are no intersections
    pave1: dictionary with dimensions(dictionary),centre(matrix 3x1), ypr_angles(dictionary)
    k: (k+1)^2 = number of points to be tested on each face, the greater the k, the plus reliable the result
    '''
#k = nombre de points par ligne
#return true si il y une intersection
      points_to_be_tested = []
      for i in range (k + 1):
        for j in range (k + 1):
          y = i*pave1['dimensions']['largeur']/k
          z = j*pave1['dimensions']['hauteur']/k
          points_to_be_tested.append(point_3d(0,y,z))
          points_to_be_tested.append(point_3d(pave1['dimensions']['longueur'],y,z))
      for i in range (k + 1):
        for j in range(k + 1):
          x = i*pave1['dimensions']['longueur']/k
          z = j*pave1['dimensions']['hauteur']/k
          points_to_be_tested.append(point_3d(x,0,z))
          points_to_be_tested.append(point_3d(x,pave1['dimensions']['largeur'],z))

      for i in range(k + 1):
        for j in range(k + 1):
          x = i*pave1['dimensions']['longueur']/k
          y = j*pave1['dimensions']['largeur']/k
          points_to_be_tested.append(point_3d(x,y,0))
          points_to_be_tested.append(point_3d(x,y,pave1['dimensions']['hauteur']))


      for index in range(len(points_to_be_tested)):
          points_to_be_tested[index] = matrice_rotation_z1_y2_x3(pave1['ypr_angles'])*points_to_be_tested[index]
          points_to_be_tested[index] = points_to_be_tested[index] + pave1['centre']- point_3d(pave1['dimensions']['longueur']/2,pave1['dimensions']['largeur']/2,pave1['dimensions']['hauteur']/2)
    #  i = 0
      for point in points_to_be_tested:
          if(point_appartient_pave(point,pave2['centre'],pave2['ypr_angles'],pave2['dimensions'])):
    #            print('Point ' + str(point) +  '  belongs to cube: ')
    #            print('centre: ' + str(pave2['centre'].transpose()))
    #            print('ypr_angles: ' + str(pave2['ypr_angles']))
    #            print('dimensions: ' + str(pave2['dimensions']))
    #            print('ponto ruim:' + str(i))
                return False
          else:
              print(str(i) + ':::Point ' + str(point) +  ' doesnt belong to cube: ')
        #      print('centre: ' + str(pave2['centre'].transpose()))
    #          print('ypr_angles: ' + str(pave2['ypr_angles']))
    #          print('dimensions: ' + str(pave2['dimensions']))
    #      i += 1

      return True

pave1 = {'dimensions':{'longueur' : 10, 'largeur' : 10 , 'hauteur' : 10 },
        'centre': point_3d(5.0,5.0,5.0),
        'ypr_angles':{'yaw' : 0, 'pitch' : 0, 'row' : 0}}
pave2 =  {'dimensions':{'longueur' : 5, 'largeur' : 5 , 'hauteur' : 5 },
        'centre' : point_3d(5.0,5.0,5.0),
        'ypr_angles':{'yaw' : radians(90), 'pitch' : radians(90), 'row' : radians(90)}}

if(verifierPaves(pave2,pave1, 2)):
    print("nao achou intersection, OK!1")
else:
    print("deu ruim, achou intersection1")
print('SEGUNDO TESTE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
if(verifierPaves(pave1,pave2, 2)):
    print("nao achou intersection, OK!2")
else:
    print("deu ruim, achou intersection2")
