class CompteBancaire:
    def __init__(self,nom):
        self._nom = nom
        self._solde = 0


    def __str__(self,nom,solde):
        return f"{self._nom} {self._solde}"

    def get_nom(self):
        print("Récupération du nom")
        return self._nom


    def get_solde(self):
        print("Récupération du solde")
        return self._solde

    


print("Attention votre solde est insuffisant pour pouvoir faire ce retrait")
