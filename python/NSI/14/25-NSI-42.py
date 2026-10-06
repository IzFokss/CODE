def binaire(a):
    '''convertit un nombre entier a en sa représentation
    binaire sous forme de chaîne de caractères.'''
    if a == 0:
        return '0'
    bin_a = ""
    while a:
        bin_a = str(a % 2) + bin_a
        a = a // 2
    return bin_a


print(f"Convertir 5 en binaire : {binaire(5)}")
print(f"Convertir 25 en binaire : {binaire(25)}")










