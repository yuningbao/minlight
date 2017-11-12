from entites import Cable,Vecteur3D

cable1 = Cable(Vecteur3D(0,0,90),"a",Vecteur3D(5,5,90),1)
cable2 = Cable(Vecteur3D(5,0,90),"b",Vecteur3D(6,6,90),1)

if(cable1.intersects_cable(cable2)):
  print("deu ruim, teve intersecao")
else:
  print("deu bom, nao se cruzaram")
