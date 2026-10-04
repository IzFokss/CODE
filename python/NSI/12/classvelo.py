class ClasseVelo:                                                   #Définition de la classe
                                                                    #Documentation/Docstring
    roues = 2

    def __init__(self,marque,prix,masse):
        self.marque = marque
        self.prix =prix
        self.masse =masse


velo1 = ClasseVelo("btwin",250,15)
velo2 = ClasseVelo("rockrider",170,12)




print("L'objet velo1",velo1)
print("L'objet velo2",velo2)
print("Le nombre de roues de velo1 est :",velo1.roues)
print("Le nombre de roues de velo2 est :",velo2.roues)
print("La marque de velo1 est :",velo1.marque)
print("La marque de velo2 est :",velo2.marque)
print("Le prix de velo1 est : ", velo1.prix)
print("La masse de velo2 est : ", velo2.masse)

