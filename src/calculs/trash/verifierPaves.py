from entites import Pave,Vecteur3D,TupleAnglesRotation,DimensionsPave
from math import radians

pave1 = Pave(Vecteur3D(56.0,5.0,5.0), TupleAnglesRotation(0,47,0),DimensionsPave(10,10,10))

pave2 = Pave(Vecteur3D(55.0,5.0,5.0),TupleAnglesRotation(90.0,90.0,90.0),DimensionsPave(5,5,5))

if(pave1.intersectsPave(pave2)):
    print("deu ruim, achou intersecao")
else:
    print("deu bom, nao achou intersecao")
