class Personne : 
    def __init__(self, nombre, genre,age):
        self._prenom = nombre
        self._genre = genre
        self._age = age
    def __repr__(self) -> str:
        return f"{self._prenom, self._genre, self._age}"
    def __str__(self) -> str:
        return f"{self._prenom, self._genre, self._age}"
    def get_age(self):
        print("Récupération de l'age de la personne")
        return self._age
    def set_age(self,age):
        print("Changement de l'age de la personne")
        self._age = age
        return self._age
    def del_genre(self):
        print("Deletion de l'age de la personne")
        self.genre = ""
        return self._genre
    def set_genre(self,genre):
        print("Modification du genre de la personne")
        self._genre = genre
        return self._genre

        
alex = Personne("Alex","masculin",15)
bob = Personne("Bob","feminin",20)
beatrice = Personne("Beatrice","féminin",14)
elsa = Personne("Elsa","féminin",17)

print(alex)
print("Le prénom est :",alex._prenom)
print("Le genre est :",alex._genre)
print("L' age est :",alex._age)

print(bob)
print("Le prenom est :",bob._prenom)
print("Le genre est :",bob._genre)
print("L' age est :",bob._age)

print(beatrice)
print("Le prenom est :",beatrice._prenom)
print("Le genre est :",beatrice._genre)
print("L' age est :",beatrice._age)

print(elsa)
print("Le prenom est :",elsa._prenom)
print("Le genre est :",elsa._genre)
print("L' age est :",elsa._age)

print("Modification avec getter et setter")
print("L'age d'Elsa est:",elsa.get_age())
print("Les attributs d'Elsa sont :",elsa)

elsa.set_age(98)
print("L'age d'Elsa est:",elsa.get_age())
print("Les attributs d'Elsa sont :",elsa)

elsa.del_genre()
print("Les attributs d'Elsa sont :",elsa)
elsa.set_genre("masculin")
print("Les attributs d'Elsa sont :",elsa)



