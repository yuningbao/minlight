from .parametres import *
from .outils import *

"""
Pa(  xp,  yp,  zp, theta, phi,
   xa11,ya11,za11,
   xa12,ya12,za12,
   xa21,ya21,za21,
   xa22,ya22,za22,
   xa31,ya31,za31,
   xa32,ya32,za32,
   xa41,ya41,za41,
   xa42,ya42,za42,
   n)
"""

Pa = (creerPoint(0, 0, 400), \
      creerPoint(0, 0, 0), \
      creerPoint(0, 500, 400), \
      creerPoint(0, 500, 0), \
      creerPoint(1000, 0, 400), \
      creerPoint(1000, 0, 0), \
      creerPoint(1000, 500, 400), \
      creerPoint(1000, 500, 0))

# ConflitDePosition(100,100,300,0.52,0.24,Pa,1000)

"""
ConflitDePosition(creerPoint(100,100,300),0,0,Pa,1000)
ConflitDePosition(creerPoint(600,250,200),0,0,Pa,1000)
ConflitDePosition(creerPoint(100,50,100),0,0,Pa,1000)
ConflitDePosition(creerPoint(100,200,40),0,0,Pa,1000)
"""

# print(appartientVolumeSoleil(creerPoint(0,0,0), creerPoint(0,0,0), 0, 0))
# print(appartientVolumeSoleil(creerPoint(40,40,40), creerPoint(200,200,200), 0, 0))
# print(appartientVolumeSoleil(creerPoint(200,200,200), creerPoint(200,200,200), 0, 0))
# print(appartientVolumeSoleil(creerPoint(200,200,200), creerPoint(200,200,200), math.pi/4, math.pi/4))
# print(appartientVolumeSoleil(creerPoint(205,205,205), creerPoint(200,200,200), math.pi/4, math.pi/4))
