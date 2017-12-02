from modeles.entites_systeme_minlight import Cable,Vecteur3D

cable1 = Cable(Vecteur3D(5000,0,0),"a",Vecteur3D(4500,4500,4500),1)
cable2 = Cable(Vecteur3D(0,0,0),"b",Vecteur3D(3500,4500,4500),1)

if(cable1.intersects_cable(cable2)):
  print("deu ruim, teve intersecao")
else:
  print("deu bom, nao se cruzaram")
